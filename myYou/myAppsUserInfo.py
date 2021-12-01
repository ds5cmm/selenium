import os
import sys
import re
import datetime
import time
import json
import pymysql
from flask import Flask, request, jsonify

hostname = "54.199.13.56"
#hostname = "127.0.0.1"
username = "soulway"
pwd = "plokijuh1@"
dbname = "soulway"

host_addr = "0.0.0.0"
port_num = "8081"

# in생성
def create_in(params):
    id = 0
    try:
        conn = pymysql.connect(user=username, password=pwd, host=hostname, db=dbname, charset='utf8')
        cur = conn.cursor()
        sql = "INSERT INTO TBL_IN ( id, nickname, name, mw, year, image ) VALUE (%s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (params['id'], params['nickname'], params['name'], params['mw'], params['year'], params['image']))
        conn.commit()
        conn.close()
        id = cur.lastrowid
    except Exception as e:
        print('예외가 발생했습니다.', e)
        return False, 0
    return True, id

# in수정
def update_in(params):
    try:
        conn = pymysql.connect(user=username, password=pwd, host=hostname, db=dbname, charset='utf8')
        cur = conn.cursor()
        sql = "UPDATE TBL_IN SET nickname = %s, name = %s, mw = %s, year = %s, image = %s WHERE id = %s AND seq = %s"
        cur.execute(sql, (params['nickname'], params['name'], params['mw'], params['year'], params['image'], params['id'], params['seq']))
        conn.commit()
        conn.close()
    except Exception as e:
        print('예외가 발생했습니다.', e)
        return False
    return True

# in삭제
def delete_in(params):
    try:
        conn = pymysql.connect(user=username, password=pwd, host=hostname, db=dbname, charset='utf8')
        cur = conn.cursor()
        sql = "DELETE FROM TBL_IN WHERE id = %s AND seq = %s" 
        cur.execute(sql, (params['id'], params['seq']))
        conn.commit()
        conn.close()
    except Exception as e:
        print('예외가 발생했습니다.', e)
        return False
    return True

# in단건조회
def select_in(params):
    try:
        conn = pymysql.connect(user=username, password=pwd, host=hostname, db=dbname, charset='utf8')
        cur = conn.cursor()
        sql = "SELECT * FROM TBL_IN WHERE id = %s AND seq = %s" 
        cur.execute(sql, (params['id'], params['seq']))
        row_headers=[x[0] for x in cur.description]
        rv = cur.fetchone()
        conn.close()
        return json.dumps(dict(zip(row_headers,rv)))
    except Exception as e:
        print('예외가 발생했습니다.', e)
        return ""
    return ""

