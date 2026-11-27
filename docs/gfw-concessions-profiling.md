# Profiling & Data Dictionary: GFW Concessions

## 1. Sumber Data & Tata Kelola (Lembar Etika)

- **Penyedia Data:** Global Forest Watch (GFW) Open Data Portal (`data.globalforestwatch.org`)
- **Tanggal Unduh:** 27 November 2026
- **Lisensi:** Creative Commons Attribution 4.0 International (CC BY 4.0) _(verifikasi di halaman metadata GFW)_
- **Skema Target Database:** `gfw` pada Supabase PostGIS (`EPSG:4326`)
- **Ringkasan Total Fitur:** `2.941` poligon konsesi di Indonesia (`539` Wood Fiber + `1.845` Oil Palm + `557` Logging)

---

## 2. Dataset 1: Indonesia Wood Fiber Concessions

- **Nama File Sumber:** `Indonesia_wood_fiber_concessions.shp`
- **Tabel Target:** `gfw.wood_fiber_concessions`
- **Jumlah Fitur:** `539` poligon
- **Tipe Geometri Asli:** `3D Multi Polygon (MULTIPOLYGONZ)` $\rightarrow$ dinormalisasi ke `MULTIPOLYGON`
- **CRS Asli:** `WGS 84 / Pseudo-Mercator` (`EPSG:3857`) $\rightarrow$ ditransformasi ke `WGS 84` (`EPSG:4326`)
- **Validitas Geometri:** `0` geometri invalid setelah impor (`-makevalid`), `539` valid, SRID `4326`

### Data Dictionary (`gfw.wood_fiber_concessions`)

| Nama Kolom   | Tipe Data (PostGIS)            | Keterangan                                                   |
| :----------- | :----------------------------- | :----------------------------------------------------------- |
| `gid`        | `integer`                      | Primary key hasil generate `ogr2ogr`                         |
| `objectid_1` | `integer`                      | ID objek internal sumber                                     |
| `objectid`   | `integer`                      | ID objek sekunder sumber                                     |
| `group_comp` | `character varying`            | Nama grup perusahaan induk                                   |
| `name`       | `character varying`            | Nama pemegang izin konsesi                                   |
| `type`       | `character varying`            | Kode tipe konsesi bawaan GFW                                 |
| `country`    | `character varying`            | Kode negara (`IDN`)                                          |
| `area_ha`    | `integer`                      | Luas area konsesi dalam hektar (atribut sumber)              |
| `source`     | `character varying`            | Instansi/dokumen sumber peta asal                            |
| `last_updat` | `character varying`            | Tahun/waktu pembaruan terakhir data                          |
| `gfwid`      | `character varying`            | Pengenal unik global milik GFW                               |
| `globalid`   | `character varying`            | UUID global ESRI                                             |
| `shape_leng` | `double precision`             | Panjang keliling poligon dalam satuan CRS asli (`EPSG:3857`) |
| `shape_area` | `double precision`             | Luas poligon dalam satuan CRS asli (`EPSG:3857`)             |
| `geom`       | `geometry(MultiPolygon, 4326)` | Geometri poligon utama dalam koordinat `EPSG:4326`           |

---

## 3. Dataset 2: Indonesia Oil Palm Concessions

- **Nama File Sumber:** `Indonesia_oil_palm_concessions.shp`
- **Tabel Target:** `gfw.oil_palm_concessions`
- **Jumlah Fitur:** `1.845` poligon
- **Tipe Geometri Asli:** `3D Multi Polygon (MULTIPOLYGONZ)` $\rightarrow$ dinormalisasi ke `MULTIPOLYGON`
- **CRS Asli:** `WGS 84` (`EPSG:4326`)
- **Validitas Geometri:** `0` geometri invalid setelah impor (`-makevalid`), `1.845` valid, SRID `4326`

### Data Dictionary (`gfw.oil_palm_concessions`)

| Nama Kolom   | Tipe Data (PostGIS)            | Keterangan                                         |
| :----------- | :----------------------------- | :------------------------------------------------- |
| `gid`        | `integer`                      | Primary key hasil generate `ogr2ogr`               |
| `objectid_1` | `integer`                      | ID objek internal sumber                           |
| `objectid`   | `integer`                      | ID objek sekunder sumber                           |
| `po_legalst` | `character varying`            | Status legalitas izin perkebunan kelapa sawit      |
| `po_legal_1` | `character varying`            | Keterangan tambahan status legalitas               |
| `po_hgu`     | `character varying`            | Nomor/informasi Hak Guna Usaha (HGU)               |
| `po_area_hg` | `double precision`             | Luas area HGU dalam hektar                         |
| `subgroup`   | `character varying`            | Sub-kelompok grup perusahaan                       |
| `groupid`    | `integer`                      | ID grup perusahaan                                 |
| `source`     | `character varying`            | Instansi/dokumen sumber peta asal                  |
| `zsl`        | `integer`                      | Indikator pelaporan/cakupan ZSL SPOTT              |
| `group_comp` | `character varying`            | Nama grup perusahaan induk                         |
| `shape_leng` | `double precision`             | Panjang keliling poligon (atribut sumber)          |
| `type`       | `character varying`            | Tipe konsesi (`Oil palm`)                          |
| `area_ha`    | `integer`                      | Luas area konsesi dalam hektar (atribut sumber)    |
| `country`    | `character varying`            | Kode negara (`IDN`)                                |
| `company`    | `character varying`            | Nama perusahaan operasional pemegang izin          |
| `name`       | `character varying`            | Nama unit/area konsesi                             |
| `gfwid`      | `character varying`            | Pengenal unik global milik GFW                     |
| `globalid`   | `character varying`            | UUID global ESRI                                   |
| `shape_le_1` | `double precision`             | Panjang keliling poligon sekunder                  |
| `shape_area` | `double precision`             | Luas poligon dalam derajat persegi                 |
| `geom`       | `geometry(MultiPolygon, 4326)` | Geometri poligon utama dalam koordinat `EPSG:4326` |

