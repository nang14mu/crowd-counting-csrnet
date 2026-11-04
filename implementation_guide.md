# HƯỚNG DẪN CÀI ĐẶT & CHẠY PIPELINE DỮ LIỆU

Tài liệu ngắn gọn hướng dẫn cài đặt thư viện và thực thi 2 Jupyter Notebooks để phân tích và tiền xử lý dữ liệu cho mô hình đếm đám đông.

---

### Bước 1: Cài đặt thư viện cần thiết

Mở PowerShell tại thư mục dự án và chạy:

```powershell
python -m pip install -r requirements.txt
```

*(Nếu dùng công cụ `uv` có sẵn trên máy:)*
```powershell
uv pip install -r requirements.txt
```

---

### Bước 2: Chạy Phân tích & Thống kê Dữ liệu (EDA)

1. Mở file notebook **[eda_dataset.ipynb](file:///d:/University/Seventh%20Semester/Deep%20Learning/Crowd%20Counting/eda_dataset.ipynb)** trong VS Code hoặc Jupyter Notebook.
2. Chọn Python Kernel (Python 3.10 hoặc 3.11).
3. Bấm **Run All** (hoặc chạy lần lượt từng ô lệnh).

* **Kết quả thu được:**
  - Bảng thống kê chi tiết số người (Min, Max, Mean, Median, Std) và độ phân giải ảnh hiển thị trực tiếp trong notebook.
  - Tự động xuất biểu đồ phân phối tần suất và biểu đồ hộp tại: `reports/figures/count_distribution_comparison.png`.
  - Hiển thị trực quan các ảnh mẫu đối chiếu: `[Ảnh gốc]` | `[Tọa độ điểm đầu người]` | `[Ground Truth Density Map]`.
  - Toàn bộ nội dung phân tích chi tiết đã được lưu sẵn tại: **[reports/DATA_EDA_REPORT.md](file:///d:/University/Seventh%20Semester/Deep%20Learning/Crowd%20Counting/reports/DATA_EDA_REPORT.md)** để đưa vào báo cáo đồ án.

---

### Bước 3: Chạy Tiền xử lý Dữ liệu & Sinh Ground Truth Density Map

1. Mở file notebook **[preprocess_dataset.ipynb](file:///d:/University/Seventh%20Semester/Deep%20Learning/Crowd%20Counting/preprocess_dataset.ipynb)** trong VS Code hoặc Jupyter Notebook.
2. Bấm **Run All**.

* **Quá trình thực hiện:**
  - Sinh bản đồ nhiệt density map dạng HDF5 (`.h5`) lưu cạnh mỗi file ảnh `.jpg` (áp dụng KD-Tree Geometry-adaptive Gaussian cho Part A và Fixed Gaussian cho Part B, co 1/8 và nhân hệ số 64).
  - Tự động chia tỷ lệ 90% Train / 10% Val và xuất 6 file JSON chỉ mục đường dẫn tương đối (portable):
    * `part_A_train.json`, `part_A_val.json`, `part_A_test.json`
    * `part_B_train.json`, `part_B_val.json`, `part_B_test.json`
  - Thực hiện ô kiểm tra chất lượng (Sanity Check) đảm bảo độ sai lệch tích phân $\le 0.05$ người.

*(Thời gian chạy: khoảng 5 - 15 phút tùy CPU, tự động bỏ qua các ảnh đã có sẵn file `.h5`).*

---

### Kết quả đầu ra bàn giao (Gửi cho bạn Nam Huấn luyện)

Sau khi chạy xong 2 notebook trên, bạn bàn giao:
1. Thư mục dữ liệu đã sinh đầy đủ các file `.h5`: `Crowd_Counting_ShanghaiTech/ShanghaiTech/`
2. 6 file danh sách JSON tại thư mục gốc: `part_A_*.json` và `part_B_*.json`
3. Báo cáo phân tích số liệu: **[reports/DATA_EDA_REPORT.md](file:///d:/University/Seventh%20Semester/Deep%20Learning/Crowd%20Counting/reports/DATA_EDA_REPORT.md)**
