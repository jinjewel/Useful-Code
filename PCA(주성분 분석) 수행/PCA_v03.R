rm(list=ls())

# 원본 데이터 가져오기
# install.packages("openxlsx")
library(openxlsx)
data_name = read.xlsx("C:/Users/User/Desktop/Environmental-Data-Analysis-Competition/5.PCA/최종요인.xlsx")
data <- data_name[,-c(1)]


# PCA를 위한 패키지 
# install.packages("stats")
library(stats)


# 데이터 스케일링 (PCA 수행 전 필수)
scaled_data <- scale(data)


# PCA 수행
pca_result <- prcomp(scaled_data, center = TRUE, scale. = TRUE)
summary_pca <- summary(pca_result) # PCA 결과 요약
pca_components <- pca_result$x # 각 변수에 대한 주성분에 해당하는 가중치
explained_variance <- summary_pca$importance[2, ] # 설명된 분산 비율
cumulative_explained_variance <- summary_pca$importance[3, ] # 누적 설명된 분산 비율
cumulative_explained_variance # 2번째 주성분까지 설명력이 88% 된다.


## 인자부하 행렬
pca_result
## 각 주성분에 대한 가중치
explained_variance


## 입지 스코어 생성
# socre_1 : 첫번째 부하 행렬
# socre_2 : 두번째 부하 행렬
socre_1 =  data[,1] * (0.644*0.534 - 0.428*0.3444) + data[,2] * (- 0.716*0.534 - 0.044*0.344) + data[,3] * (0.270*0.534 + 0.903*0.344)
socre_2 =  data[,1] * (0.644*0.534 + 0.428*0.3444) + data[,2] * (- 0.716*0.534 + 0.044*0.344) + data[,3] * (0.270*0.534 - 0.903*0.344)
socre_3 =  data[,1] * (0.644*0.534 + 0.428*0.3444) + data[,2] * (0.716*0.534 + 0.044*0.344) + data[,3] * (0.270*0.534 + 0.903*0.344)


## 지역명 + 입지스코어
score_data = data.frame(cbind(data_name[,1],socre_1, socre_2, socre_3))


# 결과를 엑셀 파일로 저장
library(writexl)
write_xlsx(score_data, path = "C:/Users/User/Desktop/Environmental-Data-Analysis-Competition/5.PCA/최종 입지 점수.xlsx")

























