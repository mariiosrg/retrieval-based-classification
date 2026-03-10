# Project retrieval-based classification

Project ini mendemonstrasikan klasifikasi gambar sederhana berbasis embedding multimodal dan vector database. Gambar pada folder train diubah menjadi embedding menggunakan model CLIP, disimpan ke Qdrant, lalu gambar pada folder test diklasifikasikan dengan mencari embedding terdekat.

Pendekatan yang dipakai bukan training CNN dari nol. Repo ini menggunakan retrieval-based classification:

- embedding gambar dibuat dengan model `clip-ViT-B-32`
- embedding disimpan ke Qdrant
- label prediksi diambil dari tetangga terdekat dengan skor kemiripan tertinggi

Repo ini cocok untuk:

- demo image retrieval / image classification berbasis vector database
- eksperimen CLIP + Qdrant
- belajar alur ingestion dan inference tanpa training model sendiri

## Fitur

- Ingestion otomatis dari folder dataset per label
- Klasifikasi gambar dari folder test
- Penyimpanan embedding ke Qdrant Cloud
- Ringkasan akurasi dan waktu inferensi
- Struktur dataset sederhana dan mudah direplikasi

## Cara Kerja

Alur proyek:

1. Script [ingestion_qdrant.py](./ingestion_qdrant.py) membaca semua gambar di folder `train/`.
2. Nama subfolder dipakai sebagai label, misalnya `cats` dan `dogs`.
3. Setiap gambar diubah menjadi embedding 512 dimensi dengan model CLIP `clip-ViT-B-32`.
4. Embedding dan metadata gambar disimpan ke collection Qdrant bernama `image_classifier_rag`.
5. Script [prediction.py](./prediction.py) membaca gambar di folder `test/`.
6. Embedding gambar query dibandingkan ke data yang sudah diindeks di Qdrant.
7. Label dari hasil paling mirip dipakai sebagai prediksi akhir.

## Struktur Folder

```text
project_RAG_Klasifikasi_Gambar/
|- ingestion_qdrant.py
|- prediction.py
|- main.py
|- pyproject.toml
|- README.md
|- hasil_ingestion.md
|- hasil_prediksi.md
|- train/
|  |- cats/
|  \- dogs/
\- test/
	|- cats/
	\- dogs/
```

Dataset yang saat ini ada di repo:

- `train/cats`: 279 gambar
- `train/dogs`: 278 gambar
- `test/cats`: 70 gambar
- `test/dogs`: 70 gambar

## Kebutuhan

Sebelum menjalankan proyek, pastikan tersedia:

- Python 3.12 atau lebih baru
- akun Qdrant Cloud atau instance Qdrant yang bisa diakses
- file `.env` yang berisi kredensial Qdrant
- koneksi internet saat pertama kali model CLIP diunduh

Dependensi Python yang dipakai:

- `pillow`
- `python-dotenv`
- `qdrant-client`
- `sentence-transformers`

## Setup

### 1. Clone repo

```bash
git clone <url-repo-anda>
cd project_RAG_Klasifikasi_Gambar
```

### 2. Install dependency

Repo ini sudah memakai `pyproject.toml` dan `uv.lock`, jadi cara paling praktis adalah memakai `uv`.

Jika belum ada `uv`:

```bash
pip install uv
```

Lalu install dependency proyek:

```bash
uv sync
```

Alternatif tanpa `uv`:

```bash
pip install pillow python-dotenv qdrant-client sentence-transformers
```

Catatan: `sentence-transformers` akan menarik dependency PyTorch. Pada beberapa mesin, proses install pertama bisa cukup lama.

### 3. Buat file `.env`

Buat file `.env` di root project dengan isi:

```env
QDRANT_URL=https://xxxxxx.your-qdrant-host
QDRANT_API_KEY=your_qdrant_api_key
```

Penjelasan:

- `QDRANT_URL`: URL instance Qdrant Anda
- `QDRANT_API_KEY`: API key instance Qdrant Anda

Jika file `.env` tidak ada atau nilainya kosong, script akan gagal saat start.

## Menjalankan Proyek

### 1. Ingestion data train ke Qdrant

Jalankan:

```bash
uv run ingestion_qdrant.py
```

Atau jika tidak memakai `uv`:

```bash
python ingestion_qdrant.py
```

Yang dilakukan script ini:

- membuat collection `image_classifier_rag` jika belum ada
- membaca semua gambar pada folder `train/`
- membuat embedding per gambar
- menyimpan embedding dan metadata ke Qdrant

Contoh output:

