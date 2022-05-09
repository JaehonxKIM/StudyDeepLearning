# -*- coding: utf-8 -*-
"""11. RNN_LSTM_Attention.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ile_dfTdLXf1S7VNV6Wt3oVdAitHx3AH
"""

from google.colab import drive
drive.mount('/content/drive')

"""# 개요

- 분장
  - 여러 개의 단어들로 구성이 되어있다
  - 다만, 문장의 의미를 정확하게 전달하기 위해서, 각 단어들이 어떤 **시퀀스(순서)로 배치**되고 전달 되었는가
  - 과거에 입력된 데이터와 최근에 입력된 데이터 간의 간계과 고려되어야 한다
  - 이를 처리하기 위해서는 기존 신경망으로 한계, **순환신경망이 고안되었다(Recurrent Netural Network, RNN)**

# 순환신경망

- RNN 원리
  - 여러 개의 데이터가 순서대로 입력되면, 앞에서 받은 데이터를 잠시 **기억**해 둔다 (**메모리**)
  - 기억한 데이터가 얼마나 **중요한지 판단**(저장된 내용의 중요도)
  - **별도의 가중치를 부여**하여 다음 데이터로 이동
  - 모든 데이터는 이 과정을 거친다
  - 이런 행위를 다른 각도로 보면 순환한것으로 보인다
"""

from IPython.core.display import Image
Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/RNN_NEW/RNNvs일반.png')

Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/RNN_NEW/rnn_단어처리1.png')

Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/RNN_NEW/rnn_단어처리2.png')

Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/RNN_NEW/RNN구조.png')

"""- RNN Cell
  - 기억을 해야 하는 메모리 셀을 빗대서 표현
  - 입력 2개
    - Xt
    - Ht-1
  - 출력 2개
    - Yt : 타입 step 1번째 출력
    - Ht : 타입 step 메모리의 출력값(h : Hidden 은닉층)
  - 총 길이 T(총 시간, 총 순서)만큼 타입 step이 순전파 방향으로 이동한다
  - 최종 출력
    - Yt = 활성화함수(Ht) + ...
    - 이 값이 손실함수에 전달되어 순환신경망의 순방향전파 완료

- RNN 장점 및 구조 특징

|구조|:--|
|--:|:--|
|one-to-one|- 일반적인 순방향 신경망 형태<br>- 문장을 읽고 의미를 파악할 때 사용|
|one-to-one|- 하나의 입력을 받고, 여러개의 출력을 생성<br>- 이미지 캡셔닝, 이미지를 설명하는 문장 생성|
|many-to-one|- 여러개를 입력받고, 하나의 출력을 생성<br>- 감정분류(Sentiment Classfication)|
|many-to-many|- case1 : 여러개를 입력 받고, 은닉층으로 정보를 취합후 여러개의 출력을 생성 (비대칭구조) : 기계번역<br>- case2 : 대칭적 구조, 영상의 여러 프레임을 입력받아서 어떤 내용인지 분류하는 방식<br>- 챗봇의 경우 중간 정도에 위치한다|
"""

Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/RNN_NEW/순환신경망의장점.png')

Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/RNN_NEW/rnn_case1.png', width = 500)

Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/RNN_NEW/rnn_case2.png', width = 500)
# # one to many : 이미지 캡셔닝 예시

Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/RNN_NEW/rnn_case3.png', width = 500)

"""# RNN 문제점

- 망이 깊어질수록, 최조의 기억이 희미해진다
  - **기억의 소실**
  - 타 신경망에 비해 구조적으로 기울기 소실문제가 있어서 더 많이 발생한다
- **장기 의존성 문제**
  - long-term dependency
  - 초반의 정보가 전체 문장의 맥락을 이해하는데 중요한데 이 부분이 희미해져서 그 의도를 누락할 수 있다
  - 역전파를 통해 최적화를 수행하는데 입력에 도달할 수 없게 된다 -> 기울기가 0에 가깝게 수렴한다
    - 경사손실(Vanishing Gradient)

## LSTM(Long Short Term Memory)

  - RNN 단점 극복을 위해 등장
    - 1997 : Long Short Term memory
    - 2014 : gated recurrent
  - RNNCELL 구조를 새롭게 변경
    - Cell State이라는 변수를 추가해서 경사소실 문제 해결
    - 잊혀질 정보, 기억할 정보, 새로들어온 정보를 컨베이밸트처럼 구성해서 cell을 설계
"""

Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/RNN_NEW/LSTM-cell2.png')
# 문장상에서 특정 토큰이 반복적으로 등장한다면 -> 중요한 정보 (단, 품사, 조사는 제외)
# 토큰의 빈도를 체크해서 그 중요도를 결정, 단어 연관성, 상관성, 유사도 분석

