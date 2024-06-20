
## 파일 설명
- `README.md`: 프로젝트의 개요 및 사용법을 설명합니다.
- `arguments/`: 명령줄 인수와 관련된 파일들이 저장된 디렉토리입니다.
  - `argument_file.txt`: 명령줄 인수의 예제 파일입니다.
- `assets/`: 프로젝트에 필요한 자산 파일들이 저장된 디렉토리입니다.
  - `asset_file.bin`: 자산 파일의 예제입니다.
- `gaussian_renderer/`: Gaussian 렌더러의 소스 코드가 포함된 디렉토리입니다.
  - `renderer.cpp`: Gaussian 렌더러의 주요 구현 파일입니다.
  - `renderer.h`: Gaussian 렌더러의 헤더 파일입니다.
- `lpipsPyTorch/`: PyTorch를 사용하여 LPIPS를 계산하는 코드가 포함된 디렉토리입니다.
  - `lpips.py`: LPIPS 계산을 위한 Python 스크립트입니다.
- `scene/`: 장면 파일들이 저장된 디렉토리입니다.
  - `scene_file.txt`: 장면 파일의 예제입니다.
- `submodules/`: 서브모듈 파일들이 저장된 디렉토리입니다.
  - `submodule_file.txt`: 서브모듈 파일의 예제입니다.
- `utils/`: 유틸리티 함수들이 포함된 디렉토리입니다.
  - `utility.py`: 유틸리티 함수가 구현된 파일입니다.
- `.gitignore`: Git에서 버전 관리에서 무시할 파일 목록을 지정합니다.
- `.gitmodules`: Git 서브모듈 설정 파일입니다.
- `convert.py`: 데이터 변환을 위한 스크립트입니다.
- `environment.yml`: Conda 환경 설정 파일입니다.
- `full_eval.py`: 전체 평가를 위한 스크립트입니다.
- `metrics.py`: 평가 메트릭스를 계산하는 스크립트입니다.
- `render.py`: 렌더링을 위한 스크립트입니다.
- `train.py`: 모델 훈련을 위한 스크립트입니다.


# Gaussian Splatting 설치 튜토리얼

| **총 파일 크기** | **7GB** |
|---|---|
|**VRAM**|**24GB**|

## 1단계: 환경 설정

[Pinokio](https://pinokio.computer/)를 설치하세요. 우리는 Pinokio 파일을 작성했기 때문에 **한 번의 클릭으로 모든 종속성을 설치**할 수 있습니다. 
Pinokio를 열고, 오른쪽 상단의 "Discover" 버튼을 클릭하세요. 
이 저장소의 링크를 복사하여 "enter git URL" 옆에 붙여넣으세요. 
다운로드 버튼을 누르세요. 
Pinokio 목록에서 "Project_Final.git"을 찾을 수 있습니다 (저장 이름을 변경하지 않았다면). 
**Install**을 눌러 conda 환경에 모든 종속성을 다운로드하세요.

## 2단계: COLMAP을 사용한 Structure from Motion (SfM)

### 비디오를 입력으로 사용하는 경우 추가 단계
이 단계는 사용자 정의 입력에 해당합니다. 비디오가 있는 경우 이미지를 프레임으로 추출해야 합니다. FFMPEG를 사용하여 이 작업을 수행할 수 있습니다. 아래는 ffmpeg 명령의 템플릿입니다.

```
ffmpeg -i input_data/file.mp4 -r 1/1 input_data/$filename%03d.png
```



이제 장면의 이미지 모음을 `input_data/<your_image_collection>/input` 폴더에 넣어야 합니다. 예: `fern/input`

두 개의 이미지 모음(fern과 toy_truck)을 예로 들어, `convert.py`를 실행하기 전에 필요한 파일 구조는 아래와 같습니다. 이러한 폴더를 만들어야 합니다.
```
📂gaussian-splatting-Windows.git/ # this is root
├── 📂input_data/
│	├── 📂fern/
│	│	├── 📂input/
│	│	│	├── 🖼️image1.jpg
│	│	│	├── 🖼️image2.jpg
│	│	│	│...
│	├── 📂toy_truck/
│	│	├── 📂input/
│	│	│	├── 🖼️image1.jpg
│	│	│	├── 🖼️image2.jpg
│	│	│	│...
│ │...
│...
```

이제 `fern`을 예로 들어,
```
python convert.py -s input_data/fern --colmap_executable COLMAP-3.8-windows-cuda\COLMAP.bat
```
아래는 템플릿입니다::
```
python convert.py -s <your_input_dir> --colmap_executable COLMAP-3.8-windows-cuda\COLMAP.bat
```

## 3단계: 이미지 학습/최적화

이 단계는 매우 간단합니다. 아래 명령어를 실행하면 됩니다 (`fern`을 예로 들었습니다):


```
python train.py -s input_data/fern
```
아래는 템플릿입니다:
```
python train.py -s <input_dir>
```

## 4단계: 결과 보기!
`output` 폴더로 이동하면 무작위로 생성된 폴더 이름을 볼 수 있습니다. 이를 장면 이름이나 실행 횟수 등 원하는 이름으로 변경할 수 있습니다.


```
📂gaussian-splatting-Windows.git/ # this is root
├── 📂output/ 
│	├── 📂a2973a46-9/ <--
│ │	├── 📂point_cloud/
│ │	│	└── ...
│ │	├── 📜cameras.json/
│ │	├── 📜cfg_args/
│ │	└── 📜input.ply/
│ │...
│...
```


이제 제 폴더 이름을 `a2973a46-9`에서 `fern`으로 변경하겠습니다.

아래 명령어를 사용하여 `fern`을 예로 들어 3D로 볼 수 있습니다.

```
start viewers/bin/SIBR_GaussianViewer_app.exe . -m output\fern
```
Below would be a template
```
start viewers/bin/SIBR_GaussianViewer_app.exe . -m <output_folder>
```


## 튜토리얼 끝.