# in여러건조회
def list_in(params):
    try:
        conn = pymysql.connect(user=username, password=pwd, host=hostname, db=dbname, charset='utf8')
        cur = conn.cursor()
        sql = "SELECT * FROM TBL_IN WHERE id = %s" 
        cur.execute(sql, (params['id']))
        row_headers=[x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data=[]
        for result in rv:
            row = dict(zip(row_headers,result))
            json_data.append(row)
        conn.close()
        return json.dumps(json_data)
    except Exception as e:
        print('예외가 발생했습니다.', e)
        return ""
    return ""

# yu생성
def create_yu(params):
    try:
        conn = pymysql.connect(user=username, password=pwd, host=hostname, db=dbname, charset='utf8')
        cur = conn.cursor()
        sql = "INSERT INTO TBL_YU ( id, inseq, gwangye, nickname, name, mw, year ) VALUE (%s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (params['id'], params['inseq'], params['gwangye'], params['nickname'], params['name'], params['mw'], params['year']))
        conn.commit()
        conn.close()
        id = cur.lastrowid
    except Exception as e:
        print('예외가 발생했습니다.', e)
        return False, 0
    return True, id

# yu수정
def update_yu(params):
    try:
        conn = pymysql.connect(user=username, password=pwd, host=hostname, db=dbname, charset='utf8')
        cur = conn.cursor()
        sql = "UPDATE TBL_YU SET gwangye = %s, nickname = %s, name = %s, mw = %s, year = %s, image = %s WHERE id = %s AND seq = %s "
        cur.execute(sql, (params['gwangye'], params['nickname'], params['name'], params['mw'], params['year'], params['image'], params['id'], params['seq']))
        conn.commit()
        conn.close()
    except Exception as e:
        print('예외가 발생했습니다.', e)
        return False
    return True

# yu삭제
def delete_yu(params):
    try:
        conn = pymysql.connect(user=username, password=pwd, host=hostname, db=dbname, charset='utf8')
        cur = conn.cursor()
        sql = "DELETE FROM TBL_YU WHERE id = %s AND seq = %s " 
        cur.execute(sql, (params['id'], params['seq']))
        conn.commit()
        conn.close()
    except Exception as e:
        print('예외가 발생했습니다.', e)
        return False
    return True

# yu단건조회
def select_yu(params):
    try:
        conn = pymysql.connect(user=username, password=pwd, host=hostname, db=dbname, charset='utf8')
        cur = conn.cursor()
        sql = "SELECT * FROM TBL_YU WHERE id = %s AND seq = %s " 
        cur.execute(sql, (params['id'], params['seq']))
        row_headers=[x[0] for x in cur.description]
        rv = cur.fetchone()
        conn.close()
        return json.dumps(dict(zip(row_headers,rv)))
    except Exception as e:
        print('예외가 발생했습니다.', e)
        return ""
    return ""

# yu여러건조회
def list_yu(params):
    try:
        conn = pymysql.connect(user=username, password=pwd, host=hostname, db=dbname, charset='utf8')
        cur = conn.cursor()
        sql = "SELECT * FROM TBL_YU WHERE id = %s AND inseq = %s" 
        cur.execute(sql, (params['id'], params['inseq']))
        row_headers=[x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data=[]
        for result in rv:
            row = dict(zip(row_headers,result))
            json_data.append(row)
        conn.close()
        return json.dumps(json_data)
    except Exception as e:
        print('예외가 발생했습니다.', e)
        return ""
    return ""

# te생성
def create_te(params):
    try:
        conn = pymysql.connect(user=username, password=pwd, host=hostname, db=dbname, charset='utf8')
        cur = conn.cursor()
        sql = "INSERT INTO TBL_TE ( id, inseq, gubun, bzgubun, name, juso, lng, lat, cheung ) VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (params['id'], params['inseq'], params['gubun'], params['bzgubun'], params['name'], params['juso'], params['lng'], params['lat'], params['cheung']))
        conn.commit()
        conn.close()
        id = cur.lastrowid
    except Exception as e:
        print('예외가 발생했습니다.', e)
        return False, 0
    return True, id

# te수정
def update_te(params):
    try:
        conn = pymysql.connect(user=username, password=pwd, host=hostname, db=dbname, charset='utf8')
        cur = conn.cursor()
        sql = "UPDATE TBL_TE SET gubun = %s, bzgubun = %s, name = %s, juso = %s, lng = %s, lat = %s, cheung = %s WHERE id = %s AND seq = %s "
        cur.execute(sql, (params['gubun'], params['bzgubun'], params['name'], params['juso'], params['lng'], params['lat'], params['cheung'], params['id'], params['seq']))
        conn.commit()
        conn.close()
    except Exception as e:
        print('예외가 발생했습니다.', e)
        return False
    return True

# te삭제
def delete_te(params):
    try:
        conn = pymysql.connect(user=username, password=pwd, host=hostname, db=dbname, charset='utf8')
        cur = conn.cursor()
        sql = "DELETE FROM TBL_TE WHERE id = %s AND seq = %s " 
        cur.execute(sql, (params['id'], params['seq']))
        conn.commit()
        conn.close()
    except Exception as e:
        print('예외가 발생했습니다.', e)
        return False
    return True

# te단건조회
def select_te(params):
    try:
        conn = pymysql.connect(user=username, password=pwd, host=hostname, db=dbname, charset='utf8')
        cur = conn.cursor()
        sql = "SELECT * FROM TBL_TE WHERE id = %s AND seq = %s " 
        cur.execute(sql, (params['id'], params['seq']))
        row_headers=[x[0] for x in cur.description]
        rv = cur.fetchone()
        conn.close()
        return json.dumps(dict(zip(row_headers,rv)))
    except Exception as e:
        print('예외가 발생했습니다.', e)
        return ""
    return ""

# te여러건조회
def list_te(params):
    try:
        conn = pymysql.connect(user=username, password=pwd, host=hostname, db=dbname, charset='utf8')
        cur = conn.cursor()
        sql = "SELECT * FROM TBL_TE WHERE id = %s AND inseq = %s" 
        cur.execute(sql, (params['id'], params['inseq']))
        row_headers=[x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data=[]
        for result in rv:
            row = dict(zip(row_headers,result))
            json_data.append(row)
        conn.close()
        return json.dumps(json_data)
    except Exception as e:
        print('예외가 발생했습니다.', e)
        return ""
    return ""

# bz생성
def create_bz(params):
    try:
        conn = pymysql.connect(user=username, password=pwd, host=hostname, db=dbname, charset='utf8')
        cur = conn.cursor()
        sql = "INSERT INTO TBL_BZ ( inseq, id, gubun, eopjong, name, bzno, bir, image ) VALUE (%s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (params['inseq'], params['id'], params['gubun'], params['eopjong'], params['name'], params['bzno'], params['bir'], params['image']))
        conn.commit()
        conn.close()
        id = cur.lastrowid
    except Exception as e:
        print('예외가 발생했습니다.', e)
        return False, 0
    return True, id

# bz수정
def update_bz(params):
    try:
        conn = pymysql.connect(user=username, password=pwd, host=hostname, db=dbname, charset='utf8')
        cur = conn.cursor()
        sql = "UPDATE TBL_BZ SET gubun = %s, eopjong = %s, name = %s, bzno = %s, bir = %s, image = %s WHERE id = %s AND seq = %s "
        cur.execute(sql, (params['gubun'], params['eopjong'], params['name'], params['bzno'], params['bir'], params['image'], params['id'], params['seq']))
        conn.commit()
        conn.close()
    except Exception as e:
        print('예외가 발생했습니다.', e)
        return False
    return True

# bz삭제
def delete_bz(params):
    try:
        conn = pymysql.connect(user=username, password=pwd, host=hostname, db=dbname, charset='utf8')
        cur = conn.cursor()
        sql = "DELETE FROM TBL_BZ WHERE id = %s AND seq = %s " 
        cur.execute(sql, (params['id'], params['seq']))
        conn.commit()
        conn.close()
    except Exception as e:
        print('예외가 발생했습니다.', e)
        return False
    return True

# bz단건조회
def select_bz(params):
    try:
        conn = pymysql.connect(user=username, password=pwd, host=hostname, db=dbname, charset='utf8')
        cur = conn.cursor()
        sql = "SELECT * FROM TBL_BZ WHERE id = %s AND seq = %s " 
        cur.execute(sql, (params['id'], params['seq']))
        row_headers=[x[0] for x in cur.description]
        rv = cur.fetchone()
        conn.close()
        return json.dumps(dict(zip(row_headers,rv)))
    except Exception as e:
        print('예외가 발생했습니다.', e)
        return ""
    return ""

# bz여러건조회
def list_bz(params):
    try:
        conn = pymysql.connect(user=username, password=pwd, host=hostname, db=dbname, charset='utf8')
        cur = conn.cursor()
        sql = "SELECT * FROM TBL_BZ WHERE id = %s AND inseq = %s" 
        cur.execute(sql, (params['id'], params['inseq']))
        row_headers=[x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data=[]
        for result in rv:
            row = dict(zip(row_headers,result))
            json_data.append(row)
        conn.close()
        return json.dumps(json_data)
    except Exception as e:
        print('예외가 발생했습니다.', e)
        return ""
    return ""

# HTTP Server
app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/c_in",methods=["POST"])
def c_in():
    params = request.get_json()
    result, id= create_in(params)
    return {"success":result, "seq":id}

@app.route("/r_in",methods=["POST"])
def r_in():
    params = request.get_json()
    result= select_in(params)
    
    return result

@app.route("/u_in",methods=["POST"])
def u_in():
    params = request.get_json()
    result= update_in(params)
    return {"success":result}

@app.route("/d_in",methods=["POST"])
def d_in():
    params = request.get_json()
    result= delete_in(params)
    return {"success":result}

@app.route("/l_in",methods=["POST"])
def l_in():
    params = request.get_json()
    result= list_in(params)
    return result

@app.route("/c_yu",methods=["POST"])
def c_yu():
    params = request.get_json()
    result, id = create_yu(params)
    return {"success":result, "seq":id}

@app.route("/r_yu",methods=["POST"])
def r_yu():
    params = request.get_json()
    result= select_yu(params)
    return result

@app.route("/u_yu",methods=["POST"])
def u_yu():
    params = request.get_json()
    result= update_yu(params)
    return {"success":result}

@app.route("/d_yu",methods=["POST"])
def d_yu():
    params = request.get_json()
    result= delete_yu(params)
    return {"success":result}

@app.route("/l_yu",methods=["POST"])
def l_yu():
    params = request.get_json()
    result= list_yu(params)
    return result

@app.route("/c_te",methods=["POST"])
def c_te():
    params = request.get_json()
    result, id = create_te(params)
    return {"success":result, "seq":id}

@app.route("/r_te",methods=["POST"])
def r_te():
    params = request.get_json()
    result= select_te(params)
    return result

@app.route("/u_te",methods=["POST"])
def u_te():
    params = request.get_json()
    result= update_te(params)
    return {"success":result}

@app.route("/d_te",methods=["POST"])
def d_te():
    params = request.get_json()
    result= delete_te(params)
    return {"success":result}

@app.route("/l_te",methods=["POST"])
def l_te():
    params = request.get_json()
    result= list_te(params)
    return result

@app.route("/c_bz",methods=["POST"])
def c_bz():
    params = request.get_json()
    result, id = create_bz(params)
    return {"success":result, "seq":id}

@app.route("/r_bz",methods=["POST"])
def r_bz():
    params = request.get_json()
    result= select_bz(params)
    return result

@app.route("/u_bz",methods=["POST"])
def u_bz():
    params = request.get_json()
    result= update_bz(params)
    return {"success":result}

@app.route("/d_bz",methods=["POST"])
def d_bz():
    params = request.get_json()
    result= delete_bz(params)
    return {"success":result}

@app.route("/l_bz",methods=["POST"])
def l_bz():
    params = request.get_json()
    result= list_bz(params)
    return result

@app.route("/",methods=["POST"])
def alive():
    
    now = datetime.datetime.now()
    print('>>>>>>>>>>>>>> alive time  : '+ str(now))
    return {"success":"true"}

if __name__ == "__main__":

    app.run(host=host_addr, port=port_num)


