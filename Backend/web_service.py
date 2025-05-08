from flask import Flask, request, jsonify
from model_service import predict
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/predict', methods=['POST'])
def handle_predict():
    if 'image' not in request.files:
        return jsonify({'error': "No image upload"}), 400
    
    image = request.files['image']
    filepath = os.path.join('uploads',image.filename)
    os.makedirs('uploads',exist_ok=True)
    image.save(filepath)

    result = predict(filepath)
    return jsonify({'result':result})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)