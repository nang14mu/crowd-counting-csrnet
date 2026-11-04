# HƯỚNG DẪN CÀI ĐẶT & CHẠY PIPELINE DỮ LIỆU

---

### Bước 1: Cài đặt thư viện cần thiết

Mở PowerShell tại thư mục dự án và chạy lệnh:

```powershell
python -m pip install numpy scipy h5py opencv-python pillow matplotlib
```

_(Nếu máy báo lỗi không tìm thấy `pip`, bạn có thể dùng lệnh thay thế:)_

```powershell
uv pip install numpy scipy h5py opencv-python pillow matplotlib
```

---

### Bước 2: Chạy thống kê dữ liệu (EDA)

Trích xuất số lượng người (Min, Max, Mean, Median) và độ phân giải ảnh để đưa vào báo cáo đồ án:

```powershell
python eda_dataset.py
```

- **Kết quả:** Bảng thống kê hiển thị trên màn hình và tự động lưu tại `reports/DATA_EDA_REPORT.md`.

---

### Bước 3: Chạy tiền xử lý tạo Ground Truth Density Map

Tạo bản đồ mật độ `.h5` (co 1/8, nhân 64, Gaussian KD-Tree cho Part A và Fixed cho Part B) và chia tập train/val/test:

```powershell
python preprocess_dataset.py
```

_(Thời gian chạy: khoảng 5 - 15 phút tùy CPU)._

---
