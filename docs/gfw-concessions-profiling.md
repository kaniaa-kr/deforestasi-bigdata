# Profiling & Data Dictionary: GFW Concessions

## 1. Sumber Data & Tata Kelola (Lembar Etika)
* **Penyedia Data:** Global Forest Watch (GFW) Open Data Portal (`data.globalforestwatch.org`)
* **Tanggal Unduh:** 27 November 2026 *(sesuaikan jika diunduh di tanggal berbeda)*
* **Lisensi:** Creative Commons Attribution 4.0 International (CC BY 4.0) *(verifikasi di halaman metadata GFW)*
* **Skema Target Database:** `gfw` pada Supabase PostGIS (`EPSG:4326`)

---

## 2. Dataset 1: Indonesia Wood Fiber Concessions
* **Nama File Sumber:** `Indonesia_wood_fiber_concessions.shp`
* **Tabel Target:** `gfw.wood_fiber_concessions`
* **Jumlah Fitur:** 539 poligon
* **Tipe Geometri Asli:** `3D Multi Polygon (MULTIPOLYGONZ)` -> dinormalisasi ke `MULTIPOLYGON`
* **CRS Asli:** `WGS 84 / Pseudo-Mercator` (`EPSG:3857`) -> ditransformasi ke `WGS 84` (`EPSG:4326`)
* **Validitas Geometri:**
  * Setelah impor (`-makevalid`): `0` geometri invalid (539 valid)
  * *(Catatan pengecekan sebelum `-makevalid` dapat dijalankan lewat `ogrinfo -dialect SQLite -sql "SELECT COUNT(*) FROM Indonesia_wood_fiber_concessions WHERE ST_IsValid(geometry)=0"` jika diperlukan)*

### Data Dictionary (`gfw.wood_fiber_concessions`)
| Nama Kolom | Tipe Data (PostGIS) | Keterangan |
| :--- | :--- | :--- |
| `gid` | `integer` | Primary key hasil generate `ogr2ogr` |
| `objectid_1` | `integer` | ID objek internal sumber |
| `objectid` | `integer` | ID objek sekunder sumber |
| `group_comp` | `character varying` | Nama grup perusahaan induk |
| `name` | `character varying` | Nama pemegang izin konsesi |
| `type` | `character varying` | Kode tipe konsesi bawaan GFW |
| `country` | `character varying` | Kode negara (`IDN`) |
| `area_ha` | `integer` | Luas area konsesi dalam hektar (atribut sumber) |
| `source` | `character varying` | Instansi/dokumen sumber peta asal |
| `last_updat` | `character varying` | Tahun/waktu pembaruan terakhir data |
| `gfwid` | `character varying` | Pengenal unik global milik GFW |
| `globalid` | `character varying` | UUID global ESRI |
| `shape_leng` | `double precision` | Panjang keliling poligon dalam satuan CRS asli (`EPSG:3857`) |
| `shape_area` | `double precision` | Luas poligon dalam satuan CRS asli (`EPSG:3857`) |
| `geom` | `geometry(MultiPolygon, 4326)` | Geometri poligon utama dalam koordinat `EPSG:4326` |
