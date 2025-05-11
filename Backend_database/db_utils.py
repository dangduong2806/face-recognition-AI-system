from supabase_client import supabase
import json

def save_embedding(name, embedding, image_url= None, chuc_vu= None):
    data = {
        "name": name,
        "embedding": embedding,
        "image_url": image_url,
        "chuc_vu": chuc_vu
    }
    result = supabase.table("people").insert(data).execute()
    return result