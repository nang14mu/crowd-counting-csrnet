"""
Preprocessing Script for ShanghaiTech Dataset (Python 3)
Chức năng:
1. Đọc nhãn gốc .mat (tọa độ x, y các điểm đầu người)
2. Sinh Ground Truth Density Map:
   - Part A: Geometry-adaptive Gaussian Kernel (KD-Tree k-NN, k=3, beta=0.3)
   - Part B: Fixed Gaussian Kernel (sigma=15)
3. Thu nhỏ 1/8 kích thước & nhân 64 (bảo toàn tích phân số lượng người)
4. Lưu file .h5 cùng tên cạnh mỗi file ảnh .jpg
5. Phân chia Train / Val (90/10) và xuất file json: train.json, val.json, test.json
"""

import os
import glob
import json
import random
import h5py
import scipy.io as io
import numpy as np
from PIL import Image
import scipy.spatial
import scipy.ndimage
import cv2

# Cố định seed ngẫu nhiên để đảm bảo tính tái lập (Reproducibility)
random.seed(42)
np.random.seed(42)

def gaussian_filter_density_adaptive(gt_pts, img_shape):
    """
    Sinh density map cho Part A (cảnh đông đúc) bằng Geometry-adaptive Gaussian (k-NN KD-Tree)
    """
    density = np.zeros(img_shape, dtype=np.float32)
    gt_count = len(gt_pts)
    if gt_count == 0:
        return density

    pts = np.array(gt_pts)
    leafsize = 2048
    tree = scipy.spatial.KDTree(pts.copy(), leafsize=leafsize)
    # Tìm 4 điểm gần nhất (điểm thứ nhất là chính nó, 3 điểm tiếp theo là láng giềng)
    distances, _ = tree.query(pts, k=min(4, gt_count))

    for i, pt in enumerate(pts):
        x = min(int(round(pt[0])), img_shape[1] - 1)
        y = min(int(round(pt[1])), img_shape[0] - 1)
        
        pt2d = np.zeros(img_shape, dtype=np.float32)
        pt2d[y, x] = 1.0

        if gt_count > 3:
            # sigma = 0.3 * khoảng cách trung bình đến 3 láng giềng
            sigma = (distances[i][1] + distances[i][2] + distances[i][3]) * 0.1
        else:
            sigma = np.average(np.array(img_shape)) / 4.0

        density += scipy.ndimage.gaussian_filter(pt2d, sigma, mode='constant')

    return density

def gaussian_filter_density_fixed(gt_pts, img_shape, sigma=15.0):
    """
    Sinh density map cho Part B (cảnh thưa thớt) bằng Gaussian Kernel cố định (sigma=15)
    """
    density = np.zeros(img_shape, dtype=np.float32)
    for pt in gt_pts:
        x = min(int(round(pt[0])), img_shape[1] - 1)
        y = min(int(round(pt[1])), img_shape[0] - 1)
        pt2d = np.zeros(img_shape, dtype=np.float32)
        pt2d[y, x] = 1.0
        density += scipy.ndimage.gaussian_filter(pt2d, sigma, mode='constant')
    return density

