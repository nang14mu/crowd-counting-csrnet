# BÁO CÁO PHÂN TÍCH KHÁM PHÁ DỮ LIỆU ĐẾM ĐÁM ĐÔNG (SHANGHAITECH EDA REPORT)

- **Dự án:** Ước Lượng Mật Độ & Đếm Đám Đông (Crowd Counting & Density Map Estimation)
- **Kế thừa & Thử nghiệm trên mô hình:** CSRNet (CVPR 2018)
- **Người thực hiện:** Trịnh Minh Quân
- **Ngày hoàn thành:** 04/11/2026

---

## 1. TỔNG QUAN BỘ DỮ LIỆU (DATASET OVERVIEW)

Bộ dữ liệu **ShanghaiTech** (giới thiệu tại CVPR 2016 bởi Zhang et al.) là bộ dữ liệu tiêu chuẩn (_gold standard benchmark_) được sử dụng rộng rãi nhất để đánh giá hiệu năng các mô hình đếm đám đông.

Toàn bộ tập dữ liệu gồm **1,198 bức ảnh**, tổng cộng **329,547 điểm đầu người** được gán nhãn thủ công (mỗi điểm đầu người được xác định bởi một tọa độ pixel $(x, y)$).

Bộ dữ liệu phân tách thành 2 phần độc lập với đặc tính không gian và mật độ hoàn toàn khác nhau:

1. **ShanghaiTech Part A (Cảnh cực đông ngoài trời - Highly Congested):** Thu thập ngẫu nhiên từ mạng Internet (các cuộc tuần hành, mít tinh, lễ hội âm nhạc, khán đài sân vận động).
2. **ShanghaiTech Part B (Cảnh đường phố đô thị - Sparse Urban):** Chụp từ các góc camera cố định trên các tuyến phố đi bộ sầm uất tại Thượng Hải.

---

## 2. BẢNG TỔNG HỢP PHÂN TÍCH ĐỊNH LƯỢNG (QUANTITATIVE ANALYSIS TABLE)

Dưới đây là số liệu thống kê chi tiết được trích xuất trực tiếp từ toàn bộ 1,198 ảnh và file nhãn `.mat`:

| Tập dữ liệu             |   Phân vùng   | Số lượng ảnh |  % Số ảnh   | Tổng số người | % Số người  | Số người Min | Số người Max | Trung bình (Mean) | Trung vị (Median) | Độ lệch chuẩn (Std) |       Dải phân giải (Resolution)       |
| :---------------------- | :-----------: | :----------: | :---------: | :-----------: | :---------: | :----------: | :----------: | :---------------: | :---------------: | :-----------------: | :------------------------------------: |
| **ShanghaiTech Part A** |   **Train**   |     300      |   25.04%    |    162,413    |   49.28%    |      33      |    3,138     |     **541.4**     |       378.0       |        504.3        | $299 \times 182 \sim 1024 \times 1024$ |
|                         |   **Test**    |     182      |   15.19%    |    78,862     |   23.93%    |      66      |    2,256     |     **433.3**     |       307.5       |        353.5        | $293 \times 200 \sim 1024 \times 1024$ |
|                         | _Tổng Part A_ |    _482_     |  _40.23%_   |   _241,275_   |  _73.21%_   |     _33_     |   _3,138_    |      _500.6_      |      _351.0_      |       _453.6_       |     _Đa kích thước, không cố định_     |
| **ShanghaiTech Part B** |   **Train**   |     400      |   33.39%    |    49,151     |   14.91%    |      12      |     576      |     **122.9**     |       99.0        |        93.8         |      $1024 \times 768$ (Cố định)       |
|                         |   **Test**    |     316      |   26.38%    |    39,121     |   11.87%    |      9       |     539      |     **123.8**     |       93.0        |        95.1         |      $1024 \times 768$ (Cố định)       |
|                         | _Tổng Part B_ |    _716_     |  _59.77%_   |   _88,272_    |  _26.79%_   |     _9_      |    _576_     |      _123.3_      |      _96.0_       |       _94.4_        |     _Độ phân giải đồng nhất 100%_      |
| **TOÀN BỘ DỮ LIỆU**     |               |  **1,198**   | **100.00%** |  **329,547**  | **100.00%** |    **9**     |  **3,138**   |     **275.1**     |     **156.0**     |      **341.2**      |                   —                    |

### 2.1. Phân tích Tỷ trọng Dữ liệu (% Data Proportion Analysis)

![Tỷ lệ phân bổ dữ liệu ShanghaiTech](figures/proportion_distribution.png)

