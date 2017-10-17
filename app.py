#!/Users/AkhilU/anaconda/bin/python

from flask import Flask
#import sys
#sys.path.append('/usr/lib/python2.7/dist-packages')
#sys.path.append('/usr/local/lib/python2.7/dist-packages/goose_extractor-1.0.25-py2.7.egg')
#sys.path.append('/usr/local/lib/python2.7/dist-packages')
from flask_cors import CORS, cross_origin
import mysql.connector
from flask import request, session
from flask import render_template, send_file, redirect
import datetime
import json
import base64

cnx = mysql.connector.connect(user='root', password='1234',host='127.0.0.1',database='dbmsproject');
cursor = cnx.cursor()

app = Flask(__name__)

app.secret_key = 'why would I tell you my secret key?'

app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
   return render_template('index.html')

@app.route("/img/contact.jpg")
def getcontactimage():
    return send_file('static/contact.jpg')

@app.route("/img/header.jpg")
def getheaderimage():
    return send_file('static/header.jpg')

@app.route('/static/bootstrap.css.map')
def getbootstrap():
    return send_file('static/bootstrap.css')

@app.route('/handle_login',methods=['POST'])
def handle_login():
    user = request.form['user']
    passwd = request.form['pass']
    passwd = base64.b64encode(passwd)
    session['user'] = user
    checkquery = ("SELECT * FROM AuthCred WHERE UserId= \'%s\'" % user)
    cursor.execute(checkquery)
    rs = cursor.fetchone()
    if rs[1]==passwd:
        if rs[2]==0:
            #return 'Successful admin login'
            return render_template('admin.html')
            #return redirect('/adminHome')
        elif rs[2]==1:
            #return 'Successful company login'
            return render_template('company.html')
            #return redirect('/companyHome')
    else:
        return 'Wrong login credentials'

@app.route('/handle_signup',methods=['POST'])
def handle_signup():
    encrypted_passwd = base64.b64encode(request.form['pass'])
    choice = request.form['usertype']
    if choice == 'Admin':
	checkquery = ("SELECT * FROM AuthCred WHERE UserID= \'%s\'" % request.form['user'])
	cursor.execute(checkquery)
	rs = cursor.fetchall()
	if cursor.rowcount == 0 and request.form['pass']==request.form['passconfirm']:
	    print "new record"
	    insertquery = ("Insert into AuthCred values (\'%s\',\'%s\',%d,\'%s\')" % (request.form['user'],encrypted_passwd,0,datetime.date.today()))
	    cursor.execute(insertquery)
	    insertquery = ("Insert into Staff values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" % (request.form['employeeid'],request.form['user'],request.form['role'],request.form['employeename'],request.form['roomno']))
	    cursor.execute(insertquery)
	    cnx.commit()
	    return 'Success'
	else:
	    return 'Error creating account'

    else:
	checkquery = ("SELECT * FROM AuthCred WHERE UserID= \'%s\'" % request.form['user'])
        cursor.execute(checkquery)
        rs = cursor.fetchall()
        if cursor.rowcount == 0 and request.form['pass']==request.form['passconfirm']:
            print "new record"
            insertquery = ("Insert into AuthCred values (\'%s\',\'%s\',%d,\'%s\')" % (request.form['user'],encrypted_passwd,1,datetime.date.today()))
            cursor.execute(insertquery)
	    companyid = request.form['companyname'][:8] + request.form['user'][:7]
	    insertquery = ("Insert into Company values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" % (companyid,request.form['user'],request.form['hrname'],request.form['hrphone'],request.form['companyname'],datetime.date.today(),request.form['companyindustry']))
	    cursor.execute(insertquery)
	    cnx.commit()
	    return 'Success'
	else:
	    return 'Error Creating Account'

@app.route('/adminHome')
def adminHome():
    if session.get('user'):
        return render_template('admin.html',user=session.get('user'))
    else:
        return 'Unauthorised access'
    #return 'haajhacksjh'

@app.route('/companyHome')
def companyHome():
    if session.get('user'):
        return render_template('company.html',user=session.get('user'))
    else:
        return 'Unauthorised access'

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