def process_image(img_path, mat_path, part_name):
    """
    Xử lý 1 ảnh: đọc ảnh, đọc mat, sinh density map, resize 1/8 và lưu file .h5
    """
    h5_path = img_path.replace('.jpg', '.h5')
    
    # Nếu file .h5 đã tồn tại, bỏ qua để tiết kiệm thời gian
    if os.path.exists(h5_path):
        return True, 0, 0

    # Đọc ảnh
    img = Image.open(img_path).convert('RGB')
    w, h = img.size

    # Đọc nhãn Matlab .mat
    mat = io.loadmat(mat_path)
    # Cấu trúc của ShanghaiTech: mat["image_info"][0, 0][0, 0][0] chứa danh sách tọa độ (x, y)
    gt_pts = mat["image_info"][0, 0][0, 0][0]
    actual_count = len(gt_pts)

    # Sinh density map
    if "part_A" in part_name:
        density = gaussian_filter_density_adaptive(gt_pts, (h, w))
    else:
        density = gaussian_filter_density_fixed(gt_pts, (h, w), sigma=15.0)

    # Co tỉ lệ 1/8 và nhân 64 để bảo toàn tích phân số lượng người
    density_1_8 = cv2.resize(
        density,
        (int(w // 8), int(h // 8)),
        interpolation=cv2.INTER_CUBIC
    ) * 64.0

    # Lưu vào file HDF5 (.h5)
    with h5py.File(h5_path, 'w') as h5f:
        h5f.create_dataset('density', data=density_1_8)

    computed_count = float(np.sum(density_1_8))
    return False, actual_count, computed_count

def process_dataset_split(base_dir, part_name, split_type):
    """
    Quét thư mục train_data hoặc test_data, gọi hàm xử lý và trả về danh sách ảnh
    """
    split_dir = os.path.join(base_dir, part_name, split_type)
    img_dir = os.path.join(split_dir, 'images')
    gt_dir = os.path.join(split_dir, 'ground-truth')

    img_paths = sorted(glob.glob(os.path.join(img_dir, '*.jpg')))
    print(f"\n--- Đang xử lý {part_name} | {split_type} ({len(img_paths)} ảnh) ---")

    for i, img_path in enumerate(img_paths):
        fname = os.path.splitext(os.path.basename(img_path))[0]
        mat_path = os.path.join(gt_dir, f"GT_{fname}.mat")

        if not os.path.exists(mat_path):
            print(f"[CẢNH BÁO] Không tìm thấy file nhãn: {mat_path}")
            continue

        skipped, actual_cnt, comp_cnt = process_image(img_path, mat_path, part_name)
        if (i + 1) % 50 == 0 or (i + 1) == len(img_paths):
            if skipped:
                print(f"[{i + 1}/{len(img_paths)}] Đã có sẵn .h5, bỏ qua.")
            else:
                print(f"[{i + 1}/{len(img_paths)}] Xử lý: {fname} | Số người thật: {actual_cnt} | Tích phân h5: {comp_cnt:.2f}")

    return img_paths

def main():
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Crowd_Counting_ShanghaiTech', 'ShanghaiTech')
    print(f"Thư mục gốc Dataset: {root_dir}")

    if not os.path.exists(root_dir):
        print("Lỗi: Không tìm thấy thư mục ShanghaiTech!")
        return

    # 1. Xử lý Part A
    part_a_train = process_dataset_split(root_dir, 'part_A', 'train_data')
    part_a_test = process_dataset_split(root_dir, 'part_A', 'test_data')

    # Chia Part A Train thành Train (90%) và Val (10%)
    random.shuffle(part_a_train)
    val_len_a = int(len(part_a_train) * 0.1)
    a_val_list = part_a_train[:val_len_a]
    a_train_list = part_a_train[val_len_a:]

    # Xuất các file JSON cho Part A
    with open('part_A_train.json', 'w') as f:
        json.dump(a_train_list, f, indent=4)
    with open('part_A_val.json', 'w') as f:
        json.dump(a_val_list, f, indent=4)
    with open('part_A_test.json', 'w') as f:
        json.dump(part_a_test, f, indent=4)
    print("=> Đã tạo thành công: part_A_train.json, part_A_val.json, part_A_test.json")

    # 2. Xử lý Part B
    part_b_train = process_dataset_split(root_dir, 'part_B', 'train_data')
    part_b_test = process_dataset_split(root_dir, 'part_B', 'test_data')

    # Chia Part B Train thành Train (90%) và Val (10%)
    random.shuffle(part_b_train)
    val_len_b = int(len(part_b_train) * 0.1)
    b_val_list = part_b_train[:val_len_b]
    b_train_list = part_b_train[val_len_b:]

    # Xuất các file JSON cho Part B
    with open('part_B_train.json', 'w') as f:
        json.dump(b_train_list, f, indent=4)
    with open('part_B_val.json', 'w') as f:
        json.dump(b_val_list, f, indent=4)
    with open('part_B_test.json', 'w') as f:
        json.dump(part_b_test, f, indent=4)
    print("=> Đã tạo thành công: part_B_train.json, part_B_val.json, part_B_test.json")

    print("\n=======================================================")
    print("HOÀN THÀNH TIỀN XỬ LÝ TOÀN BỘ TẬP DỮ LIỆU!")
    print("=======================================================")

if __name__ == '__main__':
    main()

