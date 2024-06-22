from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from fpdf import FPDF
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PDF_FOLDER'] = 'pdfs'
app.config['ALLOWED_EXTENSIONS'] = {'txt'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PDF_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def text_to_pdf(text_file_path, pdf_file_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    with open(text_file_path, 'r') as file:
        for line in file:
            pdf.cell(200, 10, txt=line, ln=True, align='L')
    pdf.output(pdf_file_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        text_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(text_file_path)
        pdf_filename = filename.rsplit('.', 1)[0] + '.pdf'
        pdf_file_path = os.path.join(app.config['PDF_FOLDER'], pdf_filename)
        text_to_pdf(text_file_path, pdf_file_path)
        return redirect(url_for('download_file', filename=pdf_filename))
    return redirect(request.url)

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['PDF_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
