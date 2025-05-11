from deepface import DeepFace
import numpy as np
import requests
# def predict(image_path):
#     check = DeepFace.find(img_path=image_path,db_path="/web_service/people")
#     if len(check[0]) > 0:
#         return True
#     return False
backend_db_url = "http://localhost:8000/get_embeddings"
def predict(image_path):
    # trích xuất embedding ảnh đầu vào
    embedding = DeepFace.represent(img_path= image_path, model_name="Facenet")[0]["embedding"]
    embedding = np.array(embedding)
    # lấy danh sách embeddings đã lưu
    try:
        response = requests.get(f"{backend_db_url}/get_embeddings")
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return {"status": "error", "message": f"Lỗi khi truy vấn dữ liệu: {e}"}
    
    # Tìm khoảng cách gần nhất
    min_distance = float('inf')
    best_match_face = "unknown"
    best_match_cv = "unknown"
    for item in data:
        stored_embedding = np.array(eval(item["embedding"]))
        distance = np.linalg.norm(embedding - stored_embedding)

        if distance < min_distance:
            min_distance = distance
            best_match_face = item["name"]
            best_match_cv = item["chuc_vu"]
            

    if min_distance < 0.6:
        return {"name": best_match_face, "chuc_vu": best_match_cv, "status": "Duoc phep vao"} 
    return {"status": "Khong duoc phep vao"}
