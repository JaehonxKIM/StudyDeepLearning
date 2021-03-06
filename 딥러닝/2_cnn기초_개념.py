# -*- coding: utf-8 -*-
"""2.  CNN기초 개념.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zmWmwvXGXgUb5thwCTa-kOHxuvh12RnH

# CNN 개요

- 사람이 눈을 통해 사물을 인지하는 절차를 그대로 적용하여 만든 인공신경망 혹은 네트워크 구조이다 
- 합성곱 인공 신경망
  - Convolution Netual Network(CNN)
- History
  - 1989 : Lecun 논문에서 개념 발표
  - 2006 : CNN을 일반화한 논문 발표
  - 2012 : AlexNet을 통해 구현
    - 영상처리 / 분류 / 인식 분야의 가장 기본적인 성능을 제시
    - 이후는 이를 기반한 파생 네트워크들이 주류로 등장

# 네트워크 구조(신경망의 구조)

- ANN

```
입력층
은닉층(중간층)
출력층
```

- DNN(심층 인공신경망)


```
입력층
은닉층(중간층)
...
은닉층(중간층)
출력층
```

- CNN(합성곱층 인공신경망)
  - 은닉층을 사물인식 단계의 특성을 적용하여 설계

```
입력층
은닉층(중간층)
  L 합성곱층 -> 이미지 공간 상의 특징 추출
  L 풀링층   -> 그렇게 나온 특징을 강화하는 단계
  L 합성곱층
  L 풀링층
  L 합성곱층
  L 풀링층
  ...
  L 전결합층 => 이 이미지는 무엇보다 분류하기 위해 1차원으로 flattern 해준다(수렴)
출력층 => 최종 분류형태로 수렴
```

# 원리 및 특징

- 이미지 관점
  - 이미지 내에 공간 정보를 특징으로 추출하고 학습
  - 이미지 내의 인접정보를 특징으로 추출하고 학습
  - 이것을 수행하기 위해서 해당 정보를 추출하기 위해서 특정 크기의 기준이 필요 => 커널 혹은 필터라고 부름 => 이 커널에는 W가 세팅되어 있다

- 예시
  - 커널 크기가 (3, 3)
  - 정사각형 커널
  - 이미지 공간상에서 왼쪽 상단부터 오른쪽으로 이동해 가면서 정보를 추출

# 입력층

- 원본 이미지 데이터 입력
- 데이터를 설계된 shape에 맞게 크기를 조정
- 원본 크기가 제각각이면 전처리 통해서 조정
  - opencv 같이 활용
- 데이터는 다음과 같은 shape을 가짐
  - (?, x1,x2,x3,...)
  - 2D-Tensor 형태가 유력(2D 이미지)

# 은닉층

## 합성곱층(이미지상의 공간정보, 인접정보 등 특징 추출)
"""

from IPython.display import Image
Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/dl/cnn2.png')
# 합성곱층이 가중치(W)를 파라미터로 가진 필터(커널K)를 스트라이드(S)하면서 
# 슬라이딩하면 특징을 뽑는다 => 이것을 모아두면 Feature map이 된다

"""### 합성곱층의 구성요소

- ***입력 (x)***
  - 이전 층에서 나오는 최종 산출물
    - 최초 입력층, 전 단계의 풀링층, 전단계의 과적합방지층
    - shape 기억

- ***커널 (k)***
  - 이미지 공간 / 인접 상의 특징을 추출할 때 그 경계 크기
  - 특징을 추출하기 위해서 값이 존재 -> 변경 -> 파라미터 -> 실체는 W
  - 행렬
  - 가중치를 파라미터로 가지는 커널(필터)
    - 수직커널, 수평 커널, 가우시안 커널...
    - 통계적인 함수를 대입
    - 랜덤값을 넣을 수도 있음
  - ***편향***(커널을 이용해 이미지 원본데이터에서 특징을 추출하고 나서 편향값을 적용할 수 있다

- ***스트라이드 (s)***
  - STRIDE
  - 커널이 이미지 원본 상에서 슬라이딩을 하며 이동할 때 그 크기를 지정
  - 이동량
  - 왼쪽에서 오른쪽, 위에서 아래로 

- ***패팅 (p)***
  - 커널이 스트라이드 값에 의해 슬라이딩하는 중에 경계선을 넘어갈 수 있다
  - 이런 경우, 패딩을 적용하여 이미지 외곽을 통상 0으로 채워서 특징을 추출할 수 있게 보완함

- ***출력***
  - feature map : 특징을 정보로 가진 맵
  - activation map : 활성화 함수를 통과한다면 활성화 맵
"""

Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/dl/cnn1.png')

Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/dl/cnn3.png', width = 500)
# 입력 데이터에 필터가 적용되어 특징이 뽑히는 전 과정

Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/dl/cnn4.png')
# 흑백, grayscale 이미지는 1 channel
# 컬러이미지는 3channel
# 채널이 많은 경우 각각 채널별로 추출해서 특징을 합산 => 최종 결과 추출

Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/dl/cnn5.jpeg')
# 패딩의 예시
# SAME :  커널이 정보 추출 후 특징맵의 크기가 원본과 동일(stride가 1인 경우)
# VALID : 커널이 정보 추출 후 특징맵의 크기가 원본보다 작아짐(stride가 1인 경우)

Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/dl/cnn6.png')
# 0으로 일반적으로 채우고 1칸이 아닌 2칸 이상도 채울 수 있다

"""## 풀링층(특징을 강화)

- 역할
  - 풀링층으로 들어오는 입력 데이터의 강화하는 목적(특징맵, 활성화맵)
  - 특징 강화
  - 기법
    - 최대 풀링
    - 평균 풀링
    - xxx
  - 커널을 이동시키면서 풀링 처리를 해야 하는데, 이미 풀링의 목표가(최대, 평균,...) 정해져 있어 W가 필요없다
"""

Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/dl/cnn7.jpeg', width = 500)
# 풀링은 설계에 따라 이미지 원본 크기가 줄어들 수 있다
# s, p값에 따라 크기는 달라진다

Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/dl/cnn8.jpeg', width = 600)

"""## 전결합층

- 결과에 수렴하기 위한 중간단계, 완충단계
"""

Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/dl/cnn9.png')
# 전결합층 전까지는 특징 추출단계, 이후는 분류 단계로 구분된다
# Flattern 처리를 하고 1차원 백터로 펴주는 단계(선형으로 수렴하는 단계)
# 최종 결과 출력층에 연결되는 층

"""# 출력층

- 입력데이터는 x = 3이다 => 분류(인식)
- 1일 확률 5%, 2일 확률 3%, 3일 확률 69%...
- 가장 높은 확률(np.argmax())에 의해 이 이미지는 3이다 예측
- 입력데이터를 특정 값에 수렴하는 단계
"""