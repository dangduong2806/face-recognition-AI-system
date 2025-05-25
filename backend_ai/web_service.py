# web_service.py

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
import numpy as np
import cv2
from model_service import detect_face, get_face_embedding, load_saved_embeddings, compare_embedding
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
from sklearn.cluster import DBSCAN
from collections import deque

app = FastAPI()
# Cho phép mọi domain/port truy cập (demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép mọi origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Định nghĩa model cho dữ liệu nhận từ frontend
class ImageData(BaseModel):
    image_data: str  # Tham số nhận ảnh dạng base64

def encode_image_to_base64(image):
    _, buffer = cv2.imencode('.jpg', image)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{img_base64}"

@app.post("/predict")
async def predict(data: ImageData):
    # Tách header 'data:image/jpeg;base64,...' nếu có
    base64_str = data.image_data.split(',')[1] if ',' in data.image_data else data.image_data
    img_bytes = base64.b64decode(base64_str)
    nparr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Tiến hành nhận diện khuôn mặt (sử dụng các hàm bạn đã có sẵn)
    faces = detect_face(frame)
    saved_data = load_saved_embeddings()

    results = []
    for (x, y, w, h, face_img) in faces:
        embedding = get_face_embedding(face_img)
        if embedding is not None:
            name, chuc_vu, dist = compare_embedding(embedding, saved_data)

            # Convert distance to a regular float and handle invalid values
            # dist = float(dist) if np.isfinite(dist) else float('inf')
            dist = float(dist)
            if not np.isfinite(dist):  # fix lỗi JSON không chấp nhận NaN, inf
                dist = 9999.0
                
            results.append({
                "name": name,
                "chuc_vu": chuc_vu,
                "distance": dist,
                "status": "Duoc phep vao" if dist < 6.03 else "Khong duoc phep vao",
                "bounding_box": {"x": int(x), "y": int(y), "w": int(w), "h": int(h)}  # Thêm tọa độ bounding box
            })

    
    if not results:
        results.append({
            "name": "Không xác định",
            "chuc_vu": "",
            "distance": 9999.0,
            "status": "Khong duoc phep vao",
            "bounding_box": None #thêm thông tin bounding box nếu cần
        })
    return JSONResponse(content={"results": results})
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7000)
