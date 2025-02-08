install.packages("stats")

# 샘플 데이터 생성 (원하는 데이터를 사용하세요)
set.seed(123)
data <- data.frame(
  var1 = rnorm(100),
  var2 = rnorm(100),
  var3 = rnorm(100),
  var4 = rnorm(100)
)

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
