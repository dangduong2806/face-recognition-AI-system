from fastapi import FastAPI, UploadFile, Form, HTTPException
from model_utils import get_embedding
from db_utils import save_embedding
import time
from supabase_client import supabase
from fastapi.middleware.cors import CORSMiddleware

import logging
import mimetypes
import re
from unidecode import unidecode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
# Cho phép mọi domain/port truy cập (demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép mọi origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Tải ảnh lên và lấy URL
def upload_image_to_supabase(image_bytes: bytes, file_name: str):
    bucket_name = "area1"
    file_path = f"{file_name}.jpg"
    storage = supabase.storage

    upload_response = storage.from_(bucket_name).upload(file_path, image_bytes)
    if isinstance(upload_response, dict) and 'error' in upload_response:
        raise Exception(f"Failed to upload image: {upload_response['error']}")

    public_url = storage.from_(bucket_name).get_public_url(file_path)
    return public_url  # Đây là chuỗi string

def convert_vietnamese_to_ascii(text):
    # Dùng unidecode để chuyển toàn bộ chuỗi có dấu thành không dấu (kể cả đ)
    text = unidecode(text)

    
    # Đổi về chữ thường, thay dấu cách bằng gạch dưới
    text = text.lower()
    text = re.sub(r'\s+', '_', text)

    # Chỉ giữ ký tự chữ, số, _, ., -
    text = re.sub(r'[^a-z0-9_\.-]', '', text)

    return text

@app.post("/add_person")
async def add_person(
    name: str = Form(...),
    image: UploadFile = Form(...),
    chuc_vu: str = Form(...)
):
    image_bytes = await image.read()
    embedding = get_embedding(image_bytes)
    if not embedding:
        raise HTTPException(status_code=422, detail="Ảnh bị quá nghiêng hoặc không có khuôn mặt, hãy thử lại với ảnh khác.")
    # Tải lên Supabase và lấy URL
    name2 = convert_vietnamese_to_ascii(name)
    file_name = f"{name2}_{int(time.time())}"
    image_url = upload_image_to_supabase(image_bytes, file_name)
    

    result = save_embedding(name, embedding, image_url, chuc_vu)
    return {"status": "Ok", "result": result.data}  

@app.get("/get_embeddings")
def get_embeddings():
    try:
        response = supabase.table("people").select("*").execute()
        return response.data
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
@app.get("/get_people")
async def get_people():
    try:
        result = supabase.table("people").select("*").execute()
        return {"status": "Ok", "data": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch people: {str(e)}")
    
@app.delete("/delete_person/{person_id}")
async def delete_person(person_id: int):
    try:
        result = supabase.table("people").delete().eq("id", person_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Person not found")
        return {"status": "Ok", "message": "Person deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete person: {str(e)}")
    
@app.put("/update_person/{person_id}")
async def update_person(
    person_id: int,
    name: str = Form(...),
    image: UploadFile = Form(None),  # Không bắt buộc
    chuc_vu: str = Form(...)
):
    logger.info(f"Received request to update person: id={person_id}, name={name}, chuc_vu={chuc_vu}")
    try:
        data = {
            "name": name,
            "chuc_vu": chuc_vu
        }
        if image:
            image_bytes = await image.read()
            if not image_bytes:
                raise HTTPException(status_code=422, detail="Image file is empty")
            content_type = image.content_type
            if content_type not in ["image/jpeg", "image/png"]:
                raise HTTPException(status_code=422, detail="Only JPEG or PNG images are supported")
            embedding = get_embedding(image_bytes)
            name2 = convert_vietnamese_to_ascii(name)
            file_name = f"{name2}_{int(time.time())}"
            image_url = upload_image_to_supabase(image_bytes, file_name)
            data["embedding"] = embedding
            data["image_url"] = image_url

        result = supabase.table("people").update(data).eq("id", person_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Person not found")
        logger.info(f"Person updated successfully: {name}")
        return {"status": "Ok", "result": result.data}
    except Exception as e:
        logger.error(f"Error updating person: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update person: {str(e)}")