# Ct-1  이 라인은 RNN에는 없던 구조고, 장기기억선 추가
# FG : 잊어힐 정보(과거) -> 비율
# IG : 새로운 입력 -> 비율
# OG : 은닉층 가져얌난 출력 -> 비율 -> Ht
# 활성화함수 : sigmoid, tanh을 활용했다
# pointwise : 게이트를 통과한 데이터들이 Ct, Ht에 결합될 때 표현
#             연산이라는 의미, X => 행렬곱, + => 행렬합 수행하라

Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/RNN_NEW/LSTM_Cell_2.png')
# 일반 신경망 => xW + b
# 순환 신경망 => xtWt + h(t-1)W(t-1) + b

Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/RNN_NEW/LSTM_Cell.png')

"""- 파라미터가 너무 많다 : 식도 복잡, 연산량도 많다
- 이를 개선하기 위해 파라미터를 줄여서 학습 속도 상승 목표
- 망이 깊어질수록 차이가 나게 된다

## GRU

- LSTM의 매개변수를 줄여서 구현했다
- 훨씬 간단하면서 성능이 유사하다
- 게이트 역할은 동일하다
"""

Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/RNN_NEW/GRU_cell.png', width = 500)
# RNN 구조에서 메모리 셀을 LSTM처럼 설계
# 단, 장기기억선 제거, 단기기억선(Ht)에 gate 개념을 적용
# LSTM을 대체하였다. 현재 둘다 활용

Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/RNN_NEW/GRU_cell_2.png', width = 500)
# 장기기억선에 대한 식은 없다 -> 연산량이 줄어들었다(파라미터 감소)

"""# LSTM을 이용한 뉴스 카테고리 다중 분류 예측

## 연구목표 수립

- 예시
  - [PL] '클롭에게 악몽 선사' 손흥민, 커리어 첫 리그 20골! -> 해외축구, 스포츠
  - 코스피 오늘도 약세…FOMC 여진 지속 -> 국내증시, 증권

- 긴 텍스트를 읽고, 어떤 의미를 가졌는 보고, 카테고리를 분류해내는 문제
  - 문장 하나는 1개로 입력으로 본다면 one-to-one
  - 문장 안애 토큰을 기준으로 보면 mamy-to-one으로 볼수도 있다

- 데이터 
  - 로이터 뉴스 데이터 사용
  - 카테고리 46개
  - 데이터는 1만개 정도 뉴스
  - 텍스트의 수치화, 빈도 등등 다 계산되어 제공된다

## 기본 사용 모듈
"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing import sequence

from tensorflow.keras.datasets import reuters
from tensorflow.keras.callbacks import EarlyStopping

import numpy as np
import matplotlib.pyplot as plt

"""## 데이터 획득

"""

# mun_words : 빈도의 서열
# 모든 토큰의 빈도를 계산후 서열화해서 
# 1등 ~ 100등까지만 포함 => none으로 설정하면 모든 토큰을 가져온다
(X_train, y_train), (X_test, y_test) = reuters.load_data(num_words = 1000,
                                                          test_split = 0.2)

X_train.shape, y_train.shape, X_test.shape, y_test.shape

# 카테고리를 번호로 관리
y_train, np.unique(y_train), len(np.unique( y_train ))
# 카테고리는 총 46개 (정답의 개수)

# 데이터
print(X_train[0])
# 1 =>  출현 빈도가 1회라는 의미가 아닌, 빈도 서열 1위라는 것
# 데이터는 수치화 되어있고, 빈도서열로 그 중요도를 표현하고 있다

"""## 데이터 준비"""

# 패딩, 전체데이터의 크기를 동일화한다
# 특정 기준보다 넘치면 자르고, 부족하면 0으로 채운다
# maxlen은 전체 문장 중 가장 큰 값 + 1을 사용하거나
# 임의의 잣대를 넣어서 처리 가능
# 언어가 영어라서, 언어적 특성상 중요내용은 앞에 나온다
# 그래서 뒤쪽 정보는 제거해도 문제없다고 고려했음(정보손실)
X_train = sequence.pad_sequences(X_train, maxlen = 100)
X_test = sequence.pad_sequences(X_test, maxlen = 100)

