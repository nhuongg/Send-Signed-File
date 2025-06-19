# app.py

import os
from flask import Flask, request, render_template, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

# --- KHỞI TẠO ỨNG DỤNG FLASK ---
app = Flask(__name__)
# Cấu hình thư mục để upload file
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Cần có secret key để sử dụng flash message
app.config['SECRET_KEY'] = 'mot-chuoi-bi-mat-nao-do'

# --- PHẦN LOGIC XỬ LÝ (Lấy từ code cũ) ---
# Những hàm logic này không thay đổi so với các phiên bản trước
# ... (Bạn có thể copy các hàm generate_keys_logic, sign_file_logic, verify_signature_logic vào đây)
def generate_keys_logic():
    try:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        pem_private = private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())
        with open("private_key.pem", "wb") as f: f.write(pem_private)
        public_key = private_key.public_key()
        pem_public = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
        with open("public_key.pem", "wb") as f: f.write(pem_public)
        return True
    except Exception:
        return False

def sign_file_logic(file_path, private_key_path="private_key.pem"):
    if not os.path.exists(private_key_path):
        return None, "Lỗi: Không tìm thấy file 'private_key.pem'. Vui lòng tạo khóa trước."
    try:
        with open(private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(key_file.read(), password=None)
        with open(file_path, "rb") as f: data = f.read()
        digest = hashes.Hash(hashes.SHA256()); digest.update(data)
        hash_value = digest.finalize()
        signature = private_key.sign(hash_value, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        signature_path = file_path + ".sig"
        with open(signature_path, "wb") as f: f.write(signature)
        return signature_path, None
    except Exception as e:
        return None, f"Lỗi khi ký file: {e}"

def verify_signature_logic(file_path, signature_path, public_key_path="public_key.pem"):
    if not os.path.exists(public_key_path):
        return False, "Lỗi: Không tìm thấy file 'public_key.pem'."
    if not os.path.exists(file_path) or not os.path.exists(signature_path):
        return False, "Lỗi: Không tìm thấy file gốc hoặc file chữ ký."
    try:
        with open(public_key_path, "rb") as key_file: public_key = serialization.load_pem_public_key(key_file.read())
        with open(signature_path, "rb") as f: signature = f.read()
        with open(file_path, "rb") as f: data = f.read()
        digest = hashes.Hash(hashes.SHA256()); digest.update(data)
        hash_value = digest.finalize()
        public_key.verify(signature, hash_value, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True, "✅ Chữ ký HỢP LỆ. File toàn vẹn và đã được xác thực."
    except InvalidSignature:
        return False, "❌ Chữ ký KHÔNG HỢP LỆ! File có thể đã bị thay đổi hoặc chữ ký không đúng."
    except Exception as e:
        return False, f"Lỗi khi xác thực: {e}"


# --- CÁC ĐƯỜNG DẪN (ROUTES) CỦA WEB ---

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Kiểm tra xem có file được gửi lên không
        if 'file' not in request.files:
            flash('Không có file nào được chọn', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('Không có file nào được chọn', 'error')
            return redirect(request.url)

        # Lưu file vào thư mục 'uploads'
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        mode = request.form.get('mode')

        if mode == 'sign':
            signed_file_path, error = sign_file_logic(file_path)
            if error:
                flash(error, 'error')
                return redirect(request.url)
            # Trả về file chữ ký cho người dùng tải xuống
            return send_file(signed_file_path, as_attachment=True)

        elif mode == 'verify':
            if 'signature_file' not in request.files:
                flash('Vui lòng chọn cả file chữ ký (.sig)', 'error')
                return redirect(request.url)
            
            sig_file = request.files['signature_file']
            if sig_file.filename == '':
                flash('Vui lòng chọn cả file chữ ký (.sig)', 'error')
                return redirect(request.url)

            sig_filename = secure_filename(sig_file.filename)
            sig_file_path = os.path.join(app.config['UPLOAD_FOLDER'], sig_filename)
            sig_file.save(sig_file_path)

            is_valid, message = verify_signature_logic(file_path, sig_file_path)
            if is_valid:
                flash(message, 'success')
            else:
                flash(message, 'error')
            return redirect(request.url)

    # Xử lý cho GET request (khi mới vào trang)
    keys_exist = os.path.exists('private_key.pem') and os.path.exists('public_key.pem')
    return render_template('index.html', keys_exist=keys_exist)

@app.route('/generate_keys')
def generate_keys_route():
    success = generate_keys_logic()
    if success:
        flash('Đã tạo cặp khóa private/public thành công!', 'success')
    else:
        flash('Có lỗi xảy ra khi tạo khóa.', 'error')
    return redirect(url_for('index'))

# --- CHẠY ỨNG DỤNG ---

if __name__ == '__main__':
    # Tạo thư mục uploads nếu chưa có
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Lấy cổng từ biến môi trường PORT do Render cung cấp
    # Nếu không tìm thấy biến PORT (ví dụ: chạy trên máy local), mặc định dùng cổng 5000
    port = int(os.environ.get("PORT", 5000))

    # Chạy ứng dụng Flask, lắng nghe trên tất cả các địa chỉ IP (0.0.0.0)
    # và trên cổng được lấy từ biến môi trường PORT
    app.run(debug=True, host='0.0.0.0', port=port)
