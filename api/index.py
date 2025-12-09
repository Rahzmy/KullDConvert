from flask import Flask, request, send_file, jsonify
import os
from werkzeug.utils import secure_filename
from pdf2docx import Converter

app = Flask(__name__)

# Konfigurasi folder upload sementara
UPLOAD_FOLDER = '/tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/convert', methods=['POST'])
def convert_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Simpan file PDF ke /tmp
        file.save(pdf_path)
        
        # Tentukan nama output docx
        docx_filename = filename.rsplit('.', 1)[0] + '.docx'
        docx_path = os.path.join(app.config['UPLOAD_FOLDER'], docx_filename)

        try:
            # Proses Konversi
            cv = Converter(pdf_path)
            cv.convert(docx_path, start=0, end=None)
            cv.close()

            # Kirim file balik ke user
            return send_file(docx_path, as_attachment=True, download_name=docx_filename)

        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
        finally:
            # Bersihkan file dari /tmp untuk menghemat ruang
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            # File docx biasanya dihapus otomatis oleh OS di folder tmp, 
            # atau bisa dihapus setelah dikirim (sedikit tricky di serverless sync).

# Route default untuk memastikan API berjalan
@app.route('/api/hello')
def hello():
    return "KullDConvert API is running!"

# Handler untuk Vercel
app.debug = True
