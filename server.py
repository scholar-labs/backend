from flask import Flask, jsonify, request
from PyPDF2 import PdfReader
import requests
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

# here's how you can create a route
@app.route('/test')
def say_hello():   
    return ('hello')

# route to extract text from pdf
@app.route('/pdf-to-text', methods=['POST'])
def extract_text_from_pdf():
    uploaded_pdf_file = request.files['file'] # name in request would have to be 'file'.
    reader = PdfReader(uploaded_pdf_file)
    number_of_pages = len(reader.pages)
    text = ''
    for i in range(number_of_pages):
        page = reader.pages[i]
        text = text + page.extract_text()
    return text

# route to convert audio to text
@app.route('/audio-to-text', methods=['POST'])
def audio_to_text():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    audio_file = request.files['audio']
    file_data = audio_file.read()
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    headers = {"Authorization": "Bearer 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"}
    response = requests.post(API_URL, headers=headers, data=file_data)
    output = response.json()
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)
