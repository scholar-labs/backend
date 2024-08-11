# from flask import Flask
# from flask import request
# from PyPDF2 import PdfReader

# app = Flask(__name__)

# # here's how you can create a route
# @app.route('/test')
# def say_hello():   
#     return ('hello')


# # route to extract text from pdf
# @app.route('/extract-text', methods=['POST'])
# def extract_text_from_pdf():
#     uploaded_pdf_file = request.files['file'] # name in request would have to be 'file'.
#     reader = PdfReader(uploaded_pdf_file)
#     number_of_pages = len(reader.pages)
#     text = ''
#     for i in range(number_of_pages):
#         page = reader.pages[i]
#         text = text + page.extract_text()
#     return text


# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
import requests
from PyPDF2 import PdfReader

app = Flask(__name__)

# Route to test the server
@app.route('/test')
def say_hello():
    return 'hello'

# Route to extract text from PDF
@app.route('/extract-text', methods=['POST'])
def extract_text_from_pdf():
    uploaded_pdf_file = request.files['file']  # name in request must be 'file'
    reader = PdfReader(uploaded_pdf_file)
    number_of_pages = len(reader.pages)
    text = ''
    for i in range(number_of_pages):
        page = reader.pages[i]
        text += page.extract_text()
    return text

# Route to extract text from audio
@app.route('/audio-to-text', methods=['POST'])
def audio_to_text():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    
    audio_file = request.files['audio']

    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    headers = {"Authorization": "Bearer hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}  # replace with your API key

    files = {"file": (audio_file.filename, audio_file, audio_file.content_type)}
    response = requests.post(API_URL, headers=headers, files=files)
    
    if response.status_code == 200:
        output = response.json()
        return jsonify(output)
    else:
        return jsonify({"error": "Failed to transcribe audio"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)