# 데이터 1개(문장)를 100개의 피쳐로 표현
X_train.shape, X_test.shape

# y값의 전처리도 정확도에 영향을 미친다 
# 0, 1로 표현하는것이 가장 높은 성능을 낸다 - 원-핫 인코딩
y_train = to_categorical(y_train)
y_test  = to_categorical(y_test)

y_train.shape, y_test.shape

"""# 데이터 분석 - EDA, 시각적 분석"""

import seaborn as sns
import matplotlib.pyplot as plt

from numpy.core.fromnumeric import mean
# 뉴스 기사의 최대 길이, 평균길이
(X_train2, y_train2), (_, _) = reuters.load_data(
                                          num_words=1000, 
                                          test_split=0.2)

plt.hist([len(sample) for sample in X_train2], bins = 50)

plt.xlabel('length')
plt.ylabel('number')

plt.show()
print('뉴스의 최대길이', max([len(sample) for sample in X_train2 ]))
print('뉴스의 평균길이', sum(map(len, X_train2))/len(X_train2))
# 뉴스의 길이의 편차가 너무 크다
# 분포가 고르다면, 큰값, 작은 값, 중간값 정도 나눠서 데이터를 처리해도 될 듯
# 현재 패딩은 100으로 고정했기 때문에 대부분 데이터는 정보손실이 있다 => 튜닝필요

# 정답 분포 체크 -> 카테고리 0 ~ 45 이런 데이터가 균형있게 배치되었는가
# 특정 카테고리 데이터가 집중되어 있는지 체크

fig, _ = plt.subplots(ncols = 1)
fig.set_size_inches(12, 5)
sns.countplot( y_train2 )
# 3,4 뉴스가 너무 편향되었다 -> 다른 카테고리 뉴스를 보강하라
# 혹은 3,4 뉴스들을 제거하는 방식 고려

# 각 카테고리에 대한 빈도수 체크
np.unique(y_train2, return_counts = True)
# 각 중복된 카테고리의 빈도수 같이 출력

# X_train[0]을 보면, 0을 제외하고 나머지는 빈도서열이다
# 어떤 토큰으로 구성되어 있는지 체크
X_train[0]

# 워드 인덱스를 통해서 획득
tmp = reuters.get_word_index()
print(tmp)

# tmp에 + 3을 해야 실제 인덱스 위치가 나온다. 이 형식의 자료가 공통요소
for k, v in tmp.items() :
  print(k, v + 3)
  print('인덱스값', v + 3)
  print('단어값', k)
  break

"""## 모델 구축 - 인공신경망(딥러닝)"""

model = Sequential()
# 임베딩층(불러온 단어 총 수, 기사당 단어수(패딩값))
model.add(Embedding(1000, 100))
# LSTM(패딩값), 활성화함수는 기본값 적용
model.add(LSTM(100))
# 46은 데이터 정답에서 추출한 정답의 총 개수
model.add(Dense(46, activation = 'softmax'))

model.summary()

# 모델의 실행 옵션(컴파일 설정)
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

# 조기 학습 종료
early_stopping = EarlyStopping(patience = 5)

# 모델학습(실행)
his = model.fit(X_train, y_train, batch_size = 20, epochs = 200,
                validation_data = (X_test, y_test),
                callbacks = [early_stopping])

# 테스트 정확도 체크
print('\n정확도 %.4f' %(model.evaluate(X_test, y_test)[1]))

# 학습결과 확인
v_loss = his.history['val_loss']
y_loss = his.history['loss']

# 시각화
x_scope = np.arange(len(y_loss)) # x축을 몇개 표현(세대별 결과)

# 선형 그래프
plt.plot(x_scope,v_loss, marker = '.', c = 'red', label = 'val_loss')
plt.plot(x_scope,y_loss, marker = '.', c = 'blue', label = 'train_loss')

# 데코
plt.legend()
plt.grid()
plt.xlabel('epoch')
plt.ylabel('loss')
plt.show()

# 현재 기준은 네트워크를 향상, 데이터를 조정
# 다른 기법을 적용해서 정확도를 높일 필요가 있다

# 다른 데이터를 이용해서 CNN을 연결하여 처리 -> 1D 함수 사용
# 합성곱, 풀링 기법활

# 다른 기법을 적용 -> 동일 데이터에서 Attention을 사용

