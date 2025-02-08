import sys
import pymysql
import openpyxl

# 데이터(엑셀) 주소 불러오기
wb = openpyxl.load_workbook('C:/Users/User/Desktop/test.xlsx')

# 데이터가 들어있는 시트 설정
sheet_1 = wb['Sheet1'] # 시트 가지고 오기

# 연결자 생성
conn = pymysql.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'jj35909825*',
    db = 'test',
    charset = 'utf8')

# 커서 생성
cur = conn.cursor(pymysql.cursors.DictCursor)

# 데이터 입력하기

sql = """insert into test values(%s, %s, %s, %s)""" # 입력할 SQL 형식 

for rows in sheet_1.iter_rows(): # 차례대로 A,B,C ... 증가
    s_list = [] # 값을 저장할 list 선언
    for cell in rows: # 차례대로 1, 2, 3, ... 증가
        # A1, A2, ... , 마지막 행 데이터 차례로 출력
        # print(cell.value, end=" ")
        s_list.append(cell.value) # 행 데이터를 차례로 리스트에 저장
    print(s_list) # 입력할 데이터 행 출력    
    tup = tuple(s_list) # MySql로 데이터를 넣기 위해 tuple로 형변환(캐스팅)
    cur.execute(sql, tup) # MySql의 table로 데이터 삽입

# 데이터 저장하기
conn.commit()

# MySQL 닫기
cur.close()
conn.close()