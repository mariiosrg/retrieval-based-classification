# Hasil Prediksi Klasifikasi Gambar

## Ringkasan
- **Total gambar**: 140
- **Benar**: 139
- **Salah**: 1
- **Akurasi**: 99.29%
- **Total waktu**: 41.625 detik
- **Rata-rata/gambar**: 0.297 detik

## Tabel Hasil
| File         | True Label | Predicted Label | Time (s) | Status |
|-------------|------------|-----------------|----------|--------|
| cat_1.jpg   | cats       | cats            | 0.869    | OK     |
| cat_106.jpg | cats       | cats            | 0.287    | OK     |
| cat_109.jpg | cats       | cats            | 0.279    | OK     |
| cat_113.jpg | cats       | cats            | 0.287    | OK     |
| cat_114.jpg | cats       | cats            | 0.284    | OK     |
| cat_116.jpg | cats       | dogs            | 0.273    | MISS   |
| cat_118.jpg | cats       | cats            | 0.273    | OK     |
| cat_119.jpg | cats       | cats            | 0.284    | OK     |
| cat_124.jpg | cats       | cats            | 0.279    | OK     |
| cat_140.jpg | cats       | cats            | 0.313    | OK     |
| ...         | ...        | ...             | ...      | ...    |

_(Tabel dipotong, lihat output terminal untuk detail lengkap)_

## Catatan
- Satu gambar salah prediksi: `cat_116.jpg` (seharusnya cats, diprediksi dogs)
- Model CLIP + Qdrant sangat cepat dan akurat untuk dataset ini.
- Rata-rata waktu prediksi per gambar < 0.3 detik.

## Cara Reproduksi
Jalankan:
```bash
uv run prediction.py
```
Pastikan folder `test/` berisi subfolder `cats/` dan `dogs/` dengan gambar.

## Dokumentasi Laptop
- Seluruh proses hanya menggunakan CPU (tanpa GPU)
- **Device name**: marioexpertbook
- **Model**: ASUS EXPERTBOOK PM1403CDA
- **Processor**: AMD Ryzen 5 7535HS with Radeon Graphics (3.30 GHz)
- **Installed RAM**: 24.0 GB
- **Graphics Card**: AMD Radeon(TM) Graphics (483 MB)
- **Storage**: 954 GB (730 GB used)
- **OS**: Windows 11 Home Single Language 64-bit (Version 25H2, Build 26200.7922)

## Contoh Output Terminal
```
...output terminal seperti di atas...
```
https://arxiv.org/pdf/2412.11663 