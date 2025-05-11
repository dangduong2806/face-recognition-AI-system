from fastapi import FastAPI, UploadFile, Form
from model_utils import get_embedding
from db_utils import save_embedding
import time
from supabase_client import supabase

app = FastAPI()

#Tải ảnh lên và lấy url
async def upload_image_to_supabase(image_bytes: bytes, file_name: str):
    # lưu tệp lên storage
    storage = supabase.storage()
    bucket_name = "area1"
    file_path = f"{file_name}.jpg"

    storage.from_(bucket_name).upload(file_path, image_bytes)
    public_url = storage.from_(bucket_name).get_public_url(file_path)
    return public_url['publicURL']

@app.post("/add_person")
async def add_person(name: str = Form(...), image: UploadFile = Form(...), chuc_vu: str = Form(...)):
    image_bytes = await image.read()
    embedding = get_embedding(image_bytes)
    # tải lên image_url
    file_name = f"{name}_{int(time.time())}"
    image_url = await upload_image_to_supabase(image_bytes, file_name)

    result = save_embedding(name, embedding, image_url, chuc_vu)
    return {"status": "Ok", "result": result.data}

@app.get("/get_embeddings")
def get_embeddings():
    try:
        response = supabase.table("people").select("*").execute()
        return response.data
    except Exception as e:
        return {"status": "error", "message": str(e)}