# 주제

opencv / openpose / teachable machine / tensorflow를 이용한 헬스 자세교정 및 골프 스윙 경로 추적

### 2016104103 컴퓨터공학과 곽태식

* 사양

    - MacBook m1 pro 32GB 1TB
    - macOS Monterey 12.4
    - Miniforge 3
    - Python 3.9
    - TensorFlow 2.8.0

# 프로젝트 목적

헬스의 팔 각도, 골프의 스윙 경로를 추적하여 사용자 스스로 확인하여 보완, 발전 할 수 있도록 돕고자 한다.


#프로그램 및 모듈 설치

1. m1 pro TensorFlow2.x 설치
  
  apple silicon(m1)의 지원이 완벽하지 않아 miniforge의 설치가 필요하다.

  [공식링크](https://github.com/conda-forge/miniforge/) 에서 다운받는다.
  
        $ cd downloads
        $ bash Miniforge3-MacOSX-arm64.sh

# 실행화면

teachable machine으로 골프 스윙 경로를 시작할 시점을 판단할 모델을 만들었다.

pose model은 json파일만 지원을 하여 image model로 생성하여 아쉬운 점이 있다.

    0:swing

    1:swing finish // 스윙경로 지울 시점

    2:swing start // 스윙경로 생성 시점

https://user-images.githubusercontent.com/48917101/173853618-1ae59bf1-ab60-422a-9fbf-6cecd48d9dc8.mp4


model 생성 후 swing start라 예측되면 파랑색을 추적하여 경로를 그리게 된다.

스윙 후 finish라 판단되면 경로를 지우고 돌아간다.

# 결과

https://user-images.githubusercontent.com/48917101/173851027-ea5f25ea-b85c-4535-979a-d29c8ffc988b.mp4

