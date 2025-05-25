
import cv2
import numpy as np
import requests
from deepface import DeepFace
from pathlib import Path
import shutil
from scipy.spatial.distance import cosine
from PIL import Image

backend_db_url = "http://data:8000"  


def ensure_facenet_model():
    project_models_dir = Path("models")
    project_model_path = project_models_dir / "facenet_weights.h5"
    cache_dir = Path.home() / ".deepface" / "weights"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_model_path = cache_dir / "facenet_weights.h5"
    
    # Kiểm tra xem file model có tồn tại trong thư mục dự án không
    if not project_model_path.exists():
        raise FileNotFoundError(f"Model file not found at {project_model_path}. Please download facenet_weights.h5 and place it in the models/ directory.")
    
    # Sao chép file model vào thư mục cache của DeepFace nếu chưa có
    if not cache_model_path.exists():
        shutil.copy(project_model_path, cache_model_path)
        print(f"Copied Facenet model to {cache_model_path}")
    else:
        print(f"Facenet model already exists at {cache_model_path}")
        
ensure_facenet_model()


def detect_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    face_regions = []
    for (x, y, w, h) in faces:
        face_regions.append((x, y, w, h, frame[y:y+h, x:x+w]))
    return face_regions



def get_face_embedding(face_img):
    try:
        
        face_img = cv2.resize(face_img, (160, 160))  # Resize to 160x160 for Facenet
        
        face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)

        # face_img = Image.fromarray(face_img)

        result = DeepFace.represent(img_path=face_img, model_name="Facenet", enforce_detection=False)
        if result and isinstance(result, list) and len(result) > 0:
            embedding = np.array(result[0]['embedding'])
            if np.all(np.isfinite(embedding)):  # Ensure embedding is valid
                return embedding
        print("Warning: Invalid or empty embedding returned by DeepFace")
    except Exception as e:
        print(f"Error in get_face_embedding: {e}")
    return None

def load_saved_embeddings():
    try:
        response = requests.get(f"{backend_db_url}/get_embeddings")
        response.raise_for_status()
        data = response.json()
        # Validate that each item has a valid embedding
        valid_data = [
            item for item in data
            if isinstance(item.get("embedding"), list) and item.get("name") and item.get("chuc_vu")
        ]
        return valid_data
    except Exception as e:
        print(f"Lỗi khi truy vấn dữ liệu: {e}")
        return []
    

def compare_embedding(embedding, saved_data, threshold=6.03):
    min_distance = float('inf')
    best_name = "unknown"
    best_cv = "unknown"

    for i, item in enumerate(saved_data):
        try:
            raw_emb = item["embedding"]

            # ✅ Không cần eval hay ast nếu là list
            if not isinstance(raw_emb, list):
                print(f"[{i}] ⚠️ embedding không phải list, bỏ qua")
                continue

            stored_embedding = np.array(raw_emb, dtype=np.float32)

            if stored_embedding.shape != embedding.shape:
                print(f"[{i}] ❌ Shape mismatch. Skip.")
                continue

            distance = np.linalg.norm(embedding - stored_embedding)
            # distance = cosine(embedding, stored_embedding)

            if not np.isfinite(distance):
                print(f"[{i}] ❌ Distance NaN/Inf → Bỏ qua")
                continue

            if distance < min_distance:
                min_distance = distance
                best_name = item["name"]
                best_cv = item["chuc_vu"]

        except Exception as e:
            print(f"[{i}] ❌ Lỗi xử lý embedding: {e}")
            continue

    if min_distance < threshold:
        return best_name, best_cv, min_distance
    return "unknown", "unknown", min_distance

def draw_face_info(frame, x, y, w, h, name, chuc_vu, color=(0,255,0)):
    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
    label = f"{name} ({chuc_vu})" if name != "unknown" else "Khong duoc phep vao"
    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
