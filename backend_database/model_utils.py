from deepface import DeepFace
import numpy as np
from PIL import Image
import io
import cv2
import shutil
from pathlib import Path

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



def get_embedding(image_bytes):
    try:
        # Bước 1: Chuyển bytes -> ảnh RGB dạng numpy
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image_np = np.array(image)

        # Bước 2: Chuyển sang BGR (OpenCV cần BGR để detect_face)
        bgr_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # Bước 3: Dò khuôn mặt
        faces = detect_face(bgr_image)
        if not faces:
            print("❌ Không phát hiện khuôn mặt.")
            return None

        # Bước 4: Lấy khuôn mặt đầu tiên
        x, y, w, h, face_img = faces[0]
        # Bước 4.1: Resize khuôn mặt về kích thước 160x160
        face_img = cv2.resize(face_img, (160, 160))

        # Bước 4.2: Chuyển đổi khuôn mặt về định dạng mà DeepFace yêu cầu
        face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)

        # Bước 5: Trích xuất embedding từ khuôn mặt đã cắt
        result = DeepFace.represent(img_path=face_img, model_name="Facenet", enforce_detection=False)

        if result and isinstance(result, list) and "embedding" in result[0]:
            embedding = result[0]["embedding"]
            if np.all(np.isfinite(embedding)):  # kiểm tra không chứa NaN/inf
                return embedding

        print("❌ Không lấy được embedding hợp lệ.")
        return None

    except Exception as e:
        print(f"❌ Lỗi trong get_embedding: {e}")
        return None
