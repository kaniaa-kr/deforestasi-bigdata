"""Ingest NASA FIRMS (VIIRS SNPP) -> raw CSV + silver Parquet di data lake (MinIO)."""
import csv
import hashlib
import io
import os
import sys
from datetime import date, timedelta

import requests

from common import lake

BASE_URL = "https://firms.modaps.eosdis.nasa.gov/api"
SOURCE = os.environ.get("FIRMS_SOURCE", "VIIRS_SNPP_NRT")
BBOX = os.environ.get("AOI_BBOX", "94.5,-6.5,119.5,6.5")  # west,south,east,north

REQUIRED_COLS = ["latitude", "longitude", "acq_date", "acq_time",
                 "satellite", "confidence", "frp", "daynight"]
SILVER_COLS = ["hotspot_id", "latitude", "longitude", "acq_date", "acq_time",
               "acq_datetime_utc", "satellite", "instrument", "confidence", "frp",
               "daynight", "bright_ti4", "bright_ti5", "scan", "track",
               "version", "type", "source"]


def raw_key(day: str) -> str:
    return f"raw/firms/source={SOURCE}/dt={day}/firms_{SOURCE}_{day}.csv"


def silver_key(day: str) -> str:
    return f"silver/firms/source={SOURCE}/dt={day}/part-0000.parquet"


def _get(path: str, timeout=(10, 180)) -> str:
    """GET ke FIRMS. '{KEY}' pada path diganti MAP_KEY. Pesan error TIDAK memuat URL."""
    key = os.environ.get("FIRMS_MAP_KEY", "")
    if not key or key.startswith("ganti"):
        raise RuntimeError("FIRMS_MAP_KEY belum diisi di .env")
    try:
        r = requests.get(f"{BASE_URL}/{path.replace('{KEY}', key)}", timeout=timeout)
    except requests.RequestException as e:
        raise RuntimeError(f"Request FIRMS gagal ({type(e).__name__})") from None
    if r.status_code == 429:
        raise RuntimeError("FIRMS rate limit (HTTP 429), coba lagi nanti")
    if r.status_code != 200:
        raise RuntimeError(f"FIRMS HTTP {r.status_code}")
    return r.text


def check_availability(day: str) -> None:
    """Pastikan data untuk 'day' sudah tersedia. Format tak dikenal -> peringatan saja."""
    text = _get(f"data_availability/csv/{{KEY}}/{SOURCE}")
    for r in csv.DictReader(io.StringIO(text)):
        if r.get("data_id") == SOURCE and r.get("max_date"):
            if day > r["max_date"]:
                raise RuntimeError(f"Data {day} belum tersedia (max_date={r['max_date']})")
            print(f"OK: {SOURCE} tersedia sampai {r['max_date']}")
            return
    print("WARN: format data_availability tidak dikenali, lanjut tanpa pengecekan")


def validate_csv(text: str, day: str) -> int:
    reader = csv.DictReader(io.StringIO(text))
    cols = reader.fieldnames or []
    missing = [c for c in REQUIRED_COLS if c not in cols]
    if missing:
        raise RuntimeError(f"Respons FIRMS tidak valid. Kolom hilang: {missing}. Header: {cols[:6]}")
    west, south, east, north = map(float, BBOX.split(","))
    total = bad = 0
    for r in reader:
        total += 1
        try:
            lat, lon = float(r["latitude"]), float(r["longitude"])
        except ValueError:
            bad += 1
            continue
        if not (south <= lat <= north and west <= lon <= east) or r["acq_date"] != day:
            bad += 1
    if total and bad / total > 0.01:
        raise RuntimeError(f"Validasi gagal: {bad}/{total} baris di luar bbox atau tanggal salah")
    if total == 0:
        print(f"WARN: 0 baris untuk {day} (mungkin memang tidak ada titik api)")
    return total


def fetch_day(day: str) -> dict:
    text = _get(f"area/csv/{{KEY}}/{SOURCE}/{BBOX}/1/{day}").strip()
    rows = validate_csv(text, day)
    key = raw_key(day)
    lake.put_bytes(key, (text + "\n").encode())
    print(f"raw {day}: {rows} baris -> {key}")
    return {"day": day, "raw_key": key, "rows": rows}


def normalize(df, source: str):
    """Normalisasi skema. Dipakai juga oleh loader arsip supaya skema silver identik."""
    import pandas as pd

    df = df.copy()
    df["acq_time"] = df["acq_time"].astype(str).str.zfill(4)
    df["acq_datetime_utc"] = pd.to_datetime(
        df["acq_date"].astype(str) + " " + df["acq_time"].str[:2] + ":" + df["acq_time"].str[2:],
        utc=True)
    df["confidence"] = df["confidence"].astype(str).str.lower()
    if "type" in df.columns:
        df["type"] = pd.to_numeric(df["type"], errors="coerce").astype("Int64")
    else:
        df["type"] = pd.array([pd.NA] * len(df), dtype="Int64")
    df["source"] = source
    df["hotspot_id"] = [
        hashlib.md5(f"{a:.5f}|{o:.5f}|{d}|{t}|{s}".encode()).hexdigest()[:16]
        for a, o, d, t, s in zip(df["latitude"], df["longitude"], df["acq_date"],
                                 df["acq_time"], df["satellite"])
    ]
    df = df.drop_duplicates("hotspot_id")
    return df[[c for c in SILVER_COLS if c in df.columns]]


def build_silver(day: str) -> dict:
    import pandas as pd

    raw = lake.get_bytes(raw_key(day))
    df = pd.read_csv(io.BytesIO(raw), dtype={"acq_time": str, "confidence": str, "satellite": str})
    key = silver_key(day)
    raw_rows = len(df)
    if df.empty:
        if lake.exists(key):
            lake.delete(key)  # supaya hasil lama tidak tertinggal saat rerun
        return {"day": day, "raw_rows": 0, "silver_rows": 0}
    out = normalize(df, SOURCE)
    buf = io.BytesIO()
    out.to_parquet(buf, index=False, compression="snappy")
    lake.put_bytes(key, buf.getvalue())
    print(f"silver {day}: {raw_rows} -> {len(out)} baris (setelah dedup) -> {key}")
    return {"day": day, "raw_rows": raw_rows, "silver_rows": len(out)}


def _cli() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "check":
        yday = (date.today() - timedelta(days=1)).isoformat()
        check_availability(yday)
        text = _get(f"area/csv/{{KEY}}/{SOURCE}/{BBOX}/1/{yday}")
        lines = text.strip().splitlines()
        print(f"Tes {yday}: {max(len(lines) - 1, 0)} baris")
        print("Kolom:", lines[0] if lines else "(kosong)")
    elif cmd == "run":
        day = sys.argv[2]
        check_availability(day)
        print(fetch_day(day))
        print(build_silver(day))
    elif cmd == "inspect":
        import pandas as pd

        df = pd.read_parquet(io.BytesIO(lake.get_bytes(silver_key(sys.argv[2]))))
        print("bentuk:", df.shape)
        print(df.dtypes)
        print("null per kolom:\n", df.isna().sum())
        print("hotspot_id unik:", df["hotspot_id"].is_unique)
        print("confidence:\n", df["confidence"].value_counts())
        print(df.head(3).T)
    else:
        print("perintah: check | run YYYY-MM-DD | inspect YYYY-MM-DD")


if __name__ == "__main__":
    _cli()