---

## 4. Dataset 3: Indonesia Managed Forest / Logging Concessions

- **Nama File Sumber:** `gfw_logging_download_v2020.shp` _(dataset global `Managed Forest Concessions`, disaring via `-where "country = 'IDN'"`)_
- **Tabel Target:** `gfw.logging_concessions`
- **Jumlah Fitur:** `557` poligon Indonesia _(disaring dari `30.381` fitur global)_
- **Tipe Geometri Asli:** `Multi Polygon (MULTIPOLYGON)`
- **CRS Asli:** `WGS 84` (`EPSG:4326`)
- **Validitas Geometri:** `0` geometri invalid setelah impor (`-makevalid`), `557` valid, SRID `4326`

### Data Dictionary (`gfw.logging_concessions`)

| Nama Kolom   | Tipe Data (PostGIS)            | Keterangan                                         |
| :----------- | :----------------------------- | :------------------------------------------------- |
| `gid`        | `integer`                      | Primary key hasil generate `ogr2ogr`               |
| `gfw_fid`    | `integer`                      | Feature ID internal GFW                            |
| `objectid_1` | `bigint`                       | ID objek internal sumber (tahap 1)                 |
| `objectid_2` | `bigint`                       | ID objek internal sumber (tahap 2)                 |
| `objectid`   | `bigint`                       | ID objek utama sumber                              |
| `country`    | `character varying`            | Kode negara ISO-3 (`IDN`)                          |
| `name`       | `character varying`            | Nama unit/area konsesi HPH                         |
| `company`    | `character varying`            | Nama perusahaan pemegang izin                      |
| `group_comp` | `character varying`            | Nama grup perusahaan induk                         |
| `group_coun` | `character varying`            | Negara asal grup perusahaan                        |
| `legal_term` | `character varying`            | Istilah/jenis perizinan kehutanan                  |
| `status`     | `character varying`            | Status aktif/izin konsesi                          |
| `province`   | `character varying`            | Nama provinsi lokasi konsesi                       |
| `area_ha`    | `character varying`            | Luas area konsesi dalam format teks dari sumber    |
| `source`     | `character varying`            | Instansi/dokumen sumber peta asal                  |
| `last_updat` | `character varying`            | Tahun/waktu pembaruan terakhir data                |
| `shape_leng` | `double precision`             | Panjang keliling poligon (atribut sumber)          |
| `gfwid`      | `character varying`            | Pengenal unik global milik GFW                     |
| `shape_le_1` | `double precision`             | Panjang keliling poligon sekunder 1                |
| `shape_le_2` | `double precision`             | Panjang keliling poligon sekunder 2                |
| `shape_le_3` | `double precision`             | Panjang keliling poligon sekunder 3                |
| `shape_area` | `double precision`             | Luas poligon dalam derajat persegi                 |
| `gfw_area__` | `double precision`             | Luas area kalkulasi GFW dalam hektar (numerik)     |
| `gfw_geosto` | `character varying`            | Hash geostore GFW                                  |
| `geom`       | `geometry(MultiPolygon, 4326)` | Geometri poligon utama dalam koordinat `EPSG:4326` |

---

## 5. View Gabungan & Tata Kelola Akses (`gfw.concession`)

Ketiga tabel master di atas disatukan dalam satu database view `gfw.concession` untuk mempermudah _spatial join_ pada Apache Spark + Sedona. Pada lapisan `logging`, kolom teks `area_ha` dikonversi menjadi `double precision` dengan fallback ke `gfw_area__` jika kosong.

### Data Dictionary (`gfw.concession`)

| Nama Kolom        | Tipe Data (PostGIS)            | Keterangan                                                  |
| :---------------- | :----------------------------- | :---------------------------------------------------------- |
| `concession_type` | `text`                         | Kategori konsesi (`wood_fiber`, `oil_palm`, atau `logging`) |
| `gid`             | `integer`                      | Primary key baris dari tabel asal                           |
| `gfwid`           | `character varying`            | Pengenal unik global milik GFW                              |
| `name`            | `character varying`            | Nama unit/area konsesi                                      |
| `group_comp`      | `character varying`            | Nama grup perusahaan induk                                  |
| `area_ha`         | `double precision`             | Luas area konsesi dalam satuan hektar                       |
| `geom`            | `geometry(MultiPolygon, 4326)` | Geometri poligon valid dalam koordinat `EPSG:4326`          |

### Definisi SQL View & Hak Akses

```sql
create or replace view gfw.concession as
select
  'wood_fiber'::text as concession_type,
  gid, gfwid, name, group_comp,
  area_ha::double precision as area_ha,
  geom
from gfw.wood_fiber_concessions
union all
select
  'oil_palm'::text as concession_type,
  gid, gfwid, name, group_comp,
  area_ha::double precision as area_ha,
  geom
from gfw.oil_palm_concessions
union all
select
  'logging'::text as concession_type,
  gid, gfwid, name, group_comp,
  coalesce(nullif(trim(area_ha), '')::double precision, gfw_area__) as area_ha,
  geom
from gfw.logging_concessions;

grant select on all tables in schema gfw to spark_reader, etl_writer;
```
