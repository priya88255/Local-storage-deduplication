from flask import Flask, request, jsonify
import hashlib
import os

app = Flask(__name__)

# Define the local folder path for storing files
UPLOAD_FOLDER = "C://Documents"  
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Chunk size for file reading (in bytes)
CHUNK_SIZE = 1024 * 1024  # 1MB chunks

@app.route('/')
def index():
    return app.send_static_file('dedup.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        
        # Chunk-based file hashing (SHA-256)
        file_hash = hashlib.sha256()
        while True:
            chunk = file.read(CHUNK_SIZE)
            if not chunk:
                break
            file_hash.update(chunk)
        
        file.seek(0)  # Reset file pointer to the beginning
        
        file_hash_hex = file_hash.hexdigest()
        
        # Define the file path based on its hash
        file_path = os.path.join(UPLOAD_FOLDER, file_hash_hex)
        
        # Check if the file already exists in the local folder
        if os.path.exists(file_path):
            return jsonify({'message': 'File already exists in the local storage'})
        else:
            # If the file doesn't exist, save it to the local folder
            file.save(file_path)
            return jsonify({'message': 'File uploaded successfully'})
    except Exception as ex:
        # Handle other errors
        return jsonify({'message': 'Error occurred while uploading file'}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
