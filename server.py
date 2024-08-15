from flask import Flask, jsonify, request
from PyPDF2 import PdfReader
import requests
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

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

# route to get captions using video link
@app.route('/captions')
def get_captions():
    video_link = request.args.get('link')
    video_id = video_link.split('v=')[-1][:11]
    captions = YouTubeTranscriptApi.get_transcript(video_id)
    l = len(captions)
    ans = ''
    for i in captions:
        ans = ans + ' ' + i['text']
    return ans


# route for Q/A
@app.route('/answer')
def QnA():
    genai.configure(api_key="AIzaSyCVMJybj7KW5wTqaFzl3McAHhqebnNfDSA")
    model = genai.GenerativeModel('gemini-1.5-flash')
    context = request.args.get('context')
    question = request.args.get('question')
    prompt = f"Given the context: {context}, and the question: {question}, please provide a clear and concise answer in plain text format."
    response = model.generate_content(prompt)
    text_response = response.candidates[0].content.parts[0].text
    text_response = text_response.replace('\n', '')
    return text_response

# route to summarize text
@app.route('/summarize', methods=['POST'])
def summarize_text():
    genai.configure(api_key="AIzaSyA0pe28Sg_5RCyDSxI8ea4r-LFHNTWbod4")
    model = genai.GenerativeModel('gemini-1.5-flash')
    data = request.json
    text_to_summarize = data.get('text')
    prompt = f"Please summarize the following text: {text_to_summarize}"
    response = model.generate_content(prompt)
    summary = response.candidates[0].content.parts[0].text
    return jsonify({"summary": summary})

if __name__ == '__main__':
    app.run(debug=True)
