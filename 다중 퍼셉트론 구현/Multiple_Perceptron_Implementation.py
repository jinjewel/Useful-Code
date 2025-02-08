#  OR, NAND, AND 구현을 통해 다층 퍼셉트론 구현


# 필요한 라이브러리 선언
import numpy as np 


# AND 게이트 (1,1,-0.5)
def AND(x1, x2):
    # 2개의 입력값과 2개의 가중치(1, 1) 생성
    x = np.array([x1, x2]) # input
    w = np.array([1, 1]) # weight
    b = -1.5 # bias(1) * bias weight(-1.5)
    
    # 활성함수에 들어갈 값 계산
    temp = np.sum(x * w) + b
    
    # 활성함수 대입 후 결과 반환
    if temp > 0:
        return 1
    else:
        return 0


# OR 게이트 (1,1,-1.5)
def OR(x1, x2):
    # 2개의 입력값과 2개의 가중치(1, 1) 생성
    x = np.array([x1, x2]) # input
    w = np.array([1, 1]) # weight
    b = -0.5 # bias(1) * bias weight(-0.5)

    # 활성함수에 들어갈 값 계산
    temp = np.sum(x * w) + b
    
    # 활성함수 대입 후 결과 반환
    if temp > 0:
        return 1
    else:
        return 0


# NAND 게이트 (-1,-1,1.5)
def NAND(x1, x2):
    # 2개의 입력값과 2개의 가중치(-1, -1) 생성
    x = np.array([x1, x2]) # input
    w = np.array([-1, -1]) # weight
    b = 1.5 # bias(1) * bias weight(1.5)

    # 활성함수에 들어갈 값 계산
    temp = np.sum(x * w) + b
    
    # 활성함수 대입 후 결과 반환
    if temp > 0:
        return 1
    else:
        return 0


# XOR 게이트
def XOR(x1, x2):
    s1 = OR(x1, x2) # OR 함수
    s2 = NAND(x1, x2) # NAND 함수
    y = AND(s1, s2) # AND 함수
    return y


# 입력과 출력 결과 출력
print("x1 x2  y")
print("----------------")
print("0   0  %d" % (XOR(0, 0)))
print("0   1  %d" % (XOR(0, 1)))
print("1   0  %d" % (XOR(1, 0)))
print("1   1  %d" % (XOR(1, 1)))