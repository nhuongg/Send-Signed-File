# Ứng dụng Ký số & Xác thực File (Giao diện Web với Python + Flask)

Đây là một ứng dụng web minh họa quy trình tạo chữ ký số và xác thực chữ ký cho file. Người dùng có thể tải file lên, thực hiện ký số bằng khóa bí mật (private key) và sau đó xác thực tính toàn vẹn cũng như nguồn gốc của file bằng khóa công khai (public key).

Toàn bộ logic xử lý được xây dựng bằng Python với thư viện `cryptography`, và giao diện người dùng được hiển thị trên nền web thông qua framework Flask.

---

## Giao diện ứng dụng

 - Giao diện ký số
<p align="center">  
   <img src="Picture/Screenshot (96).png" alt="Ảnh minh họa" width="850" height="480">  
</p>

 - Giao diện xác thực
<p align="center">  
   <img src="Picture/Screenshot (96).png" alt="Ảnh minh họa" width="850" height="480">  
</p>

---

## Công nghệ sử dụng

* **Backend**: Python 3, Flask
* **Thư viện mã hóa**: `cryptography` (cho thuật toán RSA và hàm băm SHA-256)
* **Frontend**: HTML5, CSS3, JavaScript (để xử lý giao diện động)

---

## Sơ đồ hoạt động

Quy trình mã hóa dựa trên nguyên tắc của mã hóa bất đối xứng:

1.  **Quy trình Ký (Signing)**:
    * File được băm (hash) bằng thuật toán SHA-256 để tạo ra một chuỗi dữ liệu đại diện duy nhất.
    * Giá trị băm này được mã hóa bằng **khóa bí mật (private key)** của người gửi. Kết quả chính là **chữ ký số**.
    * Chữ ký được lưu thành một file riêng (`.sig`).

2.  **Quy trình Xác thực (Verification)**:
    * Người nhận tính toán lại giá trị băm của file gốc nhận được.
    * Người nhận dùng **khóa công khai (public key)** của người gửi để giải mã chữ ký, lấy ra giá trị băm ban đầu.
    * Nếu hai giá trị băm này **trùng khớp**, chữ ký hợp lệ, file được đảm bảo toàn vẹn và đúng nguồn gốc.

---

## Cài đặt & Chạy dự án

Để chạy dự án này trên máy của bạn, hãy làm theo các bước sau:

**1. Tải mã nguồn về**

```bash
git clone [https://github.com/nhuongg/Send-Signed-File.git](https://github.com/your-username/your-repository-name.git)
cd Send-Signed-File
```
*(Thay `your-username/your-repository-name` bằng thông tin repo của bạn)*

**2. Tạo và kích hoạt môi trường ảo (Khuyến khích)**

Điều này giúp cô lập các thư viện của dự án, tránh xung đột.

* Trên macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
* Trên Windows:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

**3. Cài đặt các thư viện cần thiết**

Dự án có 2 thư viện chính là Flask và cryptography.

```bash
pip install Flask cryptography
```

**4. Chạy ứng dụng**

Sau khi cài đặt xong, chạy file `app.py` để khởi động server:

```bash
python app.py
```

Terminal sẽ hiển thị một dòng thông báo cho biết server đang chạy, thường là:
`* Running on http://127.0.0.1:5000`

**5. Truy cập ứng dụng**

Mở trình duyệt web (Chrome, Firefox,...) và truy cập vào địa chỉ: **http://127.0.0.1:5000**

---

## Cách sử dụng

Giao diện web rất trực quan và dễ sử dụng.

**1. Tạo cặp khóa (Lần đầu tiên)**
* Nếu bạn chưa có cặp khóa `private_key.pem` và `public_key.pem`, một nút màu xanh sẽ xuất hiện.
* Hãy nhấn vào nút **"Bấm vào đây để tạo cặp khóa lần đầu"**.
* Trang sẽ tự động tải lại và một thông báo thành công sẽ hiện ra.

**2. Để ký một file**
* Tại mục "1. Chọn chế độ", chọn **"Ký số"**.
* Nhấn vào nút **"Chọn File"** và chọn file bạn muốn ký từ máy tính.
* Nhấn nút **"Thực hiện"**.
* Trình duyệt sẽ tự động tải về một file có đuôi `.sig`. Đây chính là file chữ ký của bạn.

**3. Để xác thực một chữ ký**
* Tại mục "1. Chọn chế độ", chọn **"Xác thực"**.
* Hai ô chọn file sẽ hiện ra.
* Tại "2. Chọn file gốc", hãy chọn file dữ liệu gốc (ví dụ: `document.pdf`).
* Tại "3. Chọn file chữ ký", hãy chọn file `.sig` tương ứng (ví dụ: `document.pdf.sig`).
* Nhấn nút **"Thực hiện"**.
* Một thông báo sẽ xuất hiện ở đầu trang cho biết chữ ký **HỢP LỆ** hay **KHÔNG HỢP LỆ**.

---

## Cấu trúc thư mục

```
/digital_signature_webapp/
|
|-- app.py             # File Python chính chứa server Flask
|
|-- /templates/
|   |-- index.html     # File giao diện HTML
|
|-- /uploads/
|   # Thư mục tạm thời chứa các file được upload lên
|
|-- private_key.pem    # (Được tạo tự động)
|-- public_key.pem     # (Được tạo tự động)
|
|-- README.md          # File hướng dẫn này
```

---

## ⚠️ Lưu ý về Bảo mật

* Đây là một dự án **minh họa** cho mục đích học tập. Không nên sử dụng trong môi trường sản phẩm thực tế mà không có sự đánh giá và kiểm thử bảo mật chuyên sâu.
* File `private_key.pem` là **tuyệt đối bí mật**. Bất kỳ ai có được file này đều có thể giả mạo chữ ký của bạn. Hãy bảo vệ nó cẩn thận.

---

## License

Dự án này được tạo để phục vụ cho mục đích học tập.
