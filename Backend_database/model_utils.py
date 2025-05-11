from deepface import DeepFace
import numpy as np
from PIL import Image
import io
def get_embedding(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    embedding = DeepFace.represent(img_path=np.array(image), model_name="Facenet")[0]["embedding"]
    return embedding