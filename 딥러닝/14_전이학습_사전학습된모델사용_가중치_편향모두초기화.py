# -*- coding: utf-8 -*-
"""14.전이학습_사전학습된모델사용_가중치_편향모두초기화.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16q9IaqO359q1rPQAF-T2eEZ5F5qXQFG1

# 개요
"""

from google.colab import drive
drive.mount('/content/drive')

"""- 성과가 잘 나온 모델을 가져온다
- 사전 학습된 W,b는 모두 초기화 한다
  - 모델이 학습한 데이터와, 내 데이터가 다르므로 초기화했다
- 현재 남은것은 네트워크만 있을것이다
- 새로운 데이터를 넣고, 가중치도 초기화값 세팅 학습 진행
- 신경망 구조만 사용하고, 가중치는 내가 직접 훈련해서 세팅하겟다
- 예측
  - **정확도가 떨어질듯 하고, 많은 훈련시간이 필요할듯 하다**

# 데이터 준비

- 케글에서 제공되는 데이터 활용



```
# 패키지 설치
!pip install kaggle

# 환경변수
import os

os.envrion['KAGGLE_USERNAME'] = '이름'
os.envrion['KAGGLE_KEY'] = '인증키'

# 다운로드
!kaggle competitions download -c 경쟁부분이름
```
"""

import tensorflow as tf
tf.__version__

# 인터넷상의 자료를 받아서 로컬 PC에 원하는 위치에 바로 저장
#tf.keras.utils.get_file('/content/labels.csv', '링크')

"""# 데이터 확인 및 준비

## 정답 데이터
"""

import pandas as pd

#label = pd.read_csv('/content/labels.csv')
#label.shape

#label.head()
# id는 이미지 파일명, breed는 해당 이미지의 품종/견종

#label.info()
# 결측치가 없다

# 견종의 총 종류수
#len( label.breed.unique() )

"""## 훈련데이터 확인"""

#!tar -xvf /content/drive/MyDrive/k-디지털-품질재단/딥러닝/dog_cat_data/images.tar

"""# 정답 데이터 생성"""

# 정답 레이블 생성 코드
fDir = '/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/res/dog_cat_data/Images'
import os

labels = list()
for dir in os.listdir(fDir):
  # 종의 이름
  dog_type = '-'.join(dir.split('-')[1:])
  # 경로, 종의이름
  #print( dir, dog_type )
  # 해당 종의 하위 폴더로 이동
  for f in os.listdir( os.path.join( fDir, dir) ):
    #print( f )
    # 파일의 이름 추출, 단 모든 파일은 .jpg로 끝난다(전제)
    name = f.split('.')[0]
    data = f'{dir},{name},{dog_type}\n'
    #print( data )
    labels.append( data )
    #break
  #break

len( labels )

with open('new_labels.csv', 'w') as f:
  f.write( 'dir,name,label\n'+ ''.join(labels) )

"""# 전이학습 진행

## 사전학습된 모델 획득
"""

from tensorflow.keras.applications import MobileNetV2
mobilev2 = MobileNetV2()

"""## 가중치 초기화"""

# 전체 layers 수
len( mobilev2.layers ) 
# 156 layer 사용

mobilev2.summary()

from tensorflow.python.ops.variables import model_variables
# 이 모델은 출력층에서 분류하는 값이 1000개 중에 하나를 분류
# 이 프로젝트는 120개 중에 하나를 분류하는 미션
# 훈련 가능한 형태로 layer를 조정 => 1000개로 출려되는 부분  제거
for layer in mobilev2.layers[:-1]:
  # 해당층이 훈련 가능한가?  
  layer.trainable = True
# 마지막층을 제외하고 모든층은 다시 훈련할수 있게 조정

