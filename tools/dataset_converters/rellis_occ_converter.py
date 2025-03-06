from os import path as osp
from pathlib import Path
from glob import glob
import mmengine

# 시퀀스 04의 총 프레임 수 (예시)
total_frames_seq4 = 61

# 사용할 시퀀스 (예: 시퀀스 04만 사용)
used_sequences = [4]

def find_camera_img(seq_str, frame_str):
    """
    지정한 시퀀스(seq_str)와 프레임 번호(frame_str)에 해당하는 카메라 이미지 파일을 찾습니다.
    파일명은 'frame{frame_str}*' 형태로 glob 검색을 진행합니다.
    """
    # data_root를 절대경로로 검색한 뒤 data_root에 대한 상대 경로를 반환하도록 함.
    data_root = '/media/spalab/sdb/dhkim/OCCFusion/data'
    camera_dir = osp.join(data_root, 'sequences', seq_str, 'camera')
    pattern = osp.join(camera_dir, f"frame{frame_str}*")
    files = glob(pattern)
    if files:
        abs_img_path = files[0]
        rel_img_path = osp.relpath(abs_img_path, data_root)
        return rel_img_path
    else:
        print(f"[Warning] No camera image found for sequence {seq_str}, frame {frame_str}")
        return ""

def get_occfusion_info():
    """
    OCCFusion 데이터셋의 info 파일을 생성하는 함수.
    
    생성되는 정보의 형식은 SemanticKITTI와 유사하게 구성됩니다.
    
    각 샘플은 아래와 같이 구성됩니다.
    
        {
            'lidar_points': {
                'lidar_path': 'sequences/04/lidar/000000.bin'
            },
            'pts_semantic_mask_path': 'sequences/04/labels/000000.label',
            'img_path': 'sequences/04/camera/frame000000-1581791678_408.jpg',
            'calib': {
                 'transforms_path': 'sequences/04/transforms.yaml',
                 'camera_info_path': 'sequences/04/camera_info.txt',
                 'calib_txt_path': 'sequences/04/calib.txt'
            },
            'sample_id': '04'
        }
    
    최종 결과 info 파일은 data_infos 딕셔너리에 저장됩니다.
    """
    data_infos = {}
    data_infos['metainfo'] = {'DATASET': 'OCCFusion'}
    
    data_list = []  # 각 샘플 정보를 담은 리스트
    
    # data_root는 info 파일 내 상대 경로 기준
    data_root = '/media/spalab/sdb/dhkim/OCCFusion/data'
    
    for seq in used_sequences:
        # 시퀀스 번호를 2자리 문자열로 변환 (예: '04')
        seq_str = str(seq).zfill(2)
        for frame in range(total_frames_seq4):
            frame_str = str(frame).zfill(6)  # 예: '000000', '000001', ...
            sample_info = {
                'lidar_points': {
                    'lidar_path': osp.join('sequences', seq_str, 'lidar', frame_str + '.bin')
                },
                'pts_semantic_mask_path': osp.join('sequences', seq_str, 'labels', frame_str + '.label'),
                'img_path': find_camera_img(seq_str, frame_str),
                # 시퀀스별 캘리브레이션 정보 (transforms.yaml, camera_info.txt, calib.txt)
                'transforms_path': osp.join('sequences', seq_str, 'transforms.yaml'),
                'camera_info_path': osp.join('sequences', seq_str, 'camera_info.txt'),
                'calib_txt_path': osp.join('sequences', seq_str, 'calib.txt'),
                'sample_id': seq_str  # SemanticKITTI 포맷에 따라 sample_id는 시퀀스 번호 사용
            }
            data_list.append(sample_info)
    
    data_infos['data_list'] = data_list
    print(data_infos)
    return data_infos

def create_occfusion_info_file(pkl_prefix, save_path):
    """
    OCCFusion 데이터셋의 info 파일을 생성하여 저장하는 함수.
    
    저장되는 pkl 파일 이름은 예: '{pkl_prefix}_infos_train.pkl'
    """
    print('Generate OCCFusion info file.')
    save_path = Path(save_path)
    
    occfusion_infos = get_occfusion_info()
    filename = save_path / f'{pkl_prefix}_infos_train.pkl'
    mmengine.dump(occfusion_infos, filename)
    print(f'OCCFusion info file is saved to {filename}')

if __name__ == '__main__':
    create_occfusion_info_file(pkl_prefix='occfusion', save_path='./data_infos')
