# SVM을 이용한 분류 구현


# 필요한 라이브러리 선언
from sklearn.svm import SVC # Soft Vector Machine를 사용하기 위한 라이브러리
from sklearn.datasets import load_iris # iris 데이터를 사용하기 위한 라이브러리
from sklearn.model_selection import train_test_split # 데이터 셋을 나누기 위한 라이브러리
from sklearn.preprocessing import StandardScaler # 정규화를 위한 라이브러리
from matplotlib import pyplot as plt # 그래프 출력을 위한 라이브러리

import numpy as np 
import mglearn


# 데이터 선언
iris = load_iris() # 붓꽃 데이터 불러오기
x = iris.data[:, [0,1]] # 첫번째열과 두번째열만 사용하여 독립변수에 저장
y = iris.target # 종속변수 저장


# 데이터 셋 분류 : 120개 훈련데이터와 30개 테스트 데이터로 분류
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)


## 데이터 정규화
print("꽃받침 길이 값의 범위 : ", "[", min(X_train[:,0]), ",", max(X_train[:,0]),"]") # 정규화 전의 첫번째 열 데이터의 범위
print("꽃받침 너비 값의 범위 : ", "[", min(X_train[:,1]), ",", max(X_train[:,1]),"]") # 정규화 전의 두번째 열 데이터의 범위
sc = StandardScaler() # 정규화를 위한 매소드 저장
sc.fit(X_train) # 정규화에 train 데이터를 적합
X_train_std = sc.transform(X_train) # train 데이터의 독립변수에 정규화 진행
X_test_std = sc.transform(X_test) # test 데이터의 독립변수에 정규화 진행
print("표준화된 꽃받침 길이 값의 범위 : ", "[", min(X_train_std[:,0]), ",", max(X_train_std[:,0]),"]") # 정규화 후의 첫번째 열 데이터의 범위
print("표준화된 꽃받침 너비 값의 범위 : ", "[", min(X_train_std[:,1]), ",", max(X_train_std[:,1]),"]") # 정규화 후의 두번째 열 데이터의 범위


# 모델 생성 및 적합, 예측
svm_model = SVC(kernel='linear', C=8, gamma=0.1) # linear 커널 방식으로 SVM 모델 생성
svm_model.fit(X_train_std, y_train) # train 데이터를 이용하여 모델 훈련
y_pred = svm_model.predict(X_test_std) # test 데이터를 통한 모델 적합


# 예측된 결과 출력
print("예측된 라벨:", y_pred)
print("실제 라벨:", y_test)
print("prediction accuracy: {:.2f}".format(np.mean(y_pred == y_test))) # 예측된 라벨과 실제 라벨이 같은 경우의 확률


## 그래프 시각화
plt.figure(figsize=[9,7]) # 출력 창 사이즈 설정
mglearn.plots.plot_2d_classification(svm_model, X_train_std, alpha=0.1) # svm_model의 영역 결과를 2차원 그림에 출력
mglearn.discrete_scatter(X_train_std[:, 0], X_train_std[:, 1], y_train) # 변수 1과 변수 2사이의 마크는 3번째 변수로 그린 산점도그림 
plt.legend(iris.target_names) # 범례 설정
plt.xlabel('sepal length') # x축 변수 이름 설정
plt.ylabel('sepal width') # y축 변수 이름 설정
plt.show() # 그래프 출력