import numpy as np
# 가중치, 커널 초기화
for layer in mobilev2.layers[:-1]:
  # 레이어를 구성하는 성분들 중에 
  if 'kernel' in layer.__dict__: # 커널이 있다면 => 합성곱층이면
    # 현재 커널의 shape 획득
    kernel = np.array( layer.get_weights() ).shape
    # 평균이 0, 표준편차가 1인 정규분포를 가진 난수값을 W로 가진
    # 커널을 생성해서 새로 세팅한다 => 초기화 했다
    layer.set_weights( tf.random.normal( kernel, 0, 1 ) )

"""## 훈련 데이터 전처리-부풀리기

- 데이터가 부족할때 사용(이미지)
- 이미지 데이터 라면
  - 이미지 부풀리기
    - 자르기, 회전하기, 뒤틀리기, 반전, 왜곡,.... => 생각보다 정확도가 높아지진 않는다
  - GAN을 통해서 생성하기
"""

import pandas as pd
import cv2
# 이미지 리사이징 처리에 활용
# 이미지 원재료 그대로 리사이징 하면 이미지가 깨진다
# 특정 부위만 필요로 한다면, 
# 바운딩박스를 표시 -> 해당 부분만 컷 -> 리사이징

label = pd.read_csv('/content/new_labels.csv')
label.head(2)

label.loc[0, 'dir'], label.loc[0, 'name']

train_X = list()
for i in range(1000): # 파일목록개수): # <- 나중에 파일이 다 업로드되면 교체
  dir   = label.loc[i, 'dir']
  name  = label.loc[i, 'name']
  fName = f'/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/res/dog_cat_data/Images/{dir}/{name}.jpg'

  # 1. 이미지 읽기
  img = cv2.imread( fName )
  #print( img.shape ) # (500, 333, 3) => 3채널(칼라), 크기는 다양하다

  # 2. cv2 제공 함수를 통해서 리사이징 => (224,224)
  img = cv2.resize( img, dsize=(224,224) )
  #print( img.shape ) # 이미지상에서 대상(객체)를 고려하지 않고 리사이즈 진행
  #    이미지 손상이 많을것으로 예상됨.

  # 3. 정규화 -> 3채널, 1채널 관계없이 개별성분을 255로 나눠서 처리
  #print( img[0][0] )
  img = img / 255.0
  #print( img[0][0] )

  # 4. 훈련용 데이터로 추가 
  train_X.append( img )
  #break

"""## 정답 데이터 전처리 """

# 정답에서 중복제거 공유한값만 리스트로 묶어서 확인
unique_label = label.label.unique().tolist()
print( unique_label[:10] )
# 정확도를 높이기 위해 정답을 원-핫인코딩 혹은 문자열 인덱스를 이용 수치화
train_y = [ unique_label.index(name) for name in label.label ]
# 텍스트로 준비된 정답값은 수치로 변경(인덱스)
train_y = np.array( train_y )
train_y[:10], train_y[-10:]

"""## 모델에 적용하여 전이학습-실제학습 진행

- 전이 학습용 모델 + 새로운 구조를 추가(후반부 작업)
  - 기존 모델은 156층
  - 마지막 2개층 flattern->y에 수렴하는 구조
  - 후반 수렴지점을 교체해서 처리
"""

# 교체 지점 획득
x        = mobilev2.layers[-2].output
# 기존모델 flattern 단계에서 마지막에 120개 백터를 가진 층으로 수렴
# 출력층 교체
preModel = tf.keras.layers.Dense( 120, activation='softmax' )( x )
# 모델획득(입력와 출력을 새로세팅)
model    = tf.keras.Model( inputs=mobilev2.input, outputs=preModel )

# 컴파일(실행)
model.compile( optimizer='sgd', loss='sparse_categorical_crossentropy', 
               metrics=['accuracy'])
model.summary()

train_X = np.array( train_X )
train_X.shape

train_y[:1000].shape

# 학습
hist = model.fit( train_X, train_y[:1000], epochs=10, 
                  validation_split=0.25, batch_size=32 )