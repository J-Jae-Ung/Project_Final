
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




# Installation Tutorial For Gaussian Splatting

| **Total file size** | **7GB** |
|---|---|
|**VRAM**|**24GB**|

## step 1: setting up the environment

Install [Pinokio](https://pinokio.computer/), we wrote a pinokio file where you **just need 1 click to install all of the dependencies**. 
Then open up Pinokio, go to the top right button "Discover" 
Copy the link of this repository, paste the link at the side that says "enter git URL"
And press download
You can find "Project_Final.git" in your Pinokio list (if you didn't change the save name). 
Press **Install** to download all the dependencies in a conda env

## step 2: Structure from Motion (SfM) with COLMAP

### Extra step for inputs that are videos
This step is for custom inputs. If you have a video, please extract it into image frames. This can be done with FFMPEG. Below is a template for the ffmpeg command.
```
ffmpeg -i input_data/file.mp4 -r 1/1 input_data/$filename%03d.png
```

Now, with a collection of images of a scene, you would need to put the **set** of input images into the `input_data/<your_image_collection>/input` folder. Eg. `fern/input`

Taking 2 collections (fern and toy_truck) of input images as an example, below is the File Structure **requirements** before running `convert.py`. You would need to create these folders.
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

Now, using `fern` as an example, 
```
python convert.py -s input_data/fern --colmap_executable COLMAP-3.8-windows-cuda\COLMAP.bat
```
Below is the template:
```
python convert.py -s <your_input_dir> --colmap_executable COLMAP-3.8-windows-cuda\COLMAP.bat
```

## step 3: Train/optimize the images

This step is pretty straight forward, you just got to run the below command (using `fern` as an example):
```
python train.py -s input_data/fern
```
Below is the template:
```
python train.py -s <input_dir>
```

## step 4: View the result!
Go to the `output` folder, and you can see some randomly generated folder name. You can rename this to anything you want, like the scene name and the times it was ran.

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

So I'll rename mine from `a2973a46-9` -> `fern`

Now, using the below command with `fern` as an example, you can view it in 3D.
```
start viewers/bin/SIBR_GaussianViewer_app.exe . -m output\fern
```
Below would be a template
```
start viewers/bin/SIBR_GaussianViewer_app.exe . -m <output_folder>
```

## The tutorial ends here. 

