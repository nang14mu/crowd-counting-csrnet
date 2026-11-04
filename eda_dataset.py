"""
EDA & Data Statistics Script for ShanghaiTech Dataset
Chức năng:
1. Thống kê số lượng ảnh, tổng số người được gán nhãn
2. Tính toán Min, Max, Mean, Median số người / ảnh
3. Thống kê kích thước ảnh (Resolution)
4. Xuất bảng tổng hợp Markdown và biểu đồ phân phối vào thư mục `reports/`
"""

import os
import glob
import scipy.io as io
import numpy as np
from PIL import Image

def analyze_split(split_name, img_dir, gt_dir):
    img_paths = sorted(glob.glob(os.path.join(img_dir, '*.jpg')))
    counts = []
    resolutions = []

    for img_path in img_paths:
        fname = os.path.splitext(os.path.basename(img_path))[0]
        mat_path = os.path.join(gt_dir, f"GT_{fname}.mat")
        
        # Đọc kích thước ảnh
        with Image.open(img_path) as im:
            w, h = im.size
            resolutions.append((w, h))

        # Đọc nhãn
        if os.path.exists(mat_path):
            mat = io.loadmat(mat_path)
            pts = mat["image_info"][0, 0][0, 0][0]
            counts.append(len(pts))

    counts = np.array(counts)
    return {
        "split": split_name,
        "num_images": len(img_paths),
        "total_heads": int(np.sum(counts)),
        "min_heads": int(np.min(counts)),
        "max_heads": int(np.max(counts)),
        "mean_heads": float(np.mean(counts)),
        "median_heads": float(np.median(counts)),
        "std_heads": float(np.std(counts)),
        "min_res": f"{min(r[0] for r in resolutions)}x{min(r[1] for r in resolutions)}",
        "max_res": f"{max(r[0] for r in resolutions)}x{max(r[1] for r in resolutions)}",
    }

def main():
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Crowd_Counting_ShanghaiTech', 'ShanghaiTech')
    splits = [
        ("Part A Train", os.path.join(root_dir, 'part_A/train_data/images'), os.path.join(root_dir, 'part_A/train_data/ground-truth')),
        ("Part A Test",  os.path.join(root_dir, 'part_A/test_data/images'),  os.path.join(root_dir, 'part_A/test_data/ground-truth')),
        ("Part B Train", os.path.join(root_dir, 'part_B/train_data/images'), os.path.join(root_dir, 'part_B/train_data/ground-truth')),
        ("Part B Test",  os.path.join(root_dir, 'part_B/test_data/images'),  os.path.join(root_dir, 'part_B/test_data/ground-truth')),
    ]

    results = []
    print("\nĐang phân tích thống kê dữ liệu...")
    for name, img_dir, gt_dir in splits:
        res = analyze_split(name, img_dir, gt_dir)
        results.append(res)

    # In bảng Markdown
    report_md = """# BÁO CÁO THỐNG KÊ DỮ LIỆU SHANGHAITECH (DATASET EDA REPORT)
**Người thực hiện:** Trịnh Minh Quân   
**Mục tiêu:** Bàn giao thông số dữ liệu phục vụ huấn luyện CSRNet

| Tập dữ liệu | Số lượng ảnh | Tổng số người | Số người Min | Số người Max | Trung bình (Mean) | Trung vị (Median) | Độ lệch chuẩn (Std) | Độ phân giải |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
"""
    for r in results:
        row = f"| **{r['split']}** | {r['num_images']} | {r['total_heads']:,} | {r['min_heads']} | {r['max_heads']} | {r['mean_heads']:.1f} | {r['median_heads']:.1f} | {r['std_heads']:.1f} | {r['min_res']} ~ {r['max_res']} |\n"
        report_md += row

    os.makedirs('reports', exist_ok=True)
    report_path = os.path.join('reports', 'DATA_EDA_REPORT.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_md)

    print("\n" + report_md)
    print(f"=> Báo cáo đã được lưu vào: {report_path}")

if __name__ == '__main__':
    main()

