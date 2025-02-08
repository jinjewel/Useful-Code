# 케라스 기반의 필기체 인식(MNIST) 구현


# 필요한 라이브러리 선언
import warnings # 해당 오류를 무시하기 위한 라이브러리
warnings.simplefilter(action='ignore', category=FutureWarning)  # FutureWarning 무시

from tensorflow.keras.datasets import mnist # MNIST 데이터를 사용하기 위한 라이브러리
from tensorflow.keras.models import Sequential # 순차적인 레이어를 쉽게 묶어 신경망 모델을 구성할 수 있는 방법을 위한 라이브러리
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D # 여러 레이어를 사용하기 위한 라이브러리

import matplotlib.pyplot as plt
import tensorflow as tf
import sys
import numpy as np
np.random.seed(7)  # 난수 시드 설정


# Python 및 TensorFlow 버전 출력
print('Python 버전', sys.version)
print('TensorFlow 버전:', tf.__version__)  


# 데이터셋 선언
(x_train, y_train), (x_test, y_test) = mnist.load_data()
img_rows = 28 # 이미지의 세로 길이 선언
img_cols = 28 # 이미지의 가로 길이 선언


# 이미지를 28x28 크기의 배열로 변환
input_shape = (img_rows, img_cols, 1) # 입력 이미지의 형태를 설정
x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1) # 데이터를 4D 텐서로 변환
x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1) # 데이터를 4D 텐서로 변환


# 데이터를 0 ~ 1 사이의 값으로 정규화
x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255


# 데이터 형태 및 샘플 수 출력
print('x_train shape:', x_train.shape) 
print(x_train.shape[0], 'train samples') 
print(x_test.shape[0], 'test samples')


# 하이퍼파라미터 설정
batch_size = 128 # 샘플 128개를 
num_classes = 10
epochs = 12 # 모두 12번 실행


# 레이블을 one-hot 인코딩
y_train = tf.keras.utils.to_categorical(y_train, num_classes)
y_test = tf.keras.utils.to_categorical(y_test, num_classes)


# 모델 정의
model = Sequential() # Sequential 모델을 정의합니다.
model.add(Conv2D(32, kernel_size=(5, 5), strides=(1, 1), padding='same', activation='relu', input_shape=input_shape))  # 첫 번째 Conv 레이어
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2))) # 첫 번째 MaxPooling 레이어

model.add(Conv2D(64, (2, 2), activation='relu', padding='same'))  # 두 번째 Conv 레이어
model.add(MaxPooling2D(pool_size=(2, 2))) # 두 번째 MaxPooling 레이어

model.add(Dropout(0.25)) # Dropout 레이어. 입력 층 이라서 Dropout의 비율을 0.25로 사용
model.add(Flatten()) # Flatten 레이어, 2차원 배열을 1차원 배열로 전환해주는 함수

model.add(Dense(1000, activation='relu')) # Dense 레이어, 1000개 노드, 활성함수로 ReLU 사용. 
model.add(Dropout(0.5)) # Dropout 레이어, . 히든층이라서 Dropout의 비율을 0.5로 사용

model.add(Dense(num_classes, activation='softmax')) # 출력 레이어
model.summary # 모델 요약 출력


# 모델 컴파일
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


# 모델 학습
hist = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1, validation_data=(x_test, y_test))


# 모델 평가
score = model.evaluate(x_test, y_test, verbose=0) 
print('Test loss:', score[0]) 
print('Test accuracy:', score[1])


# 테스트 및 학습 오차 그래프
y_vloss = hist.history['val_loss']
y_loss = hist.history['loss']
x_len = np.arange(len(y_loss))


plt.plot(x_len, y_vloss, marker='.', c="red", label='Testset_loss') 
plt.plot(x_len, y_loss, marker='.', c="blue", label='Trainset_loss')
plt.legend(loc='upper right')
plt.grid()
plt.xlabel('epoch')
plt.ylabel('loss')
plt.show()


# 예측 결과 직접 확인하기
n = 0
plt.imshow(x_test[n].reshape(28, 28), cmap='Greys', interpolation='nearest') 
plt.show()
print('The Answer is ', model.predict_classes(x_test[n].reshape((1, 28, 28, 1))))