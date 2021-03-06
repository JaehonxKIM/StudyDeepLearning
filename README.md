# StudyDeepLearning

## 1일차
- 강화학습 용어 정리(간략하게)
    - 보상
    - 학습전략, 사이클
    - 에피소드
    - 마르코프 결정 과정
    - 정책계산법
        - 정책반복법
        - 가치반복법
            - Saras(살사)
            - Q-Learning(큐러닝)
            - DQN(딥마인드에서 제작, 딥러닝)
- 다중 슬롯머신 구현

## 2일차
- 클래스의 개념, 구성, 문법
- 게임엔진(EpsilonGreedyEngine, UCB1Engine)
- 시뮬레이션(슬롯머신)
- 간단한 미로게임 만들기
    - 게임 맵 그리고 미로 만들기(plot 사용)

## 3일차
- 요소 실행
    - 에이전트 상태 정의, 시뮬레이션
    - 최단거리로 이동하게 만들기
- 정책 갱신함수
- 가치 계산법

- 수익
    - 즉시 보상을 제외한 미래에서 얻을 수 있는 수익은 확정되지 않는 값이다
    - 에이전트는 조건부로 정책을 고정하여 미래의 수입을 계산할 수 있다
        - 이렇게 반영된 수익을 가치라고 부른다
        - 이런 가치를 가장 크게 얻을 수 있는 조건을 찾아내는 것 => 학습목표

- 구현하기 위한 방법
    - 행동 가치 함수
        - Q 함수
        - Sarsa, Q-Learning, DQN,...
    - 상태 가치 함수
        - V 함수
        - A2C, Dueling Network
- 벨만 방정식
    - 행동 가치 함수, 상태 가치 함수를 수학적으로 표현한 것
    - 현재 상태와 다음 상태의 관계를 나타내는 방정식
- 마르크프 계산결정
    - 벨만 방정식이 성립하기 위한 환경은 MDP이여야 한다 -> 다음 상태가 현재 상태에서 선택한 행동에 따라 확정되는 시스템
- Q-Learning & Sarsa

## 4일차
- Q-Learning, Sarsa 시뮬레이션
- 행동가치함수 통합 -> 클로저(함수 안에 함수)
- 가치계산법 적용
    - Sarsa & Q-Learning
- 딥러닝 개요
    - 개발환경 -> GPU, CPU, TPU
- 엔진
    - Tensorflow
    - Pytorch
    - Keras
- 인공신경망
    - CNN
        - YOLO, Fast CNN, Mediapipe, opencv
    - RNN
        - 자연어처리, 시계열분야, 
    - 구성
        - one - to - many => 이미지를 보고 텍스트 생성(출력)
        - many - to - one => 감정분석, 스팸메일 분류
        - many - to - many => 기계 번역, 챗봇
    - GAN 

## 5일차
    - Tensorflow, CNN
    - Tensorflow 기본 요소
        - Tensor, 상수, 연산, 변수, 플레이스 홀더
        - 플레이스 홀더(placeholder)
            - 고정크기
            - 가변크기
    - CNN
        - 네트워크 구조 -> ANN, DNN, CNN
        - 입력층 & 은닉층 & 출력층
        - 은닉층
            - 합성곱층(입력, 커널, 스트라이드, 패딩, 출력)
            - 풀링층
            - 전결합층
        - 출력층
    - 손글씨 데이터를 이용해 손글씨를 인식하는 딥러닝 모델 구축

## 7일차
    - Tensorflow 1.x를 이용한 cnn 구현 및 mnist 손글씨 이미지 분류
    - 밑 코드에서 오류나서 다음날 고침
    - 텐서플로우의 전체적인 플로우를 알아보았다
    - keras를 이용한 cnn
    - 파이토치 기초
    - 파이토치 이용한 cnn

## 8일차 
    - 7일차 학습내용과 비슷함 => 파이토치를 이용한 cnn

## 9일차
    - 활성화함수
        - sigmoid, tanh, Relu, Leaky Relu, P Relu, ELU, Maxout, softmax
    - 자연어처리 단어임베딩 긍정 or 부정 예측
        - 인터넷 기사, 댓글
        - 한글의 처리 어려움
        - 원-핫인코딩, 패딩
        - MeCab 사용

## 10일차
    - RNN, LSTM, Attention
        - 기존 신경망에 단점이 있어 보완하여 순환신경망이 등장함
        - RNN은 망이 깊어질수록 최초의 기억이 희미해진다
        - 장기의존성에 문제 
        - Cell State이라는 변수를 추가해서 경사소실 문제 해결
        - 잊혀질 정보, 기억할 정보, 새로들어온 정보를 컨베이밸트처럼 구성해서 cell을 설계
    - GRU 
    - LSTM을 이용한 뉴스 카테고리 다중 분류 예측 모델 구축
    - LSTM과 CNN(1D)를 조합해 IMDB(영화리뷰) 분류
    - Attention(자연어 처리) 적용
## 11일차 
    - 전이학습
    - 사전학습된 모델 사용 가중치 모두 초기화
    - 사전학습된 모델 사용 가중치 모두 사용할 경우 
    - 생산성 적대 신경망
    - 딥러닝 나머지 부분