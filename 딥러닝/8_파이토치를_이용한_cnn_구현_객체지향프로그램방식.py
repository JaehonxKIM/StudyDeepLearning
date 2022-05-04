# -*- coding: utf-8 -*-
"""8. 파이토치를 이용한 CNN 구현_객체지향프로그램방식.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DwSCxkBYWNwRk2lwDG0TK375FgaIPcJS

# 목적

- 파이토치로 CNN 구현
- 객체지향 스타일로 구현
- 데이터는 FasionMNIST

# 모듈 가져오기, 환경변수
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# 자체 데이터 포멧을 사용한다
from torchvision import transforms, datasets

# GPU 설정
use_cuda = torch.cuda.is_available()
DEVICE   = torch.device( 'cuda' if use_cuda else 'cpu' )
DEVICE

# 학습 환경 변수
EPOCHES = 30 if use_cuda else 5 # CPU는 5세대학습, GPU 30세대 학습
# 1회 학습량 -> mini batch size
BATCH_SIZE = 64                 # 가급적 2의 배수로 세팅

EPOCHES, BATCH_SIZE

"""# 데이터 준비

- 제공되는 FashsionMNist 사용
- API로 제공받아서 사용
"""

# 훈련 데이터 
train_loader  = torch.utils.data.DataLoader(
  datasets.FashionMNIST(
    root  = './data',       # 데이터 저장위치
    train = True,           # 훈련용 데이터 인가
    download = True,        # 데이터가 없으면 다운로드 있으면 스킵
    # 이미지 전처리 및 가공 방식 기술
    transform = transforms.Compose([
      transforms.ToTensor(), # 이미지를 텐서로 변환해서 받겠다  
      transforms.Normalize( 0.2, 0.3 ) # 평균, 표준편차값 설정값
    ])
  ),
  batch_size  = BATCH_SIZE, 
  shuffle     = True
)
# 테스트 데이터
test_loader   = torch.utils.data.DataLoader(
  datasets.FashionMNIST(
    root  = './data',       # 데이터 저장위치
    train = True,           # 훈련용 데이터 인가
    download = False,       # 데이터가 없으면 다운로드 있으면 스킵
    # 이미지 전처리
    transform = transforms.Compose([
      transforms.ToTensor(), # 이미지를 텐서로 변환해서 받겠다 
      transforms.Normalize( 0.2, 0.3 ) # 평균, 표준편차값 설정값    
    ])
  ),
  batch_size  = BATCH_SIZE, 
  shuffle     = True
)

"""# 신경망 구성

- shape 설계 : 이미 완료(동일하게 구성)
"""

class Net(nn.Module):
  # 생성자
  def __init__(self):
    # 부모 생성자 호출
    super(Net, self).__init__()
    # 맴버 변수 초기화 ,신경망의 요소 초기화
    # 합성곱층
    self.conv1 = nn.Conv2d( 1,  32,   5, 1, padding='same')
    self.conv2 = nn.Conv2d( 32, 32*2, 5, 1, padding='same')
    # 과적합방지층
    self.conv2_drop = nn.Dropout2d(0.1)
    # 전결합층
    self.fc     = nn.Linear(7*7*32*2, 1024)
    # 출력층 
    self.output = nn.Linear(1024, 10)
    pass
  # 맴버함수 : 순전파 신경망 구성 (override:재정의)
  def forward(self, x):
    # 순전파 네트워크 구성
    # 1층 (기존 구성 대비 합성곱후 바로 활성화 함수 통과를 하지 않았다)
    x = F.relu( F.max_pool2d( self.conv1( x ), 2 ) )
    # 2층 (합성곱에서 활성화생략하고 단 과적합방지를 추가했다)
    x = F.relu( F.max_pool2d( F.dropout( self.conv2( x ) ), 2 ) )
    # Flattern (4D->2D) -> 전결합층
    x = x.view(-1, 7*7*32*2)
    x = F.relu( self.fc( x ) )
    # 드롭아웃층    
    # 부모의 맴버 변수 : self.training
    x = F.dropout( x, training=self.training )
    # 출력층
    x = F.relu( self.output(x) )
    return F.log_softmax( x, dim=1 ) # 이 이미지는 xx 옷일 확률이 y%이다
    pass

# 네트워크에 사용 하드웨어 설정
model = Net().to(DEVICE)

model.parameters(), model

# 최적화 도구준비
# 확률적 경사 하강법
# parameters : 튜닝 대상
# lr : 학습비율, 적용비율
# momentum : 속도
optimizer = optim.SGD( model.parameters(), lr=0.01, momentum=0.5  )

"""# 학습 구성"""

# 훈련용 함수
def train( model, loader, optimizer, epoch):
  '''
    model : 모델
    loader : 데이터 공급자
    optimizer : 최적화 도구 
    epoch : 에폭 (로그표시할때 사용)
  '''
  # 학습 모드 전환  
  model.train()
  # 반복적 배치학습
  # data:데이터(피처), taget:정답
  for idx, (data, target)  in enumerate( loader ):
    # 하드웨어 지정
    data  = data.to( DEVICE )
    target = target.to( DEVICE )
    # 최적화 도구 초기화-> 누적된 값을 초기화 
    optimizer.zero_grad()
    # 모델에 데이터 삽입
    output = model( data )
    # 평가 지표 함수 크로스엔트로피 연결
    loss = F.cross_entropy( output, target)
    # 오차 역전파를 진행 -> 최적화 수행
    loss.backward()
    # 최적화 도구 조정-> 모델 파라미터 갱신
    optimizer.step()
    # 로그 출력
    if idx % 200 == 0:
      print( f'Train epoch: {epoch} { idx*len(data) } / { len(loader) } \
               loss={loss.item()} ' )
  pass

# 테스트용 함수
def test( model, loader):
  '''
    model : 모델
    loader : 데이터 공급자
  '''
  # 테스트 모드 전환
  model.eval()
  loss = 0
  accuracy = 0
  # 테스트 행위가 학습에 영향을 미지치 않게 조정
  with torch.no_grad():
    # 이 내부에서 진행된 내용은 기록하지 않는다 
    for data, target  in loader:
      data, target  = data.to( DEVICE ),target.to( DEVICE )
      output       = model( data )
      # 오차율 합산(누적) 
      loss += F.cross_entropy( output, target, reduction='sum').item()
      # 예측, 예측 확률이 가장 높은 값을 가진 인덱스 추출 => [1]
      pred = output.max(1, keepdim=True)[1]
      # 정확도 체크
      accuracy += pred.eq( target.view_as(pred) ).sum().item()

  # 평균 손실
  mean_loss     = loss / len(loader.dataset)
  # 평균 정확도 => %
  mean_accuracy = 100. * accuracy / len(loader.dataset)
  return mean_loss, mean_accuracy

len(train_loader), len(train_loader.dataset)

"""# 테스트 및 실행"""

for epoch in range( 1, EPOCHES + 1 ):
  # 훈련
  train( model, train_loader, optimizer, epoch )
  # 테스트
  mean_loss, mean_accuracy = test( model, test_loader )
  # 로그
  print(f'epoch:{epoch} loss:{mean_loss:.4f} acc:{mean_accuracy:.4f}')

# 놔두면 계속 올라가는 추세이므로 정확도 92%에서 멈춤

