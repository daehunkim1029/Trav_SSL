import numpy as np
import open3d as o3d
import argparse

def load_label_file(label_file):
    """
    .label 파일을 읽어, 각 행이 [x, y, z, label]인 numpy 배열로 반환합니다.
    """
    try:
        # dtype과 reshape은 파일 포맷에 맞게 조절 (여기서는 int32로 가정)
        data = np.fromfile(label_file, dtype=np.int32).reshape(-1, 4)
    except Exception as e:
        print(f"[Error] Failed to load label file: {e}")
        data = np.empty((0, 4), dtype=np.int32)
    return data

def visualize_voxel_labels(label_data, voxel_size=0.2):
    """
    label_data: (N,4) 배열로, 각 행 [x, y, z, label] 형태.
    voxel_size: 각 voxel(박스)의 크기.
    """
    # 예시 컬러 매핑 (필요에 따라 수정)
    label_color_mapping = {
        0: [0.8, 0.8, 0.8],   # unknown/empty: 회색
        1: [0, 1, 0],         # 예: 안전 -> 초록색
        2: [1, 1, 0],         # 예: 주의 -> 노란색
        3: [1, 0, 0],         # 예: 위험 -> 빨간색
        # 추가 라벨에 대한 컬러 매핑 필요시 여기에 추가
    }
    default_color = [0, 0, 0]  # 매핑되지 않은 라벨은 검은색

    voxel_meshes = []
    for point in label_data:
        x, y, z, label = point
        color = label_color_mapping.get(label, default_color)
        
        # voxel(박스)를 생성 (기본 위치는 원점)
        box = o3d.geometry.TriangleMesh.create_box(width=voxel_size,
                                                   height=voxel_size,
                                                   depth=voxel_size)
        # 박스 중심이 (x,y,z)가 되도록 translation 조정
        box.translate((x - voxel_size / 2, y - voxel_size / 2, z - voxel_size / 2))
        box.paint_uniform_color(color)
        voxel_meshes.append(box)
        
    if not voxel_meshes:
        print("No voxel data to display.")
        return

    # 모든 박스를 하나의 리스트로 합쳐서 시각화
    o3d.visualization.draw_geometries(voxel_meshes, window_name="Voxel Labels Visualization")

def main():
    parser = argparse.ArgumentParser(
        description="Visualize .label file containing [x, y, z, label] per voxel."
    )
    parser.add_argument("--label_file", type=str, help="Path to the .label file")
    parser.add_argument("--voxel_size", type=float, default=0.2, help="Voxel size for visualization")
    args = parser.parse_args()
    
    label_data = load_label_file(args.label_file)
    print(f"Loaded {label_data.shape[0]} voxels from {args.label_file}")
    visualize_voxel_labels(label_data, args.voxel_size)

if __name__ == "__main__":
    main()
