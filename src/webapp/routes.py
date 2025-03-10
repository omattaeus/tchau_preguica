from flask import render_template, request, redirect, url_for
from src.webapp import app
import os
from werkzeug.utils import secure_filename
from src.ocr_processor import extract_receipt_data
from src.storage import save_receipt

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Página principal mostrando todos os comprovantes."""
    # Aqui você pode buscar os comprovantes do banco de dados ou da pasta
    receipts = os.listdir("data/")  # Simplificação para testar
    return render_template('index.html', receipts=receipts)

@app.route('/upload', methods=['GET', 'POST'])
def upload_comprobante():
    """Permitir que o usuário envie um comprovante."""
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            data = extract_receipt_data(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            save_receipt(filename, data['amount'], data['date'])

            return redirect(url_for('index'))
    return render_template('upload.html')