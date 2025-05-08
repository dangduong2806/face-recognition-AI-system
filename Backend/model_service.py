from deepface import DeepFace
def predict(image_path):
    check = DeepFace.find(img_path=image_path,db_path="/web_service/people")
    if len(check[0]) > 0:
        return True
    return False