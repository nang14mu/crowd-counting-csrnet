# Tiêu chí Đánh giá & Nghiệm thu (Evaluation Criteria)

Tài liệu này xác định các tiêu chuẩn kỹ thuật bắt buộc để nghiệm thu chất lượng của từng giai đoạn trong pipeline mô hình Crowd Counting.

---

## 1. Tiêu chí Dữ liệu (Data Engineering Gate)

- **Bảo toàn số đếm (Count Conservation):**
  - Với mỗi ảnh có $N$ người, tổng các giá trị trên bản đồ mật độ ground truth $D_{GT}$ sau khi downsample 1/8 và scale 64 phải thỏa mãn:
    $$\left| \sum_{x, y} D_{GT}(x, y) - N \right| \le 0.05$$
- **Độ phủ dữ liệu:** Toàn bộ file ảnh `.jpg` phải có file `.h5` tương ứng cùng thư mục và cùng tên.
- **Tính hợp lệ của split:** Danh sách `train.json`, `val.json`, `test.json` không được có phần tử giao nhau (no data leakage).

---

## 2. Tiêu chí Kiến trúc Mô hình (Model Architecture Gate)

- **Tensor Shape Match:** Đầu vào ảnh $(B, 3, H, W)$ cho đầu ra $(B, 1, \lfloor H/8 \rfloor, \lfloor W/8 \rfloor)$.
- **Receptive Field:** Backend Dilated Convolution phải đạt trường tiếp nhận tối thiểu $32 \times 32$ pixel để bao phủ toàn bộ vùng ngữ cảnh đầu người ở các tỷ lệ xa gần.

---

## 3. Tiêu chí Huấn luyện (Training & Optimization Gate)

- **Loss Convergence:** Hàm Euclidean Loss phải giảm đơn điệu theo các epoch chính, không có hiện tượng dao động đột ngột hoặc xuất hiện giá trị `NaN / Inf`.
- **Checkpointing:** Luôn lưu trữ `model_best.pth.tar` với metadata: `epoch`, `best_prec1` (MAE thấp nhất), `state_dict`, `optimizer_state_dict`.

---

## 4. Tiêu chí Đánh giá Hiệu năng (Benchmark Targets)

### Bộ dữ liệu ShanghaiTech (Chuẩn CVPR 2018):

| Tập dữ liệu             | Đặc điểm                      | MAE Tối đa (Nghiệm thu) | MSE Tối đa (Nghiệm thu) | MAE Kỷ lục CSRNet gốc |
| :---------------------- | :---------------------------- | :---------------------: | :---------------------: | :-------------------: |
| **ShanghaiTech Part A** | Mật độ cực cao, góc chụp rộng |       $\le 68.0$        |       $\le 115.0$       |       **66.4**        |
| **ShanghaiTech Part B** | Mật độ thưa, đường phố đô thị |       $\le 11.5$        |       $\le 18.0$        |       **10.6**        |

### Cách tính toán Metric:

1. **MAE (Mean Absolute Error):**
   $$\text{MAE} = \frac{1}{N} \sum_{i=1}^N |C_i - \hat{C}_i|$$
2. **MSE (Mean Squared Error / RMSE):**
   $$\text{MSE} = \sqrt{\frac{1}{N} \sum_{i=1}^N (C_i - \hat{C}_i)^2}$$
