from flask import Flask, request, send_file, jsonify
from pdf2docx import Converter
import os

app = Flask(__name__)

# Konfigurasi folder sementara (Vercel hanya mengizinkan tulis di /tmp)
UPLOAD_FOLDER = '/tmp'

@app.route('/api/convert', methods=['POST'])
def convert_file():
    # 1. Cek apakah ada file yang diupload
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # 2. Simpan file PDF ke /tmp
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_filename = file.filename.replace('.pdf', '.docx')
    output_path = os.path.join(UPLOAD_FOLDER, output_filename)
    
    file.save(input_path)

    try:
        # 3. PROSES KONVERSI (Serverless Logic)
        # Logika: PDF -> DOCX
        cv = Converter(input_path)
        cv.convert(output_path, start=0, end=None)
        cv.close()

        # --- AREA TRACKING (Poin 3 Tugas) ---
        # Di sinilah nanti Anda menyisipkan kode ke Database (Supabase/Firebase)
        # Contoh: database.insert({filename: file.filename, status: "success"})
        print(f"Log: Berhasil mengonversi {file.filename}") 

        # 4. Kirim balik file hasil ke user
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        # Bersihkan file sampah di /tmp agar memori tidak penuh
        if os.path.exists(input_path): os.remove(input_path)
        # Output path biasanya dihapus otomatis oleh sistem nanti, tapi bisa dihapus manual jika mau

# Handler wajib untuk Vercel
# Tidak perlu app.run()
