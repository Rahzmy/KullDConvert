from flask import Flask, request, send_file, jsonify
from pypdf import PdfReader
from docx import Document
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp'

@app.route('/api/convert', methods=['POST'])
def convert_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_filename = file.filename.replace('.pdf', '.docx')
    output_path = os.path.join(UPLOAD_FOLDER, output_filename)
    
    file.save(input_path)

    try:
        # --- LOGIKA BARU (Lebih Ringan) ---
        # 1. Baca PDF
        reader = PdfReader(input_path)
        
        # 2. Buat Dokumen Word Baru
        doc = Document()
        
        # 3. Salin teks per halaman
        for page in reader.pages:
            text = page.extract_text()
            if text:
                doc.add_paragraph(text)
                doc.add_page_break() # Ganti halaman di Word
        
        # 4. Simpan
        doc.save(output_path)
        # ----------------------------------

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        if os.path.exists(input_path): os.remove(input_path)
