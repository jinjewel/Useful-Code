rm(list=ls())
### k-means

# 원본 데이터 가져오기
# install.packages("openxlsx")
library(openxlsx)
data = read.xlsx("C:/Users/kcomwel/Desktop/데이터/0.전체데이터 - 복사본.xlsx")
Raw_material_data = data[1:154, c(1,4,5,6,7,8,9)]
Consider_location_data = data[1:154, c(1,10,11,12,13,14,15)]
Facilities_used_data = data[1:154, c(1,16,17,18,19,20,21,22)]

# 각 데이터 별 주요 데이터 뽑기
## 1. 원료데이터 셋
### 1) 음식물쓰레기발생량
food_waste = Raw_material_data[, 3] # 필터링
food_waste_numeric = as.numeric(food_waste) # 숫자화
food_waste_sc = scale(food_waste_numeric) # 표준화

### 2) 하수 연계처리량
throughput_water = Raw_material_data[, 6] # 필터링
throughput_waterr_numeric = as.numeric(throughput_water) # 숫자화
throughput_water_sc = scale(throughput_waterr_numeric) # 표준화

### 3) 최종 데이터 셋
df_1 = cbind(food_waste_sc, throughput_water_sc)

## 2. 입지시설데이터 셋
### 1) 하수처리 + 하수찌꺼기
sewer_Facilities = Consider_location_data[,4] + Consider_location_data[,5]
sewer_Facilities_numeric = as.numeric(sewer_Facilities) # 숫자화
sewer_Facilities_sc = scale(sewer_Facilities_numeric) # 표준화

### 2) 분뇨처리 + 음식물자원화 시설의 수
etc_Facilities = Consider_location_data[,6] + Consider_location_data[,7]
etc_Facilities_numeric = as.numeric(etc_Facilities) # 숫자화
etc_Facilities_sc = scale(etc_Facilities_numeric) # 표준화

### 3) 최종 데이터 셋
df_2 = cbind(sewer_Facilities_sc, etc_Facilities_sc)

## 3. 에너지 사용시설 셋
### 1) 발전량
power_generation = Facilities_used_data[,3]
power_generation_numeric = as.numeric(power_generation) # 숫자화
power_generation_sc = scale(power_generation_numeric) # 표준화

### 2) 산업공장수
Resource_use_facilities = Facilities_used_data[,2] + Facilities_used_data[,4] + Facilities_used_data[,5] + Facilities_used_data[,6] + Facilities_used_data[,7]
Resource_use_facilities_numeric = as.numeric(Resource_use_facilities) # 숫자화
Resource_use_facilities_sc = scale(Resource_use_facilities_numeric) + scale(as.numeric(Facilities_used_data[,8])) # 표준화

### 3) 최종 데이터 셋
df_3 = cbind(power_generation_sc, Resource_use_facilities_sc)



# 클러스트링 분석
# install.packages("factoextra")
library(factoextra)
## 1. 원료데이터 셋

### 군집 수 선택 기준
# elbow 방법 (완만해지는 곳 기준: 4개)
fviz_nbclust(df_1, stats::kmeans, method = "wss")
# silhouette 방법(실루엣 계수가 가장 높은 4개)
fviz_nbclust(df_1, stats::kmeans, method = "silhouette")

### K-Mean 방법
# elbow 방법 
x11()
kmeans_1_1_1 = kmeans(df_1, centers=4)
fviz_cluster(kmeans_1_1_1, data = df_1, stand=F, xlab = "food_waste", ylab = "throughput_water", main="1)_kmean")
# silhouette 방법
x11()
kmeans_1_1_2 = kmeans(df_1, centers=4)
fviz_cluster(kmeans_1_1_2, data = df_1, stand=F, xlab = "food_waste", ylab = "throughput_water", main="1)_kmean_silhouette")

### K-medoids 방법
# install.packages("cluster")
library(cluster)
# elbow 방법
x11() 
kmedoids_1_2_1 = pam(df_1, 4) 
fviz_cluster(kmedoids_1_2_1, data=df_1, stand=F, xlab = "food_waste", ylab = "throughput_water", main="1)_medoids")
# silhouette 방법
x11()
kmedoids_1_2_2 = pam(df_1, 4) 
fviz_cluster(kmedoids_1_2_2, data=df_1, stand=F, xlab = "food_waste", ylab = "throughput_water", main="1)_medoids_silhouette")


## 2. 입지시설데이터 셋
### 군집 수 선택 기준
# elbow 방법 (완만해지는 곳 기준: 4개)
fviz_nbclust(df_2, stats::kmeans, method = "wss")
# silhouette 방법(실루엣 계수가 가장 높은 3개)
fviz_nbclust(df_2, stats::kmeans, method = "silhouette")

### K-Mean 방법
# elbow 방법 
x11()
kmeans_2_1_1 = kmeans(df_2, centers=4)
fviz_cluster(kmeans_2_1_1, data = df_2, stand=F, xlab = "sewer_Facilities", ylab = "etc_Facilities", main="2)_kmean_elbow")
# silhouette 방법
x11()
kmeans_2_1_2 = kmeans(df_2, centers=3)
fviz_cluster(kmeans_2_1_2, data = df_2, stand=F, xlab = "sewer_Facilities", ylab = "etc_Facilities", main="2)_kmean_silhouette")

