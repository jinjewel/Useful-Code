# 케라스 기반의 MLP 회귀모델 구현


# 필요한 라이브러리 선언
from sklearn.datasets import fetch_california_housing # 캘리포니아 주택데이터를 사용하기 위해 라이브러리
from sklearn.preprocessing import StandardScaler # 정규화를 위하여 라이브러리
from sklearn.model_selection import train_test_split # 테이터 셋을 나누기 위한 라이브러리

from tensorflow.keras.models import Sequential # 케라스에서 순차적인 레이어를 쉽게 묶어 신경망 모델을 구성할 수 있는 방법을 제공하는 라이브러리
from tensorflow.keras.layers import Dense # 케라스에서 가장 기본적으로 사용되는 레이어를 사용하기 위한 라이브러리
from tensorflow.keras import optimizers # 모델을 학습할 때 사용되는 최적화 알고리즘을 제공하기 위한 라이브러리

import matplotlib.pyplot as plt # 그래프를 출력하기 위한 라이브러리
import pandas as pd


# 데이터 불러오기
housing = fetch_california_housing()


# 데이터 셋 분류
X_train_full, X_test, y_train_full, y_test = train_test_split(housing.data, housing.target, random_state=42) # 디폴트 값인 0.75:0.25 비율로 데이터 셋을 분류
X_train, X_valid, y_train, y_valid = train_test_split(X_train_full, y_train_full, random_state=42) # 디폴트 값인 0.75:0.25 비율로 데이터 셋을 분류


# 회귀를 위한 스케일링 전처리
scaler = StandardScaler() 
X_train = scaler.fit_transform(X_train) 
X_valid = scaler.transform(X_valid) 
X_test = scaler.transform(X_test)


# 모델 만들기
model = Sequential([
    Dense(30, activation="relu", input_shape = X_train.shape[1:]), # 은닉층 1 : 30개의 뉴런, ReLU 활성화 함수 사용, 입력 데이터를 X_train.shape[1:]로 입력
    Dense(8), # 은닉층 2 : 8개의 뉴런
    Dense(1) # 출력층 : 1개의 뉴런 (회귀 문제이므로 활성화 함수 없음)
]) 


# 모델 컴파일 손실함수와 최적화 방법
model.compile(loss="mean_squared_error", optimizer=optimizers.SGD(learning_rate=1e-3))


# 모델 summary 생성한 모델의 레이어ㅡ 출력모양, 파라미터 개수 체크
model.summary()


# 모델 학습 epochs : 모델 학습 횟수
history = model.fit(X_train, y_train, batch_size = 50, epochs=20, validation_data=(X_valid, y_valid)) 


# 모델 평가하기 테스트할 학습데이터와 학습 레이블을 넣어주면 손실과 정확도를 반환
mse_test = model.evaluate(X_test, y_test)


# 모델의 평가 지표 이름 및 결과값
print("%s, %f"%(model.metrics_names, mse_test))


# 예측할 데이터 준비
X_new = X_test[:3] # 처음 3개의 샘플 데이터를 선택하여 예측
y_pred = model.predict(X_new) # 새로운 데이터에 대한 예측값 계산


# 그래프 시각화
plt.plot(pd.DataFrame(history.history))
plt.grid(True)
plt.gca().set_ylim(0, 1)
plt.show()
