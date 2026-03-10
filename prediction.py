import uuid
import os
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
# PROSES INFERENCE (KLASIFIKASI)
# ==========================================

def predict_image(image_path: str, top_k: int = 1):
    try:
        # Ekstrak embedding dari gambar baru
        img = Image.open(image_path)
        query_vector = model.encode(img).tolist()
        
        # Cari vektor terdekat di Qdrant (API qdrant-client >= 1.7)
        search_result = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=top_k
        )

        if not search_result.points:
            return "Tidak ada data referensi di database."

        # Mengambil label dari hasil yang paling mirip (teratas)
        best_match = search_result.points[0]
        predicted_label = best_match.payload.get("label")
        score = best_match.score
        
        print(f"Prediksi untuk {image_path}: '{predicted_label}' (Skor Kemiripan: {score:.4f})")
        return predicted_label
        
    except Exception as e:
        print(f"Gagal memprediksi {image_path}: {e}")

def predict_all_from_directory(base_directory: str):
    """
    Memprediksikan SEMUA gambar dari sub-folder di dalam base_directory.
    Nama sub-folder dianggap sebagai label ground truth.
    Menampilkan waktu prediksi per gambar, total waktu, dan akurasi keseluruhan.
    """
    import time

    results = []  # Menyimpan (file_path, true_label, predicted_label, elapsed_time)

    # Iterasi tiap sub-folder (label)
    for folder_name in sorted(os.listdir(base_directory)):
        folder_path = os.path.join(base_directory, folder_name)
        if not os.path.isdir(folder_path):
            continue
        true_label = folder_name

        for file_name in sorted(os.listdir(folder_path)):
            if not file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                continue
            image_path = os.path.join(folder_path, file_name)

            start = time.perf_counter()
            predicted_label = predict_image(image_path)
            elapsed = time.perf_counter() - start

            results.append({
                "file":      file_name,
                "true":      true_label,
                "predicted": predicted_label,
                "time_s":    elapsed,
            })

    # ── Ringkasan ─────────────────────────────────────────────────────────────
    if not results:
        print("Tidak ada gambar yang ditemukan di folder test.")
        return

    total_images  = len(results)
    correct       = sum(1 for r in results if r["predicted"] == r["true"])
    accuracy      = correct / total_images * 100
    total_time    = sum(r["time_s"] for r in results)
    avg_time      = total_time / total_images

    print("\n" + "=" * 65)
    print(f"{'FILE':<35} {'TRUE':<10} {'PRED':<10} {'TIME (s)':>8}")
    print("-" * 65)
    for r in results:
        match_mark = "OK" if r["predicted"] == r["true"] else "MISS"
        print(f"{r['file']:<35} {r['true']:<10} {str(r['predicted']):<10} {r['time_s']:>8.3f}  {match_mark}")
    print("=" * 65)
    print(f"Total gambar   : {total_images}")
    print(f"Benar          : {correct}")
    print(f"Salah          : {total_images - correct}")
    print(f"Akurasi        : {accuracy:.2f}%")
    print(f"Total waktu    : {total_time:.3f} detik")
    print(f"Rata-rata/gambar: {avg_time:.3f} detik")
    print("=" * 65)


if __name__ == "__main__":
    print("\n--- Memulai Prediksi Seluruh Data Test ---")
    test_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test")
    print(f"Membaca folder: {test_folder}\n")
    predict_all_from_directory(test_folder)