1. **Nghịch lý Mật độ giữa Part A và Part B:**
   - **Part A** chỉ chiếm **40.23% tổng số lượng ảnh** (482 / 1,198 ảnh) nhưng lại nắm giữ tới **73.21% tổng số lượng người** (241,275 / 329,547 người).
   - Ngược lại, **Part B** chiếm tới **59.77% tổng số lượng ảnh** (716 / 1,198 ảnh) nhưng chỉ đóng góp **26.79% tổng số lượng người** (88,272 / 329,547 người).
   - **Hệ quả kỹ thuật:** Mật độ trung bình trên mỗi ảnh của Part A cao gấp hơn **4 lần** Part B. Do đó, việc tách riêng 2 mô hình huấn luyện độc lập cho Part A và Part B (như thiết kế của tác giả CSRNet) là hoàn toàn chính xác và khoa học.

2. **Tỷ lệ phân chia Train / Test:**
   - **Tập Huấn luyện (Train):** 700 ảnh (**58.43%** số ảnh), 211,564 người (**64.20%** số người).
   - **Tập Kiểm thử (Test):** 498 ảnh (**41.57%** số ảnh), 117,983 người (**35.80%** số người).
   - Tỷ lệ kiểm thử 41.57% là một tỷ lệ tương đối lớn trong học sâu, giúp việc đánh giá chỉ số MAE/MSE có độ tin cậy và tính khái quát cao.

---

## 3. SO SÁNH CHUYÊN SÂU: PART A vs PART B

```mermaid
graph LR
    subgraph Part A [Part A - Thách thức cực độ]
        A1["Mật độ: 500 người/ảnh (Max 3,138)"]
        A2["Kích thước: Tùy biến (299x182 -> 1024x1024)"]
        A3["Che khuất: Nghiêm trọng, đầu người 3-5px"]
        A4["Phương pháp: Geometry-adaptive Gaussian (k-NN)"]
    end
    subgraph Part B [Part B - Đường phố ổn định]
        B1["Mật độ: 123 người/ảnh (Max 576)"]
        B2["Kích thước: Cố định 1024x768"]
        B3["Che khuất: Nhẹ, nhận diện rõ thân người"]
        B4["Phương pháp: Fixed Gaussian Kernel (sigma=15)"]
    end
```

### 3.1. Về Mật độ & Phân phối (Density & Distribution)

- **Part A:** Độ phân tán cực kỳ lớn (Std = 504.3). Có những ảnh chỉ 33 người nhưng có những ảnh lên tới **3,138 người** nén chặt vào một khung hình. Phân phối bị lệch phải nghiêm trọng (_heavy right-skewed_), đòi hỏi mô hình phải có khả năng khái quát tốt trên các dải mật độ đa dạng.
- **Part B:** Phân phối đồng đều, đối xứng và ổn định hơn rất nhiều (Mean $\approx$ 123 người, Median $\approx$ 96 người, Max chỉ 576 người).

### 3.2. Về Kích thước ảnh & Tỷ lệ phối cảnh (Resolution & Perspective)

- **Part A:** Mỗi ảnh có một tỷ lệ khung hình và độ phân giải khác nhau (từ rất nhỏ $299 \times 182$ đến vuông $1024 \times 1024$). Điều này gây khó khăn khi gom batch huấn luyện (phải train với `batch_size = 1` hoặc crop ngẫu nhiên).
- **Part B:** 100% các bức ảnh đều có độ phân giải chuẩn $1024 \times 768$ pixel, góc nhìn từ camera trên cao nhìn xuống (surveillance perspective).

---

## 4. VÍ DỤ MINH HỌA TRỰC QUAN (CASE STUDIES)

Để hiểu rõ dữ liệu, nhóm đã tiến hành trực quan hóa đối chiếu 3 lớp thông tin cho từng trường hợp điển hình:

### Ví dụ 1: Trường hợp Cực đông (Part A - `IMG_1.jpg`)

- **Số người thực tế (Ground Truth count):** $1,547$ người.
- **Đặc điểm:** Các cá nhân ở tiền cảnh (gần ống kính) có khuôn mặt to rõ ràng; trong khi hàng nghìn người ở hậu cảnh chỉ hiển thị dưới dạng các chấm nhỏ li ti (3 đến 5 pixel).
- **Bản đồ nhiệt Density Map:**
  - Vùng hậu cảnh: Các đốm nhiệt Gaussian thu nhỏ lại ($\sigma_i \approx 1.5 - 2.5$) để phân biệt từng cá nhân đứng sát nhau.
  - Vùng tiền cảnh: Đốm nhiệt Gaussian mở rộng ($\sigma_i \approx 8.0 - 15.0$) tương ứng với kích thước đầu người lớn hơn.
- **Tích phân bảo toàn:** $\sum \text{DensityMap}_{1/8} = 1,546.98$ (Sai số tuyệt đối $< 0.02$ người).

### Ví dụ 2: Trường hợp Thưa thớt đường phố (Part B - `IMG_1.jpg`)

