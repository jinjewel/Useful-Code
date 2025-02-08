import sys
import pymysql

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
sql = """insert into test values(%s, %s, %s, %s)"""
s_ID = '1234123123'
s_fname = '난'
s_lname = '가상'
s_address = '없는광역시 남구 삼산동 808-11'

tup = (s_ID, s_fname, s_lname, s_address)
cur.execute(sql, tup)

# 데이터 저장하기
conn.commit()

# MySQL 닫기
cur.close()
conn.close()















