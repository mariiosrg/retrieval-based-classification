# Dokumentasi Ingestion Gambar

## Ringkasan
- **Total gambar**: 200
- **Label**: cats, dogs
- **Total waktu**: 216.79 detik
- **Rata-rata/gambar**: 1.08 detik

## Tabel Ingestion
| File         | Label | Status |
|-------------|-------|--------|
| dog_92.jpg  | dogs  | Uploaded |
| dog_93.jpg  | dogs  | Uploaded |
| dog_97.jpg  | dogs  | Uploaded |
| dog_98.jpg  | dogs  | Uploaded |
| dog_99.jpg  | dogs  | Uploaded |
| ...         | ...   | ...      |

_(Tabel dipotong, lihat output terminal untuk detail lengkap)_

## Catatan
- Semua gambar berhasil diunggah ke Qdrant.
- Proses ingestion berjalan lancar.
- Rata-rata waktu ingestion per gambar dapat digunakan untuk estimasi batch berikutnya.

## Cara Reproduksi
Jalankan:
```bash
uv run ingestion_qdrant.py
```
Pastikan folder `train/` berisi subfolder `cats/` dan `dogs/` dengan gambar.

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
Menyiapkan gambar: dog_92.jpg | Label: dogs
Berhasil mengunggah: /mnt/c/Users/mario/agentic_ai/project_RAG_Klasifikasi_Gambar/train/dogs/dog_92.jpg dengan label 'dogs'
...
Dokumentasi: Proses ingestion selesai dalam 216.79 detik.
```
