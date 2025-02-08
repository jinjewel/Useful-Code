rm(list=ls())

# 원본 데이터 가져오기
# install.packages("openxlsx")
library(openxlsx)
data = read.xlsx("C:/Users/User/Desktop/Environmental-Data-Analysis-Competition/5.PCA/최종요인.xlsx")
data <- data[,-c(1)]


# PCA를 위한 패키지 
# install.packages("stats")

# 데이터 스케일링 (PCA 수행 전 필수)
scaled_data <- scale(data)

# PCA 수행
pca_result <- prcomp(scaled_data, center = TRUE, scale. = TRUE)

# PCA 결과 요약
summary_pca <- summary(pca_result)

# 주성분
pca_components <- pca_result$x

# 설명된 분산 비율
explained_variance <- summary_pca$importance[2, ]

# 누적 설명된 분산 비율
cumulative_explained_variance <- summary_pca$importance[3, ]

# 결과 출력
print("PCA 결과 요약:")
print(summary_pca)

print("주성분:")
print(head(pca_components))

print("설명된 분산 비율:")
print(explained_variance)

print("누적 설명된 분산 비율:")
print(cumulative_explained_variance)
