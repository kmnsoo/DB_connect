# 라이브러리 import
import os, sys, time
import requests
from bs4 import BeautifulSoup
import mariadb
import json


# 파이썬과 데이터 베이스 연결을 위해 DB와 connet를 해주어야 한다. mariaDB를 사용하였다.
# 인자로는 호스트 값, 유저 ,패스워드 등을 넣는다.
conn = mariadb.connect(host="260.267.161.**", user="user", password="password**", port=32**, db="funding")
curs = conn.cursor()

sql_insert  = "insert into cm_invest_goods(loan_id, invest_date, title, period, target_amount, c_datetime)"
sql_insert += "values(%s, %s, %s, %s, %s, now())"

sql_select = "select loan_id from cm_invest_goods"

# 데이터 제거 함수
def delete(p_no):

    # sql_delete  = " DELETE FROM cm_invest_goods "
    # sql_delete += " WHERE invest_date < curdate() "

    sql_delete  = " DELETE FROM press "
    sql_delete += " WHERE p_no = %s "

    try:
        curs.execute(sql_delete, (p_no))
        conn.commit()
    # 예외 처리.     
    except:
        print("deleteGoods Unexpected error:" + str(sys.exc_info()[0]))

    sql_delete  = " DELETE FROM cm_invest_info "
    sql_delete += " WHERE invest_date < curdate() "

    try:
        curs.execute(sql_delete, ())
        conn.commit()
    except:
        print("deleteInvestInfo Unexpected error:" + str(sys.exc_info()[0]))

# 데이터 입력 함수
def insertGoods(loan_id, invest_date, title, period, target_amount):
    
    try:
        curs.execute(sql_insert, (loan_id, invest_date, title, period, target_amount))
        conn.commit()
    except:
        # 예외처리 요청 대로 처리 할 시 try 수행. 하지만 그렇지 않을 때 예외 처리를 해준다. 
        # 데이터 입력 함수 실행 후 예외 처리 시에 오류 발생시 데이터가 꼬일 수 있어서 롤백 처리를 해준다.
        #conn.rollback()
        print("insertGoods Unexpected error:" + str(sys.exc_info()[0]))

# 데이터 조회 함수 
def selectGoods(sql):
    rows={}
    # sql_select = "select * from press"
    try:
        curs.execute(sql)
        rows = curs.fetchall()
        
    except:
        print("selectGoods Unexpected error:" + str(sys.exc_info()[0]))

    return rows

# 메인 함수. 위에 작성한 CRUD 함수를 호출하여 요청을 실행한다.
if __name__ == "__main__":

    sql = 'select * from press'

    insert_goods_list = selectGoods(sql)
    print('insert_goods_list ==> ', insert_goods_list)
    if insert_goods_list[0]['p_no'] == 1:
        delete(insert_goods_list[0]['p_no'])

    sql = 'select * from company'
    insert_goods_list2 = selectGoods(sql)
    

    # insertGoods(loan_id, invest_date, title, period, target_amount)
    
    # 쿼리 1번 실행 후 메모리 효율을 위해 종료.
    conn.close()