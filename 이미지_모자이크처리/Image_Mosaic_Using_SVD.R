# SVD를 이용한 이미지 처리
rm(list=ls())

# 이미지를 가져오기 위해 {OpenImageR}패키지 readImage()함수 사용
### install.packages("OpenImageR") # 패키지 다운로드 필요
library(OpenImageR)


# 경로 불러오기 및 원본 사진 저장
setwd("C:/Users/User/Desktop/다변량통계 분석 및 실습/2장") # 디렉토리를 바꾼다
dir() # 작업 디렉토리에 지정되어있는 경로의 파일명 등을 알려준다.
image_real <- readImage("pansy.jpg") # 사진 정보를 저장한다.


# 사진 데이터를 요약
dim(image_real) # 3차원 데이터를 요약


# 저장된 사진 데이터를 사진으로 복구하기
### method = ‘bilinear’또는 ‘nearest’ 인접이웃 방법 
image_bil = resizeImage(image_real,dim(image_real)[1],dim(image_real)[2],method="bilinear") 
imageShow(image_bil)
image_nea = resizeImage(image_real,dim(image_real)[1],dim(image_real)[2],method="nearest") 
imageShow(image_nea)


# 저장된 사진 데이터를 흑백 데이터로 변형하고 표현하기
image_gra <- rgb_2gray(image_real) # rgb_2gray()함수를 이용하여 흑백으로 변경
dim(image_gra) # 데이터를 3차원에서 2차원 배열로 요약, 600 * 465 = 279,000 메모리 필요
imageShow(image_gra)


# SVD 적용 (사용된 색상의 횟수를 확인하기 위해)
image_gra_svd <- svd(image_gra)
image_gra_lamda <- diag(image_gra_svd$d)
image_gra_U <- image_gra_svd$u
image_gra_V <- image_gra_svd$v


# 그래프에 특잇값 표시
plot(1:length(image_gra_svd$d),image_gra_svd$d) # 1부터 465개의 특잇값을 순서대로 표시


# 1개의 특잇값(가장 많이 사용된 색)을 사용하여 그림을 그리기.
image_gra_U_trun <- as.matrix(image_gra_U[,1])
image_gra_V_trun <- as.matrix(image_gra_V[,1])
image_gra_lamda_trun <- as.matrix(image_gra_lamda[1,1])
restore_image_gra <- image_gra_U_trun %*% image_gra_lamda_trun %*% t(image_gra_V_trun)
dim(restore_image_gra) # 결과 [1] 600 465
plot(0,0)
imageShow(restore_image_gra) # 600*1 + 1 + 1*465 = 1066 메모리가 저장하는데 사용됨(원본의 1,066/279,000*100=0.382%)


# 5개의 특잇값, 가장 많이 사용된 색 5개를 사용하여 그림을 그리기.
depth <- 5 
image_gra_U_trun <- as.matrix(image_gra_U[,1:depth])
image_gra_V_trun <- as.matrix(image_gra_V[,1:depth])
image_gra_lamda_trun <- as.matrix(image_gra_lamda[1:depth,1:depth])
restore_image_gra <- image_gra_U_trun %*% image_gra_lamda_trun %*% t(image_gra_V_trun)
dim(restore_image_gra) # 결과 [1] 600 465
plot(0,0)
imageShow(restore_image_gra) # 600*5 + 5 + 5*465 = 5330 메모리가 저장하는데 사용됨(원본의 5,330/279,000*100=1.92%)


# 30개의 특잇값, 가장 많이 사용된 색 30개를 사용하여 그림을 그리기.
depth <- 30
image_gra_U_trun <- as.matrix(image_gra_U[,1:depth])
image_gra_V_trun <- as.matrix(image_gra_V[,1:depth])
image_gra_lamda_trun <- as.matrix(image_gra_lamda[1:depth,1:depth])
restore_image_gra <- image_gra_U_trun %*% image_gra_lamda_trun %*% t(image_gra_V_trun)
dim(restore_image_gra) # 결과 [1] 600 465
plot(0,0)
imageShow(restore_image_gra) # 600*30 + 30 + 30*465 = 31980 메모리가 저장하는데 사용됨(원본의 11.462%)


# 컬러 이미지로 근사
image_real <- readImage("C:/Users/User/Desktop/다변량통계 분석 및 실습/2장/pansy.jpg") # 사진 정보를 저장한다.
depth <- 100 # k = 100 으로 근사
for(i in 1:3){ # 3차원 배열 데이터라서 
  image_real_svd <- svd(image_real[,,i])
  image_real_svd_sigma <- diag(image_real_svd$d)
  image_real_svd_U <- image_real_svd$u
  image_real_svd_V <- image_real_svd$v
  image_real_trun_U <- as.matrix(image_real_svd_U[,1:depth]) # 절단 U 생성
  image_real_trun_V <- as.matrix(image_real_svd_V[,1:depth]) # 절단 V 생성
  image_real_trun_sigma <- as.matrix(image_real_svd_sigma[1:depth, 1:depth]) # 절단 sigma 생성
  # assign(변수, 값)함수 : 지정된 변수에 값을 대입 
  # paste(원소, 원손, ... , sep="")함수 : 각 원소를 설정된 공백으로 이어주는 함수
  assign(paste("ls",i,sep=""),image_real_trun_U %*% image_real_trun_sigma %*% t(image_real_trun_V))
}
ls <- array(c(ls1,ls2,ls3),c(nrow(ls1),ncol(ls1),3)) # 3차원 행렬로 다시 조합
plot(0,0)
imageShow(ls) # 그림 그리기