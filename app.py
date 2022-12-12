import math
import json
from flask import Flask, render_template , request , redirect
from flask_mysqldb import MySQL
import datetime

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "123456"
app.config['MYSQL_DB'] = 'emirdb'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

#Adding new datas to realtime database and from realtime database to daily database.[Normal table and Daily table]

@app.route('/')

@app.route('/newcreatetable')
def gonewcreatetable():
    return render_template('newcreatetable.html')

@app.route('/newcreatetable' , methods=['POST'])
def newtablecreate():
    if request.method == 'POST':
        table_name = request.form['tablename']
        sorgu = """CREATE TABLE IF NOT EXISTS %s (
        id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        code varchar(191) NOT NULL,
        ip varchar(150) NOT NULL,
        date DATE,
        data json)""" % table_name
        cursor = mysql.connection.cursor()
        cursor.execute(sorgu)
        mysql.connection.commit()
        cursor.close()
        return redirect('/newcreatetable')

@app.route('/newcreate')
def gonewcreate():
    return render_template('newcreate.html')

@app.route('/newcreate' , methods = ['POST'])
def newcreate():
    if request.method == 'POST':
        now = datetime.datetime.now()
        code = request.form['code']
        data = request.form.getlist('data[]')
        date = now
        ip = request.form['ip']
        r = str(data).replace("'",'')
        arraydata = json.loads(r)
        cursor = mysql.connection.cursor()
        #for döngüsü ile array icindeki number değerlerini ayrı ayrı yazdırıyorum.
        for i in range(0,len(arraydata)):
            jsondata = json.dumps(arraydata[i])
            cursor.execute("""INSERT INTO jsontable (id,code,ip,date,data) VALUES(%s,%s,%s,%s,%s)""",(None,code,ip,date,jsondata))
        #sorgu = "INSERT INTO user VALUES(%s,%s,%s,%s,%s,%s,%s)"
        #cursor.execute("""INSERT INTO jsontable (id,code,ip,date,data) VALUES(%s,%s,%s,%s,%s)""",(None,code,ip,date,jsondata))
        mysql.connection.commit()
        cursor.close()
        return redirect('/newcreate')


@app.route('/getnewall')
def getnew_all():
    now = datetime.datetime.now()
    created_at = now.strftime('%Y-%m-%d')
    date = created_at
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM jsontable')
    #cursor.execute('SELECT code,data FROM jsontable WHERE date = %s',[date])
    veriler = list(cursor.fetchall())
    cursor.close()
    return render_template("/getnewall.html",datas=veriler)

@app.route('/getnewalldaily')
def getnew_alldaily():
    now = datetime.datetime.now() 
    created_at = now.strftime('%Y-%m-%d')
    date = created_at
    #WHERE columname BETWEEN '2012-12-25 00:00:00' AND '2012-12-25 23:59:59' BU sekilde kullanılmalı.
    #WHERE date_column >='2012-12-25' AND date_column <'2012-12-26  
    #query = """INSERT INTO jsontabledaily (id,code,ip,date,data) SELECT(id,code,ip,date,data) FROM jsontable"""
    #query2 = """insert INTO jsontabledaily(id,code,ip,date,data) SELECT id,code,ip,date,data FROM jsontable WHERE date = %s"""
    #dogru syntax bu.
    cursor = mysql.connection.cursor()
    #cursor.execute("""INSERT INTO jsontabledaily(id,code,ip,date,data) SELECT id,code,ip,date,data FROM jsontable WHERE date = %s""",[date])
    #cursor.execute('SELECT * FROM jsontabledaily')
    
    cursor.execute('SELECT id,code,ip,data FROM jsontable WHERE date = %s',[date])
    veriler = list(cursor.fetchall())
    codeList = []
    ipList = []
    for i in veriler:
        y = json.dumps(i)
        x = json.loads(y)
        codeList.append(x['code'])
        ipList.append(x['ip'])
    newList = []
    for i in codeList:
        if i in newList:
            pass
        else:
            newList.append(i)
    print(newList)
    ipNewList = []
    for i in ipList:
        if i in ipNewList:
            pass
        else:
            ipNewList.append(i)
    print(ipNewList)
    sqlList = []
    ipLastlist = []
    codeValue = ''
    ip = ''
    tarih = '2020-1-1'
    for i in range(0,len(newList)):
        for j in veriler:
            y = json.dumps(j)
            x = json.loads(y)
            if x['code'] == newList[i]:
                sqlList.append(x['data'])
                codeValue = x['code']
                ip = x['ip']
        cursor.execute('SELECT * FROM jsontable WHERE date = %s',[date])
        newVeriler = list(cursor.fetchall())
        for v in newVeriler:
            if v['code'] == codeValue:
                tarih = v['date']
        for p in newVeriler:
            if p['ip'] == ip:
                ip = p['ip']
        print(ip)
        print('son tarih:',tarih)
        datasNew = str(sqlList).replace("'","")
        print(codeValue)
        print(datasNew)
        print('type:',type(datasNew))
        cursor.execute("""INSERT INTO jsontabledaily(id,code,ip,date,data) VALUES (%s,%s,%s,%s,%s)""",(None,codeValue,ip,tarih,datasNew))
        sqlList = []
    #cursor.execute("""INSERT INTO jsontabledaily(id,code,ip,date,data) SELECT id,code,ip,date,data FROM jsontable WHERE date = %s""",[date])
    cursor.execute('SELECT * FROM jsontabledaily')   
    veriler = list(cursor.fetchall())
    cursor.close()
    return render_template('/getnewalldaily.html',datas=veriler)

################################################################

if __name__ == '__main__':
    app.run(debug=True)