#!/Users/AkhilU/anaconda/bin/python

from flask import Flask
#import sys
#sys.path.append('/usr/lib/python2.7/dist-packages')
#sys.path.append('/usr/local/lib/python2.7/dist-packages/goose_extractor-1.0.25-py2.7.egg')
#sys.path.append('/usr/local/lib/python2.7/dist-packages')
from flask_cors import CORS, cross_origin
import mysql.connector
from flask import request, session
from flask import render_template, send_file, redirect, jsonify
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
            #return render_template('admin.html')
            return redirect('/adminHome')
        elif rs[2]==1:
            #return 'Successful company login'
            #return render_template('company.html')
            return redirect('/companyHome')
    else:
        return 'Wrong login credentials'

@app.route('/handle_newcourse',methods=['POST'])
def handle_newcourse():
    try:
        query = ("Insert into Program values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" % (request.form['id'],request.form['name'],request.form['description'],request.form['duration'],request.form['start'],request.form['supervisor']))
        cursor.execute(query)
        cnx.commit()
        return 'Success'
    except:
        return 'Failure'

@app.route('/handle_newtrainee',methods=['POST'])
def handle_newtrainee():
    try:
        user=session.get('user')
        query = ("SELECT companyId FROM Company WHERE userID = \'%s\'" % (user))
        cursor.execute(query)
        rs= cursor.fetchone()
        companyid = rs[0]
        query = ("Insert into Trainee values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',NULL,NULL)" % (companyid, request.form['id'],request.form['name'],request.form['phone'],request.form['residence'],request.form['street'],request.form['zipcode']))
        print query
        cursor.execute(query)
        print 'hi'
        cnx.commit()
        return 'Success'
    except:
        return 'Failure'

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

@app.route('/getIds')
def getIds():
    # try:
    if session.get('user'):
        cursor.execute("SELECT * FROM Program");
        ids = cursor.fetchall()

        wishes_dict = []
        for wish in ids:
            wish_dict = {
                    'Id': wish[0],
                    'Name': wish[1],
                    'Description': wish[2],
                    'Duration':wish[3],
                    'Start_Date':wish[4]}
            wishes_dict.append(wish_dict)

        cursor.execute("SELECT * FROM Company");
        ids = cursor.fetchall()

        companies_dict = []
        for company in ids:
            company_dict = {
                    'Id': company[0],
                    'Name': company[4],
                    'Uid': company[1],
                    'POCname':company[2],
                    'POCnum':company[3],
                    'Ind':company[6],
                    'Regdate':"{:%B %d, %Y}".format(company[5])}
            companies_dict.append(company_dict)

        data = {}
        data['progs'] = wishes_dict
        data['comps'] = companies_dict

        return json.dumps(data)
    else:
        return 'random'
    # except Exception as e:
    #     return 'random11'

@app.route('/getPrograms')
def getPrograms():
    # try:
    if session.get('user'):
        cursor.execute("SELECT * FROM Program");
        ids = cursor.fetchall()

        wishes_dict = []
        for wish in ids:
            wish_dict = {
                    'Id': wish[0],
                    'Name': wish[1],
                    'Description': wish[2],
                    'Duration':wish[3],
                    'Start_Date':wish[4]}
            wishes_dict.append(wish_dict)
        #return 'hi'

        user = session.get('user')

        query = ("SELECT companyId FROM Company WHERE userID = \'%s\'" % (user))
        cursor.execute(query)
        rs= cursor.fetchone()
        companyid = rs[0]

        query = ("SELECT b.program_name, a.* FROM Trainee a left join Program b on a.programId=b.programId WHERE a.companyId = \'%s\'" %(companyid))
        cursor.execute(query)
        trs = cursor.fetchall()

        trainees_dict = []
        for trainee in trs:
            train_dict = {
                    'ProgramId':trainee[2],
                    'Name':trainee[3],
                    'TraineeId':trainee[8],
                    'Phone':trainee[4],
                    'Grade':trainee[9]}
            trainees_dict.append(train_dict)

        data = {}
        data['progs'] = wishes_dict
        data['trains'] = trainees_dict
        return json.dumps(data)
    else:
        return 'random'
    # except Exception as e:
    #     return 'random11'

@app.route('/test',methods=['POST','GET'])
def test():
    try:
        data = json.loads(request.data)
        query = ("DELETE FROM Program WHERE programId=\'%s\'" %(data.get('id')))
        cursor.execute(query)
        cnx.commit()
        return 'Success'
    except:
        return 'Failure'

@app.route('/gettrainees',methods=['POST','GET'])
def gettrainees():
    data = json.loads(request.data)
    query = ("SELECT * FROM Trainee WHERE programId=\'%s\'" %(data.get('id')))
    cursor.execute(query)
    trs = cursor.fetchall()

    trainees_dict = []
    for trainee in trs:
        train_dict = {
                'ProgramId':trainee[1],
                'Name':trainee[2],
                'TraineeId':trainee[7],
                'Phone':trainee[3],
                'Grade':trainee[8]}
        trainees_dict.append(train_dict)
    return json.dumps(trainees_dict)

@app.route('/gradechange',methods=['POST','GET'])
def gradechange():
    print request.form['id']
    query = ("UPDATE Trainee SET Grade=\'%c\' WHERE traineeId=\'%s\'" %(request.form['grade'],request.form['id']))
    cursor.execute(query)
    cnx.commit();
    return 'Success'

@app.route('/removetrainee',methods=['POST','GET'])
def removetrainee():
    try:
        data = json.loads(request.data)
        query = ("DELETE FROM Trainee WHERE traineeId=%d" %(data.get('id')))
        cursor.execute(query)
        cnx.commit()
        return 'Success'
    except:
        return 'Failure'

if __name__ == '__main__':
    app.run(debug=True)