### K-medoids 방법
# install.packages("cluster")
library(cluster)
# elbow 방법
x11()
kmedoids_2_2_1 = pam(df_2, 4) 
fviz_cluster(kmedoids_2_2_1, data=df_2, stand=F, xlab = "sewer_Facilities", ylab = "etc_Facilities", main="2)_medoids_elbow")
# silhouette 방법
x11() 
kmedoids_2_2_2 = pam(df_2, 3) 
fviz_cluster(kmedoids_2_2_2, data=df_2, stand=F, xlab = "sewer_Facilities", ylab = "etc_Facilities", main="2)_medoids_silhouette")


## 3. 에너지 사용시설 셋
### 군집 수 선택 기준
# elbow 방법 (완만해지는 곳 기준: 3개)
fviz_nbclust(df_3, stats::kmeans, method = "wss")
# silhouette 방법(실루엣 계수가 가장 높은 2개)
fviz_nbclust(df_3, stats::kmeans, method = "silhouette")

### K-Mean 방법
# elbow 방법
x11() 
kmeans_3_1_1 = kmeans(df_3, centers=3)
fviz_cluster(kmeans_3_1_1, data = df_3, stand=F, xlab = "power_generation", ylab = "Resource_use_facilities", main="3)_kmean_elbow")
# silhouette 방법
x11()
kmeans_3_1_2 = kmeans(df_3, centers=2)
fviz_cluster(kmeans_3_1_2, data = df_3, stand=F, xlab = "power_generation", ylab = "Resource_use_facilities", main="3)_kmean_silhouette")


### K-medoids 방법
# install.packages("cluster")
library(cluster)
# elbow 방법 
x11()
kmedoids_3_2_1 = pam(df_3, 3) 
fviz_cluster(kmedoids_3_2_1, data=df_3, stand=F, xlab = "power_generation", ylab = "Resource_use_facilities", main="3)_medoids_elbow")
# silhouette 방법
x11()
kmedoids_3_2_2 = pam(df_3, 2) 
fviz_cluster(kmedoids_3_2_2, data=df_3, stand=F, xlab = "power_generation", ylab = "Resource_use_facilities", main="3)_medoids_silhouette")


# 클러스터링 결과
## 1번데이터 - kmeans 방법을 사용한 결과
### elbow 방법으로 4개 군집 생성, 4번 군집 선정
x11()
kmeans_1_1_1 = kmeans(df_1, centers=4)
fviz_cluster(kmeans_1_1_1, data = df_1, stand=F, xlab = "food_waste", ylab = "throughput_water", main="1)_kmean_elbow")
kmeans_1_1_1$size # [16 44 93 1]
kmeans_1_1_1$cluster

## 1번데이터 - medoids 방법을 사용한 결과
### elbow 방법으로 4개 군집 생성, 4번 군집 선정
x11() 
kmedoids_1_2_1 = pam(df_1, 4) 
fviz_cluster(kmedoids_1_2_1, data=df_1, stand=F, xlab = "food_waste", ylab = "throughput_water", main="1)_medoids_elbow")
kmedoids_1_2_1$clusinfo # [49 14 90 1]
kmedoids_1_2_1$clustering

## 2번데이터 - kmeans 방법을 사용한 결과
### elbow 방법으로 4개 군집 생성, 4번 군집 선정 
x11()
kmeans_2_1_1 = kmeans(df_2, centers=4)
fviz_cluster(kmeans_2_1_1, data = df_2, stand=F, xlab = "sewer_Facilities", ylab = "etc_Facilities", main="2)_kmean_elbow")
kmeans_2_1_1$size # [48 65  6 35]
kmeans_2_1_1$cluster

## 2번데이터 - medoids 방법을 사용한 결과
### silhouette 방법으로 3개 군집 생성, 3번 군집 선정
x11() 
kmedoids_2_2_2 = pam(df_2, 3) 
fviz_cluster(kmedoids_2_2_2, data=df_2, stand=F, xlab = "sewer_Facilities", ylab = "etc_Facilities", main="2)_medoids_silhouette")
kmedoids_2_2_2$clusinfo # [66 45 43]
kmedoids_2_2_2$clustering

## 3번데이터 - kmeans 방법을 사용한 결과
### elbow 방법으로 3개 군집 생성, 3번 군집 선정 
x11() 
kmeans_3_1_1 = kmeans(df_3, centers=3)
fviz_cluster(kmeans_3_1_1, data = df_3, stand=F, xlab = "power_generation", ylab = "Resource_use_facilities", main="3)_kmean_elbow")
kmeans_3_1_1$size # [29 8 117]
kmeans_3_1_1$cluster

## 3번데이터 - medoids 방법을 사용한 결과
### elbow 방법으로 3개 군집 생성, 3번 군집 선정 
x11()
kmedoids_3_2_1 = pam(df_3, 3) 
fviz_cluster(kmedoids_3_2_1, data=df_3, stand=F, xlab = "power_generation", ylab = "Resource_use_facilities", main="3)_medoids_elbow")
kmedoids_3_2_1$clusinfo # [112 33 9]
kmedoids_3_2_1$clustering


# 하드보팅(hard voting)
## 각 결과에서 해당하는 군집의 지역 확인 후 지역 고르는 기준 설정(중복되어서 나오는 횟수가 기준)


# 회귀분석 > 다중공선성 확인

