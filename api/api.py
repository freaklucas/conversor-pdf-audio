from io import StringIO
from io import BytesIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from flask import send_file, send_from_directory, safe_join, abort

import gtts
from flask import Flask
from flask import request

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def hello():
    return "hello wordl desu"

@app.route('/tes1', methods=['GET', 'POST'])
def hel():
    return "hello desu"

@app.route('/pdf_normal', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        output_string = StringIO()
        in_file = request.files["file"]
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
        texto = output_string.getvalue()
        # Gerando mp3
        tts = gtts.gTTS(texto,  lang="pt-br")
        mp3_fp = BytesIO()
        # tts.write_to_fp(mp3_fp)
        tts.save('mp3_fp.mp3')
        
        return send_file('mp3_fp.mp3', as_attachment=True)
    else:
        return "teste"

app.run()