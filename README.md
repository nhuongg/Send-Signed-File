# Công cụ Ký số và Xác thực File bằng Python

Đây là một ứng dụng command-line đơn giản được viết bằng Python để minh họa quá trình tạo chữ ký số cho file và xác thực chúng, dựa trên thuật toán mã hóa bất đối xứng (RSA) và hàm băm an toàn (SHA-256).

## Sơ đồ hoạt động

Ứng dụng được xây dựng dựa trên luồng logic chuẩn của chữ ký số:

### 1. Quy trình Ký (Signing)
![Quy trình ký](https://i.imgur.com/your-image-link-here.png)  - **Data (File)**: File gốc cần được ký.
- **Hash function**: File được đưa qua hàm băm (SHA-256) để tạo ra một chuỗi đại diện có độ dài cố định (hash value).
- **Encrypts using signer's private key**: Giá trị băm này sau đó được "mã hóa" bằng **khóa bí mật (private key)** của người gửi. Kết quả của quá trình này chính là **chữ ký số (digital signature)**.
- **Attach to data**: Chữ ký số được đính kèm (hoặc lưu thành một file riêng) với dữ liệu gốc để gửi đi.

### 2. Quy trình Xác thực (Verification)
![Quy trình xác thực](https://i.imgur.com/your-image-link-here.png) - **Data & Signature**: Người nhận nhận được cả file gốc và file chữ ký.
- **Hash function**: Người nhận dùng đúng hàm băm (SHA-256) để tính toán lại giá trị băm của file gốc nhận được. Ta gọi đây là `hash_1`.
- **Decrypt using signer's public key**: Người nhận dùng **khóa công khai (public key)** của người gửi để "giải mã" chữ ký số. Kết quả thu được là giá trị băm ban đầu do người gửi tạo ra. Ta gọi đây là `hash_2`.
- **Compare**: Hệ thống so sánh `hash_1` và `hash_2`.
    - Nếu **khớp nhau**: Chữ ký hợp lệ. Điều này chứng tỏ file không bị thay đổi trên đường truyền (tính toàn vẹn) và file đúng là của người sở hữu private key (tính xác thực).
    - Nếu **không khớp**: Chữ ký không hợp lệ. File đã bị chỉnh sửa hoặc chữ ký không thuộc về file này.

## Yêu cầu

- Python 3.6+
- Thư viện `cryptography`

Bạn có thể cài đặt thư viện cần thiết bằng pip:
```bash
pip install cryptography
```

## Cách sử dụng

Tất cả các lệnh được thực thi qua file `digital_signature_tool.py`.

### Bước 1: Tạo cặp khóa
Đầu tiên, bạn cần tạo một cặp khóa private/public. Chạy lệnh sau trong terminal:

```bash
python digital_signature_tool.py generate
```

Lệnh này sẽ tạo ra 2 file trong cùng thư mục:
- `private_key.pem`: **KHÓA BÍ MẬT**. Giữ file này tuyệt đối an toàn và không bao giờ chia sẻ nó.
- `public_key.pem`: **KHÓA CÔNG KHAI**. Bạn có thể chia sẻ file này cho bất kỳ ai cần xác thực chữ ký của bạn.

### Bước 2: Ký một file
Giả sử bạn có một file tên là `hop-dong.pdf` và muốn ký nó.

```bash
python digital_signature_tool.py sign --file hop-dong.pdf --private-key private_key.pem
```

Sau khi chạy, một file chữ ký mới sẽ được tạo ra với tên `hop-dong.pdf.sig`. Bây giờ bạn có thể gửi cả `hop-dong.pdf` và `hop-dong.pdf.sig` cho người khác.

### Bước 3: Xác thực một chữ ký
Người nhận (đã có file `public_key.pem` của bạn) sẽ tiến hành xác thực.

#### Trường hợp 1: Chữ ký hợp lệ
```bash
python digital_signature_tool.py verify --file hop-dong.pdf --signature hop-dong.pdf.sig --public-key public_key.pem
```

**Kết quả mong đợi:**
```
✅ Chữ ký HỢP LỆ.
-> File 'hop-dong.pdf' là toàn vẹn và được xác thực.
```

#### Trường hợp 2: Dữ liệu đã bị thay đổi (Chữ ký không hợp lệ)
Giả sử ai đó đã chỉnh sửa file `hop-dong.pdf` sau khi nó được ký. Khi xác thực:

```bash
python digital_signature_tool.py verify --file hop-dong.pdf --signature hop-dong.pdf.sig --public-key public_key.pem
```

**Kết quả mong đợi:**
```
❌ Chữ ký KHÔNG HỢP LỆ!
-> File 'hop-dong.pdf' có thể đã bị thay đổi hoặc chữ ký không đúng.
```

## Lưu ý về bảo mật

- **Đây là một dự án minh họa.** Không nên sử dụng trực tiếp trong môi trường sản phẩm (production) mà không có sự đánh giá và kiểm thử bảo mật chuyên sâu.
- **Bảo vệ Private Key của bạn!** Bất kỳ ai có được private key của bạn đều có thể giả mạo chữ ký của bạn.

## License
Dự án này được cấp phép theo Giấy phép MIT.