- **Số người thực tế (Ground Truth count):** $117$ người.
- **Đặc điểm:** Người đi bộ di chuyển trên vỉa hè, khoảng cách giữa các người tương đối rộng rãi, hầu như không có hiện tượng chen lấn chồng chất.
- **Bản đồ nhiệt Density Map:** Sử dụng bộ lọc Gaussian cố định ($\sigma = 15$) tạo ra các tâm nhiệt rõ ràng xung quanh mỗi người, nền đường phố và cây xanh hoàn toàn có giá trị mật độ bằng $0$.
- **Tích phân bảo toàn:** $\sum \text{DensityMap}_{1/8} = 117.00$ (Chính xác 100%).

---

## 5. CƠ SỞ KHOA HỌC CỦA BƯỚC TIỀN XỬ LÝ (PREPROCESSING RATIONALE)

### 5.1. Tại sao không dùng Object Detection (Bounding Box)?

Trong Part A, với mật độ hơn 3,000 người/ảnh:

- Nếu dùng hộp chữ nhật bounding box, các hộp sẽ chồng đè lên nhau 90% - 95%, thuật toán Non-Maximum Suppression (NMS) của YOLO/Faster R-CNN sẽ triệt tiêu nhầm các mục tiêu hợp lệ.
- Do đó, biểu diễn bằng **Bản đồ Mật độ (Density Map)** là giải pháp toán học duy nhất bảo toàn được tổng số lượng người thông qua phép tích phân không gian:
  $$\text{Count} = \iint D(x, y) \, dx dy$$

### 5.2. Tại sao phải dùng KD-Tree Geometry-Adaptive Gaussian cho Part A?

Khoảng cách giữa các đầu người tỷ lệ thuận với kích thước thực của đầu người do hiệu ứng phối cảnh xa - gần (perspective effect).

- Thuật toán **KD-Tree** tìm 3 láng giềng gần nhất ($k=3$) với độ phức tạp $O(N \log N)$.
- Khoảng cách trung bình $\bar{d}_i$ phản ánh chính xác kích thước đầu người tại vị trí đó:
  $$\sigma_i = \beta \cdot \bar{d}_i \quad (\beta = 0.3)$$
- Nếu dùng $\sigma$ cố định quá to cho Part A, bản đồ nhiệt ở vùng đông sẽ bị nhòe thành một khối phẳng lì vô nghĩa, mô hình không học được biên đặc trưng.

### 5.3. Tại sao phải co 1/8 và nhân 64?

- Frontend của CSRNet gồm 10 lớp Conv VGG-16 kèm 3 lớp MaxPool ($2 \times 2 \times 2 = 8$). Kích thước feature map đầu ra giảm 8 lần so với ảnh gốc ($H/8, W/8$).
- Khi co kích thước 8 lần, diện tích giảm đi $8 \times 8 = 64$ lần. Bắt buộc phải nhân mỗi pixel với 64 để tổng số lượng người được bảo toàn trọn vẹn:
  $$\sum \text{DensityMap}_{1/8} \times 64 = \sum \text{DensityMap}_{\text{gốc}} \approx N$$

---

## 6. KHUYẾN NGHỊ BÀN GIAO CHO KỸ SƯ HUẤN LUYỆN

1. **Về Hàm Mất Mát (Loss Function):**
   - Do ground truth density map được nhân hệ số 64, nên tổng loss theo pixel sẽ khá lớn. Bắt buộc cấu hình `nn.MSELoss(reduction='sum')` và đặt **Learning Rate cực nhỏ** ($10^{-7}$) kết hợp SGD momentum 0.95 để tránh hiện tượng bùng nổ gradient (`loss: nan`).
2. **Về Chiến lược Huấn luyện trên 2 tập:**
   - **Tập Part B:** Dễ hội tụ hơn do ảnh cùng kích thước $1024 \times 768$ và mật độ ổn định. Nên train thử nghiệm Part B trước để kiểm tra pipeline. Mục tiêu nghiệm thu: $\text{MAE} \le 11.5$.
   - **Tập Part A:** Cần nhiều epoch hơn (khoảng 300 - 400 epochs), nên huấn luyện với `batch_size = 1` hoặc crop ngẫu nhiên $1/4$ khung hình để tăng tính khái quát. Mục tiêu nghiệm thu: $\text{MAE} \le 68.0$.
3. **Danh sách Tệp bàn giao sẵn sàng:**
   - Thư mục dữ liệu đã tạo sẵn toàn bộ file `.h5`: `Crowd_Counting_ShanghaiTech/ShanghaiTech/`
   - 6 file JSON chỉ mục đường dẫn tương đối chuẩn: `part_A_train.json`, `part_A_val.json`, `part_A_test.json`, `part_B_train.json`, `part_B_val.json`, `part_B_test.json`.
