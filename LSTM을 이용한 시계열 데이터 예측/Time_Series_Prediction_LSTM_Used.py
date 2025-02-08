# 순환 신경망(LSTM)으로 시계열 예측하기

# 장단기 메모리(LSTM)
# LSTM은 망각 게이트 추가
# 역전파 시 기울기 값이 급격하게 사라지거나 증가하는 문제 방지
# LSTM 장치(unit) : 셀, 입력 게이트, 출력 게이트, 삭제 게이트로 구성
# 셀은 임의의 시점에 대한 값을 기억하고 세 개의 게이터(입력, 망각, 출력)는 셀로 들어오고 나가는 정보의 흐름 조절

# 데이터 셋 설명
# S&P 500 지수 데이터
# 2000년 1월부터 2016년 8월까지의 종가(장 마감 시점의 가격)로 구성
# Date, Open(금액), High(금액), Low(금액), Close(금액), Volume(거래수)

# 필요한 라이브러리 선언
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import LSTM 
from tensorflow.keras.layers import Dense 
from tensorflow.keras.layers import Dropout

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 데이터 불러오기
dataset_train = pd.read_csv('Google_Stock_Price_Train.csv')
print(dataset_train.head())

#keras only takes numpy array
training_set = dataset_train.iloc[:, 1:2].values

print(training_set.shape)

# 데이터 시각화
plt.figure(figsize=(18, 8)) # 출력 창 사이즈 설정
plt.plot(dataset_train['Open'])
plt.title("Google Stock Open Prices") 
plt.xlabel("Time (oldest -> latest) ") 
plt.ylabel("Stock Open Price") 
plt.show()






# 정규화 및 데이터 변환
sc = MinMaxScaler(feature_range=(0, 1)) # minmax 정규화 진행
training_set_scaled = sc.fit_transform(training_set)




# LSTM 입력 데이터 생성
X_train = []
y_train = []

# 슬라이딩 윈도우
# 순환신경망이 61번째 가격을 예측할 수 있는 60개의 타임 스템프를 포함하기 위해 데이터 구조 변경
time_step = 60
for i in range(time_step, len(training_set_scaled)):
    X_train.append(training_set_scaled[i-time_step:i, 0])
    y_train.append(training_set_scaled[i, 0])





X_train, y_train = np.array(X_train), np.array(y_train)

print(X_train.shape)
print(y_train.shape)

# LSTM 입력 형태에 맞게 데이터 reshape
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

print(X_train.shape, y_train.shape)

# 순환신경망 모델 구축
regressor = Sequential()

# 1차 LSTM 레이어 추가
regressor.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
regressor.add(Dropout(0.2))

# 2차 LSTM 레이어 추가 : 50개 뉴런
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))

# 3차 LSTM 레이어 추가
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))

# 4차 LSTM 레이어 추가
regressor.add(LSTM(units=50))
regressor.add(Dropout(0.2))

# 출력 레이어 추가
regressor.add(Dense(units=1))

# RNN 모델 컴파일
regressor.compile(optimizer='adam', loss='mean_squared_error')

# 모델 학습
regressor.fit(X_train, y_train, epochs=100, batch_size=32)
# history = regressor.fit(X_train, y_train, epochs=100, batch_size=32)

# # 학습 손실 시각화
# plt.plot(history.history['loss'])
# plt.title('Model Loss')
# plt.ylabel('Loss')
# plt.xlabel('Epoch')
# plt.legend(['Train'], loc='upper right')
# plt.show()

# 데이터 불러오기 (테스트 데이터)
dataset_test = pd.read_csv('Google_Stock_Price_Test.csv')
real_stock_price = dataset_test.iloc[:, 1:2].values

# 예측을 위한 데이터 준비
dataset_total = pd.concat((dataset_train['Open'], dataset_test['Open']), axis=0)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - time_step:].values
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)

X_test = []
for i in range(time_step, len(inputs)):
    X_test.append(inputs[i-time_step:i, 0])

X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# 예측 수행
predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

# 결과 시각화
plt.figure(figsize=(18, 8))
plt.plot(real_stock_price, color='red', label='Real Google Stock Price')
plt.plot(predicted_stock_price, color='blue', label='Predicted Google Stock Price')
plt.title('Google Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Stock Price')
plt.legend()
plt.show()