"""## 산출물(시스템통합) 생략

# LSTM + CNN(1D) 구조 조합하여 영화리뷰(IMDB)분류

- 인터넷 영화 데이터베이스(IMDB)
- 영화정보, 출연진, 개봉일시, 후기, 평점
- 25000여개 데이터 
- 긍정/부정 정보를 가지고 있다
"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding
# 합성곱 성분 추가 
from tensorflow.keras.layers import Activation, Conv1D, MaxPool1D, Dropout
# 정답이 2개 이므로, 원-핫인코딩 제외
#from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing import sequence
# 데이터는 영화 정보
from tensorflow.keras.datasets import imdb
from tensorflow.keras.callbacks import EarlyStopping

import numpy as np
import matplotlib.pyplot as plt

# 빈도 서열을 5000까지 확장 적용 -> 토큰 증가, 정보 손실도 줄어듬
(X_train, y_train), (X_test, y_test) = imdb.load_data(
                                          num_words=5000)
# imdb에서는  test_split 적용하면 오류
                                          #test_split=0.25)
# 데이터 shape 확인해 보니 훈련과 테스트가 동수로 보인다
(X_train.shape, y_train.shape), (X_test.shape, y_test.shape)

# 보건데 데이터가 다른 것 같다. 
# (단지 순서가 달라서 다르게 보일수도 있다)
X_train == X_test

# 패딩 => 앞선 프로젝트에서 토큰수를 5배 올렸으므로, 
# 패딩도 5배를 올려서 적용하겟다( 설정 )
X_train = sequence.pad_sequences( X_train, maxlen=500 )
X_test  = sequence.pad_sequences( X_test,  maxlen=500 )

# 출력의 원-핫 인코딩은 생략 => 정답이 긍정/부정 밖에 없어서

# 모델
model = Sequential()
model.add( Embedding(5000, 500) )
# 과적합
model.add(Dropout(0.5)) # 0.5 설정값
# CNN-합성곱층, 최대풀링층 -> 1f로만 구성
model.add(Conv1D(64, 5, padding= 'valid', activation = 'relu', strides = 1))
# 4 -> 설정값, 커널의 크기
model.add(MaxPool1D(4))
model.add( LSTM( 50 ) )
# 선형층 수렴, 활성화 추가
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.summary()

model.compile(loss='binary_crossentropy', 
               optimizer='adam', metrics=['accuracy'])

early_stopping  = EarlyStopping(patience = 3)

his = model.fit(X_train, y_train, 
                batch_size = 40, epochs = 100, 
                validation_split = 0.25, 
                callbacks = [early_stopping])

print('\n정확도 %.4f' % (model.evaluate(X_test, y_test)[1]))

# 학습결과 확인
v_loss = his.history['val_loss']
y_loss = his.history['loss']

# 시각화
x_scope = np.arange(len(y_loss)) # x축을 몇개 표현(세대별 결과)

# 선형 그래프
plt.plot(x_scope,v_loss, marker = '.', c = 'red', label = 'val_loss')
plt.plot(x_scope,y_loss, marker = '.', c = 'blue', label = 'train_loss')

# 데코
plt.legend()
plt.grid()
plt.xlabel('epoch')
plt.ylabel('loss')
plt.show()

"""# Attension

- 자연어 모델 기법들로 
  - 트랜스포머, BERT, GPT 등등 활용추천

- 2020.12월 세계 단백질 구조 예측대회(14회차)
  - 구글의 알파폴드 2 출전
  - 넘사벽 수준의 예측 모델 제시
  - 이것을 분석해 본 결과 -> 이것이 적용

- 원리
  - RNN의 한계점, 층이 깊어지면 기억 손실이 발생 => 매커니즘을 변경
"""

# 문제점
Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/RNN_NEW/rnn한계.png')
# 마지막 셀에 모든 정보가 집중된다 (문맥 백터)
# 입력이 길어지면 => 입력받은 셀도 많아지고 
# -> 선두의 결과가 뒤에서 희미해진다
# 문맥 백터가 결국 모든 값을 정확하게 디코딩할수 없게 된다

# 해결
# 가중치 계산 중요도 표현
Image('/content/drive/MyDrive/ComputerProgramming/DeepLearning/2.딥러닝/RNN_NEW/attension.png')
# 인코더와 디코더 사이에 층을 개입시킴(어텐션이 적용된 층)
# 각 메모리 셀에서 입력이 될 때마다 가중치 스코어를 계산 반영
# 스코어 기반으로 softmax를 처리해서 어텐션 가중치 생성(업데이트)
# 이를 통해서 각 입력대비 어떤 셀을 우선으로 처리할지 결정