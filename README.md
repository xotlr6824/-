# 주제

## opencv / openpose / teachable machine / tensorflow를 이용한 헬스 자세교정 및 골프 스윙 경로 추적

### 2016104103 컴퓨터공학과 곽태식

* 사양

    - MacBook m1 pro 32GB 1TB
    - macOS Monterey 12.4
    - Miniforge 3
    - Python 3.9
    - TensorFlow 2.8.0

# 프로젝트 목적

헬스의 팔 각도, 골프의 스윙 경로를 추적하여 사용자 스스로 확인하여 보완, 발전 할 수 있도록 돕고자 한다.

# 1. Health_degree

 ## 프로그램 및 모듈 설치
 
1.1 OpenPose 설치

 [공식링크](https://github.com/CMU-Perceptual-Computing-Lab/openpose) 에서 다운받는다.
 
    # [models] 폴더에 있는 getmodels.sh 파일 실행 /windows 환경이라면 getmodels 파일 실행
    
    # caffemodel 다운로드 확인
  
 다운로드가 확인되면 코드내에서 protxt, caffemodel 파일 경로를 설정해주면 된다.
 
 골반과 발 관절이 추가된 body25 모델을 사용하였다.
 
 mpii - 15개 / coco - 18개 / body25 - 25개
 
1.2 모듈 설치

    $ pip install opencv-python
    $ pip install math

 ## 실행 화면
 
  덤벨 숄더 프레스 운동을 한다는 과정에서 작성한 코드이다.
  
  
  ![img](https://user-images.githubusercontent.com/48917101/174013376-98a25f90-a4cb-43be-b559-97292b127541.png)

  
  
  
  openpose 관절 포인트를 잡는다.
  
  팔꿈치와 손목의 각도를 math로 측정하여 70도 보다 작으면 덜 펴진것으로 판단한다.
  
  덜 펴졌을 경우 빨간색 선으로 나타내어 잘못된 자세임을 인지시킨다.


https://user-images.githubusercontent.com/48917101/174031698-de5ec5cb-1335-4d32-bed4-1e91a005dc8d.mp4


opencv의 gpu 지원이 중단되면서 실시간으로 영상을 인퍼런스 하는 과정에서 cpu만으로 데이터 계산을 하기 때문에 프레임 드랍 현상이 있다.


실시간영상을 확인할 때 UX 차원의 답답함을 개선하고자 동작영상을 따로 인코딩하여 저장하는 방식을 추가하였다.

    #Health_degree_recod.py

 ## 결과
 
 팔, 손목 뿐 아니라 운동의 종류에 맞게 각도를 설정하면 여러가지 운동에 적용할 수 있을 것으로 보인다.

# 2. Golf_Tracking

 ## 프로그램 및 모듈 설치

1.1 m1 pro TensorFlow2.x 설치
  
  apple silicon(m1)의 지원이 완벽하지 않아 miniforge의 설치가 필요하다.

  [공식링크](https://github.com/conda-forge/miniforge/) 에서 다운받는다.
  
        $ cd downloads
        $ bash Miniforge3-MacOSX-arm64.sh
  
  ### 가상환경 생성
  
    $ conda create -n [가상환경이름] python=[파이썬버전]
    
  ### 가상환경 활성화
  
    $ conda activate [가상환경이름]
  
  ### tensorflow 설치
  
    $ conda install -c apple tensorflow-deps -y
    
    # python 설치
    $ python -m pip install tensorflow-macos
    
    # tensorflow plugin 설치
    $ pip install tensorflow-metal
    
  ### VSCode 가상환경 연동
  
   vscode 터미널에서 명령어 입력  
   
    conda activate [가상환경이름]
    
   가상환경 나올 때
   
    conda deactivate [가상환경이름]
    
1.2 모듈 설치


        $ pip install opencv-python
        
        $ pip install numpy


# 실행화면

스윙을 추적하기 위해 blue색상을 검출하여 추적하는 방법을 사용하였다.



https://user-images.githubusercontent.com/48917101/174069710-55963f27-2d4c-486d-a4a7-c688ebccfb3b.mp4


이를 바탕으로 골프채 헤드부분에 파란색 천을 감싸 진행하였다.


teachable machine으로 골프 스윙 경로를 시작할 시점을 판단할 모델을 만들었다.

pose model은 json파일만 지원을 하여 image model로 생성하였다.

    #모델
    
    0:swing

    1:swing finish // 스윙경로 지울 시점

    2:swing start // 스윙경로 생성 시점


https://user-images.githubusercontent.com/48917101/173853618-1ae59bf1-ab60-422a-9fbf-6cecd48d9dc8.mp4


model 생성 후 swing start라 예측되면 파랑색을 추적하여 경로를 그리게 된다.

스윙 후 finish라 판단되면 경로를 지우고 돌아간다.

https://user-images.githubusercontent.com/48917101/173851027-ea5f25ea-b85c-4535-979a-d29c8ffc988b.mp4



## 결과

swing판단을 할 때 image model을 사용했기 때문에 주변 환경의 영향이 있을 것으로 보인다.

또한 색상검출을 사용하여 tracking을 하기 때문에 추정색이 없는 환경이 필요하다.

따라서 골프연습장 같은 주변 환경의 변화가 없는 공간에서 유의미한 결과를 얻을 것으로 보여진다.






