# Self-supervised learning Traversability Estimation

## 설치방법 (Linux)

directory 생성
```
mkdir $[디렉토리명}
cd $[디렉토리명}
git clone https://github.com/daehunkim1029/Trav_SSL.git
```
docker image 생성

```
docker pull pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime
```

docker container 생성

```
docker run -it --gpus all --shm-size=512g -v ${서버 데이터 경로}:${원하는 경로} -w ${디렉토리 경로} --name ${container 명} pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime /bin/bash
ex) docker run -it --gpus all --shm-size=512g   -v /media:/media  -v /mnt:/mnt -w /media/spalab/sdb/dhkim/OCCFusion   --name dh_occ   pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime   /bin/bash
```

docker container 접속

```
docker exec -it ${컨테이너명} /bin/bash
```

다음 명령어 입력

```
pip install -U openmim
mim install mmengine
mim install 'mmcv>=2.0.0rc4'
mim install 'mmdet>=3.0.0'
mim install "mmdet3d>=1.1.0"
pip install "mmsegmentation>=1.0.0"

pip install focal_loss_torch

apt-get update
apt-get install -y libgl1-mesa-glx
apt-get install -y libglib2.0-0

pip install pykitti
pip install timm
```

데이터 생성

```
mkdir -p data/Rellis-3D
```

체크포인트 경로

```
mkdir ckpt
wget https://github.com/zhiqi-li/storage/releases/download/v1.0/r101_dcn_fcos3d_pretrain.pth

0.pth.tar, 1.pth.tar, 2.pth.tar 의 경우 15번 서버 /media/spalab/sdb/dhkim/OCCFusion/ckpt/0.pth.tar 에 존재함
```
```
sensor_failure_detection
├─ ckpt
│  ├─r101_dcn_fcos3d_pretrain.pth
│  └─ 0.pth.tar
|  └─ 1.pth.tar
|  └─ 2.pth.tar

├─ data
├─ occfusion
└─ tools
```


훈련 모델 실행 (예시)

```
bash tools/dist_train.sh configs/OccFusion_semanticKITTI.py  1 --amp  4

```
