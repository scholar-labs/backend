from flask import Flask
from flask import request
from PyPDF2 import PdfReader

app = Flask(__name__)

# here's how you can create a route
@app.route('/test')
def say_hello():   
    return ('hello')


# route to extract text from pdf
@app.route('/extract-text', methods=['POST'])
def extract_text_from_pdf():
    uploaded_pdf_file = request.files['file'] # name in request would have to be 'file'.
    reader = PdfReader(uploaded_pdf_file)
    number_of_pages = len(reader.pages)
    text = ''
    for i in range(number_of_pages):
        page = reader.pages[i]
        text = text + page.extract_text()
    return text


if __name__ == '__main__':
    app.run(debug=True)