```text
Collection 'image_classifier_rag' berhasil dibuat.

--- Memulai Ingestion ---
Memulai proses otomatis membaca folder: C:\...\train
Menyiapkan gambar: dog_92.jpg | Label: dogs
Berhasil mengunggah: C:\...\train\dogs\dog_92.jpg dengan label 'dogs'
Dokumentasi: Proses ingestion selesai dalam 216.79 detik.
```

### 2. Jalankan prediksi pada folder test

Jalankan:

```bash
uv run prediction.py
```

Atau:

```bash
python prediction.py
```

Yang dilakukan script ini:

- membaca semua gambar pada folder `test/`
- membuat embedding untuk tiap gambar test
- mencari tetangga terdekat di Qdrant
- menampilkan label prediksi, waktu prediksi, dan ringkasan akurasi

Contoh output ringkas:

```text
--- Memulai Prediksi Seluruh Data Test ---
Membaca folder: C:\...\test

Prediksi untuk C:\...\test\cats\cat_1.jpg: 'cats' (Skor Kemiripan: 0.9997)

=================================================================
Total gambar   : 140
Benar          : 139
Salah          : 1
Akurasi        : 99.29%
Total waktu    : 41.625 detik
Rata-rata/gambar: 0.297 detik
=================================================================
```

## Hasil Uji pada Repo Ini

Ringkasan hasil yang sudah terdokumentasi:

- ingestion terdokumentasi di [hasil_ingestion.md](./hasil_ingestion.md)
- prediksi terdokumentasi di [hasil_prediksi.md](./hasil_prediksi.md)

Hasil yang tercatat:

- total data train yang terdokumentasi saat ingestion: 200 gambar
- total data test: 140 gambar
- akurasi prediksi: 99.29%
- jumlah prediksi benar: 139 dari 140 gambar

Catatan penting: isi folder `train/` saat ini berjumlah 557 gambar, sedangkan file [hasil_ingestion.md](./hasil_ingestion.md) mencatat 200 gambar. Itu berarti dokumentasi hasil ingestion dibuat pada kondisi dataset sebelumnya atau subset data tertentu.

## Menambah Dataset Sendiri

Anda bisa mencoba dataset lain dengan format folder yang sama:

```text
train/
|- kelas_a/
|- kelas_b/
\- kelas_c/

test/
|- kelas_a/
|- kelas_b/
\- kelas_c/
```

Aturan penting:

- nama subfolder akan dijadikan label kelas
- file yang dibaca hanya berekstensi `.png`, `.jpg`, `.jpeg`, dan `.webp`
- jika dataset diubah, jalankan ulang ingestion sebelum prediksi

## Troubleshooting

### Error `QDRANT_URL atau QDRANT_API_KEY tidak ditemukan`

Penyebab:

- file `.env` belum dibuat
- nama variabel pada `.env` salah
- file `.env` dibuat bukan di root project

Solusi:

- pastikan file `.env` ada sejajar dengan `README.md`
- pastikan key yang dipakai tepat: `QDRANT_URL` dan `QDRANT_API_KEY`

### Prediksi gagal karena collection kosong

Penyebab:

- ingestion belum dijalankan
- collection pada Qdrant belum berisi data

Solusi:

- jalankan `uv run ingestion_qdrant.py` terlebih dahulu

### Install `sentence-transformers` lama atau gagal

Penyebab:

- dependency PyTorch cukup besar
- koneksi internet lambat atau konfigurasi environment belum sesuai

Solusi:

- gunakan virtual environment yang bersih
- ulangi install dengan koneksi yang stabil
- jika perlu, install PyTorch terlebih dahulu sesuai platform Anda

## Batasan Implementasi Saat Ini

- label diambil dari 1 nearest neighbor teratas (`top_k=1`)
- belum ada script evaluasi terpisah yang menyimpan hasil ke file CSV atau JSON
- belum ada dukungan upload gambar tunggal lewat CLI argument
- [main.py](./main.py) belum dipakai sebagai entry point utama

## File Penting

- [ingestion_qdrant.py](./ingestion_qdrant.py): ingestion embedding gambar ke Qdrant
- [prediction.py](./prediction.py): prediksi label gambar dari data test
- [pyproject.toml](./pyproject.toml): metadata proyek dan dependency
- [hasil_ingestion.md](./hasil_ingestion.md): dokumentasi hasil ingestion
- [hasil_prediksi.md](./hasil_prediksi.md): dokumentasi hasil prediksi

## Ringkasan Singkat untuk Mencoba

Jika ingin langsung mencoba, urutannya cukup ini:

```bash
uv sync
```

```env
QDRANT_URL=...
QDRANT_API_KEY=...
```

```bash
uv run ingestion_qdrant.py
uv run prediction.py
```

Setelah itu Anda akan melihat hasil klasifikasi gambar dari folder `test/` berdasarkan embedding yang sudah dimasukkan dari folder `train/`.
