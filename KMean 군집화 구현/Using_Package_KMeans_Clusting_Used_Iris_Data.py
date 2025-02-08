# 패키지를 이용하여 K-Means 군집화 구현

# 필요한 라이브러리 선언
from sklearn.cluster import KMeans # KMeans 클러스터링을 하기 위한 라이브러리
from sklearn.datasets import load_iris # 붓꽃 데이터를 가져오기 위한 라이브러리
from matplotlib import pyplot as plt # 그래프 라이브러리

import numpy as np # 행렬 연산을 위한 라이브러리


# 데이터 선언
iris = load_iris()
samples = iris.data # sample 데이러를 생성
x = samples[:,0] # 첫번째 열 데이터를 저장
y = samples[:,1] # 두번째 열 데이터를 저장


# kmeans 군집화 모델 생성 및 적합, 예측
model = KMeans(n_clusters = 3) # 3개의 그룹으로 나누는 K-Means 모델 생성
model.fit(samples) # 모델 적합
labels = model.predict(samples) # 새로운 값에 대한 예측


# 그래프 출력
plt.figure()
plt.scatter(x, y, c=labels, alpha=0.5)  
plt.xlabel('sepal length (cm)')
plt.ylabel('sepal width (cm)')
plt.show()
