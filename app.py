from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Ensure the uploads folder exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------- ROUTES ---------- #

@app.route('/')
def home():
    return render_template('index.html')

# 🧠 Day 2 - Text-to-Speech using Murf AI
import requests
MURF_API_KEY = "YOUR_API_KEY_HERE"
MURF_API_URL = "https://api.murf.ai/v1/speech/generate"

@app.route("/generate-audio", methods=["POST"])
def generate_audio():
    try:
        data = request.get_json(force=True)
        text = data.get("text")
        if not text:
            return jsonify({"error": "Text is required"}), 400

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "api-key": MURF_API_KEY
        }

        payload = {
            "voiceId": "en-UK-hazel",
            "text": text
        }

        response = requests.post(MURF_API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            audio_url = response.json().get("audioFile")
            return jsonify({"audio_url": audio_url})
        else:
            return jsonify({"error": "Murf API error", "details": response.json()}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🎤 Day 5 - Upload Echo Bot Audio
@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    file_size = os.path.getsize(file_path)
    content_type = file.content_type

    return jsonify({
        "filename": filename,
        "content_type": content_type,
        "size": file_size
    })

# ---------- END ---------- #

if __name__ == '__main__':
    app.run(debug=True)
