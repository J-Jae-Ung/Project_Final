gaussian-splatting/
├── README.md             # 프로젝트 개요 및 설명
├── arguments/            # 명령줄 인수 관련 파일 디렉토리
│   ├── argument_file.txt # 명령줄 인수 예제 파일
├── assets/               # 프로젝트에 필요한 자산 파일 디렉토리
│   ├── asset_file.bin    # 자산 파일 예제
├── gaussian_renderer/    # Gaussian 렌더러 소스 코드 디렉토리
│   ├── renderer.cpp      # Gaussian 렌더러의 주요 구현 파일
│   ├── renderer.h        # Gaussian 렌더러의 헤더 파일
├── lpipsPyTorch/         # PyTorch용 LPIPS 코드 디렉토리
│   ├── lpips.py          # LPIPS 계산을 위한 Python 스크립트
├── scene/                # 장면 파일 디렉토리
│   ├── scene_file.txt    # 장면 파일 예제
├── submodules/           # 서브모듈 파일 디렉토리
│   ├── submodule_file.txt# 서브모듈 파일 예제
├── utils/                # 유틸리티 함수 디렉토리
│   ├── utility.py        # 유틸리티 함수 구현 파일
├── .gitignore            # Git에서 무시할 파일 목록
├── .gitmodules           # Git 서브모듈 설정 파일
├── convert.py            # 데이터 변환 스크립트
├── environment.yml       # Conda 환경 설정 파일
├── full_eval.py          # 전체 평가 스크립트
├── metrics.py            # 평가 메트릭스 계산 스크립트
├── render.py             # 렌더링 스크립트
└── train.py              # 모델 훈련 스크립트
