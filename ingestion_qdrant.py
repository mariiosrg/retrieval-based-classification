import uuid
import os
import time  # Untuk dokumentasi waktu proses
from dotenv import load_dotenv # Tambahkan import ini
from PIL import Image
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer


# Muat variabel environment dari file .env
load_dotenv()
# ==========================================
# 1. INISIALISASI MODEL & QDRANT CLIENT
# ==========================================
# Menggunakan CLIP untuk mengekstrak dense embedding dari gambar
model = SentenceTransformer('clip-ViT-B-32')

# Ambil URL dan API Key dari environment variables
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

# Validasi sederhana untuk memastikan .env terbaca
if not qdrant_url or not qdrant_api_key:
    raise ValueError("QDRANT_URL atau QDRANT_API_KEY tidak ditemukan. Pastikan file .env sudah diatur dengan benar.")

# Inisialisasi client mengarah ke Qdrant Cloud
client = QdrantClient(
    url=qdrant_url, 
    api_key=qdrant_api_key
)
COLLECTION_NAME = "image_classifier_rag"

# ==========================================
# 2. MEMBUAT COLLECTION DI QDRANT
# ==========================================
def setup_collection():
    # Dimensi output dari model CLIP-ViT-B-32 adalah 512
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=512, distance=Distance.COSINE)
        )
        print(f"Collection '{COLLECTION_NAME}' berhasil dibuat.")
    else:
        print(f"Collection '{COLLECTION_NAME}' sudah ada.")

# ==========================================
# 3. PROSES INGESTION (MEMASUKKAN DATA)
# ==========================================
def index_image(image_path: str, label: str):
    try:
        # Buka gambar dan ubah menjadi vektor embedding
        img = Image.open(image_path)
        vector = model.encode(img).tolist() # Qdrant membutuhkan format list
        
        # Buat point struct (ID unik, vektor, dan payload/metadata)
        point = PointStruct(
            id=str(uuid.uuid4()), 
            vector=vector, 
            payload={"label": label, "file_name": os.path.basename(image_path)}
        )
        
        # Upsert ke Qdrant
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=[point]
        )
        print(f"Berhasil mengunggah: {image_path} dengan label '{label}'")
    except Exception as e:
        print(f"Gagal memproses {image_path}: {e}")


import os

# ==========================================
# FUNGSI UNTUK INGESTION DARI FOLDER
# ==========================================
def ingest_from_directory(base_directory: str):
    """
    Membaca semua gambar dari sub-folder, menjadikan nama sub-folder sebagai label,
    lalu mengirimkannya ke Qdrant.
    """
    # Mengecek semua item di dalam folder utama (dataset_gambar)
    for folder_name in os.listdir(base_directory):
        folder_path = os.path.join(base_directory, folder_name)
        
        # Pastikan yang dibaca adalah sebuah folder (bukan file nyasar)
        if os.path.isdir(folder_path):
            label = folder_name  # <-- NAMA FOLDER OTOMATIS MENJADI LABEL
            
            # Cek setiap file di dalam folder label tersebut
            for file_name in os.listdir(folder_path):
                # Filter hanya file gambar berdasarkan ekstensinya
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    image_path = os.path.join(folder_path, file_name)
                    
                    print(f"Menyiapkan gambar: {file_name} | Label: {label}")
                    
                    # Panggil fungsi index_image dari kode sebelumnya
                    index_image(image_path, label) # Hilangkan tanda pagar (#) untuk menjalankan

# ==========================================
# 5. SIMULASI PENGGUNAAN
# ==========================================
if __name__ == "__main__":
    setup_collection()

    print("\n--- Memulai Ingestion ---")

    # Path folder train relatif terhadap lokasi script ini
    folder_utama = os.path.join(os.path.dirname(os.path.abspath(__file__)), "train")

    print(f"Memulai proses otomatis membaca folder: {folder_utama}")

    start_time = time.time()
    ingest_from_directory(folder_utama)
    end_time = time.time()
    duration = end_time - start_time
    print(f"\nDokumentasi: Proses ingestion selesai dalam {duration:.2f} detik.")