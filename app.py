from re import S
from typing import ValuesView
from flask import Flask, render_template, request, redirect, session, flash, get_flashed_messages, url_for
from flask import url_for
from flask_mysqldb import MySQL, MySQLdb
import bcrypt

import MySQLdb.cursors
from flask_bootstrap import Bootstrap
from flask import *
from flask_mail import *
from random import *
from array import *

app = Flask(__name__)

app.secret_key = "caircocoders-ednalan-2020"


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sportsdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


mail = Mail(app)
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'prathibhapoojary75@gmail.com'
app.config['MAIL_PASSWORD'] = 'welcome123@'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
otp = randint(000000, 999999)


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']
        check= request.form['radio']
        admin="admin"
        staff="staff"
        student="student"
        if check == admin:
            aid="101"
            aemail="admin@gmail.com"
            apassword="admin"
            if (id==aemail and password==apassword):
                return redirect(url_for('adminpanel'))
            else:
                flash('password and email does not match','error')
                return render_template("login.html")
                
      
        if check == staff:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM staff WHERE staffid=%s",(id,))
            suser = cur.fetchone()
            cur.close()
            if (len(suser)>0):
                if (password==suser['password']):
                    session['staffid'] = suser['staffid']
                    # smail=suser['email']
                    # return render_template("staffpanel.html",smail=smail)
                    return render_template("staffpanel.html")
                else:
                    flash('password and email does not match')
                    return render_template("login.html")
            else:
                flash('user not found')
                return render_template("login.html")
        
        if check == student:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM student WHERE rollno=%s", (id,))
            stuser = cur.fetchone()
            cur.close()
            if (len(stuser)>0):
                session['rollno']=stuser['rollno']
                # studemail=stuser['email']
                if (password==stuser['password']):
                    return render_template("studpanel.html")
                else:
                    flash('password and email does not match')
                    return render_template("login.html")
            else:
                flash('user not found')
                return render_template("login.html")
    return render_template("login.html")

@app.route('/admin-panel', methods=['GET','POST'])
def adminpanel():
    return render_template('adminpanel.html')

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/forgotpassword')
def forgotpassword():
    return render_template("setpassword.html")


@app.route('/verify', methods=["POST", "GET"])
def verify():
    email = request.form["email"]
    msg = Message('OTP', sender='prathibhapoojary55@gmail.com',
                  recipients=[email])
    msg.body = str(otp)
    mail.send(msg)
    se = email
    return render_template('verify.html', otp=otp, se=se)


@app.route('/validate/<se>/<otp>', methods=["POST", "GET"])
def validate(se, otp):
    if request.method == 'POST':
        sotp = otp
        user_otp = request.form.get('otp')
        print(user_otp)
        if sotp == user_otp:
            return render_template("password.html", se=se)
        else:
            flash('OTP doesnot match')
            return redirect('/forgotpassword')


@app.route('/pwupdate/<se>', methods=["POST", "GET"])
def pwupdate(se):
    if request.method == 'POST':
        password = request.form['password']
        check= request.form['radio']
        staff="staff"
        student="student"
        password = request.form['password']
        if check == staff:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE staff SET password=%s WHERE email=%s",(password, se,))
            mysql.connection.commit()
            flash('password updated successfuly')
            return render_template("login.html")
        if check == student:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE student SET password=%s WHERE email=%s",(password, se,))
            mysql.connection.commit()
            flash('password updated successfuly')
            return render_template("login.html")


# @app.route('/loginform', methods=["GET", "POST"])
# def loginform():
#     if request.method == 'POST':
#         id = request.form['id']
#         password = request.form['password']
#         check= request.form['radio']
#         admin="admin"
#         staff="staff"
#         student="student"
#         if check == admin:
#             aemail="admin@gmail.com"
#             apassword="admin"
#             if (id==aemail and password==apassword):
#                 return render_template("adminpanel.html")
#             else:
#                 flash('password and email does not match','error')
#                 return render_template("login.html")
                
      
#         if check == staff:
#             cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#             cur.execute("SELECT * FROM staff WHERE staffid=%s",(id,))
#             suser = cur.fetchone()
#             cur.close()
#             if (len(suser)>0):
#                 if (password==suser['password']):
#                     session['staffid'] = suser['staffid']
#                     # smail=suser['email']
#                     # return render_template("staffpanel.html",smail=smail)
#                     return render_template("staffpanel.html")
#                 else:
#                     flash('password and email does not match')
#                     return render_template("login.html")
#             else:
#                 flash('user not found')
#                 return render_template("login.html")
        
#         if check == student:
#             cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#             cur.execute("SELECT * FROM student WHERE rollno=%s", (id,))
#             stuser = cur.fetchone()
#             cur.close()
#             if (len(stuser)>0):
#                 session['rollno']=stuser['rollno']
#                 # studemail=stuser['email']
#                 if (password==stuser['password']):
#                     return render_template("studpanel.html")
#                 else:
#                     flash('password and email does not match')
#                     return render_template("login.html")
#             else:
#                 flash('user not found')
#                 return render_template("login.html")
#     else:
#         return render_template("login.html") 

@app.route('/sback')
def sback():
    return render_template("staffpanel.html")

@app.route('/stback')
def stback():
    return render_template("studpanel.html")

@app.route('/studregister', methods=["GET", "POST"])
def studregister():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        rollno = request.form['rollno']
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        qry = f"INSERT INTO `student` (`name`, `rollno`, `email`, `password`) VALUES ('{name}', '{rollno}', '{email}', '{password}')"
        # qry=f("INSERT INTO student (name, rollno, email, password) VALUES (%s,%s,%s,%s)",
                    # (name, rollno,email,password,))
        res = cur.execute(qry) 
        mysql.connection.commit()
        if res:
            return render_template('success.html', msg="Registration successful")
        else:
            return render_template('failure.html', msg="registration failed")
    #     flash('you were successfully registered')
    # return render_template("login.html")

@app.route('/staffregister', methods=["GET", "POST"])
def staffregister():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        staffid = request.form['staffid']
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        qry = f"INSERT INTO `staff` (`name`, `staffid`, `email`, `password`) VALUES ('{name}', '{staffid}', '{email}', '{password}')"
      
        res = cur.execute(qry) 
        mysql.connection.commit()
        if res:
            return render_template('success.html', msg="Registration successful")
        else:
            return render_template('failure.html', msg="registration failed")
        # cur.execute("INSERT INTO staff (name, staffid, email, password) VALUES (%s,%s,%s,%s)",
        #             (name,staffid,email,password,))
        # mysql.connection.commit()
        # flash('You were successfully registered')
        # return render_template("login.html")

#regulargames
@app.route('/regulargames')
def regulargames():
    return render_template("regulargames.html")

@app.route('/addgames', methods=["GET", "POST"])
def addgames():
    if request.method == 'GET':
        return render_template("addgames.html")
    else:
        games = request.form['games']
        rules = request.form['rules']
        duration = request.form['duration']
        equipments = request.form['equipments']
        singles = request.form['singles']
        doubles = request.form['doubles']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO regulardb (gamesname,rules,duration,singles,doubles,equipments) VALUES (%s,%s,%s,%s,%s,%s)",
                    (games, rules, duration,singles,doubles,equipments,))
        mysql.connection.commit()
        flash('successfully added')
        return render_template("regulargames.html")

@app.route('/updategames')
def updategames():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM regulardb")
        data = cur.fetchall()
        if data:
            return render_template("updategames.html", data=data)


@app.route('/edit/<gameid>/', methods=["POST", "GET"])
def edit(gameid):
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM regulardb WHERE gameid=%s", (gameid,))
        mysql.connection.commit()
        data = cur.fetchone()
        return render_template("editgames.html", value=data)


@app.route('/update/<gameid>/', methods=["GET", "POST"])
def update(gameid):
    if request.method == 'POST':
        gameid = request.form.get('gameid')
        games = request.form.get('games')
        rules = request.form.get('rules')
        duration = request.form.get('duration')
        equipments = request.form.get('equipments')
        singles = request.form.get('singles')
        doubles = request.form.get('doubles')
        cur = mysql.connection.cursor()
        cur.execute("UPDATE regulardb SET gamesname=%s,rules=%s,duration=%s,equipments=%s,singles=%s,doubles=%s WHERE gameid=%s",
        (games,rules,duration,equipments,singles,doubles,gameid,))
        mysql.connection.commit()
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM regulardb")
        data = cur.fetchall()
        if data:
            flash('successfully updated')
            # return render_template("adminpanel.html", data=data)
            return redirect(url_for('.updategames'))
        
    else:

        return render_template("editgames.html")


@app.route('/deleteevent/<gameid>/', methods=["POST", "GET"])
def deleteevent(gameid):
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM regulardb WHERE gameid=%s", (gameid,))
        mysql.connection.commit()
        flash('successfully deleted')
        return redirect(url_for('.updategames'))

@app.route('/viewregstud')
def viewregstud():
     if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM regulargamebooking")
        data = cur.fetchall()
        return render_template("viewregularstud.html",data=data)

#specialevent
@app.route('/specialevent')
def specialevent():
    return render_template("specialevent.html")

@app.route('/addevent', methods=["GET", "POST"])
def addevent():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        scur = mysql.connection.cursor()
        cur.execute("SELECT * FROM regulardb")
        scur.execute("SELECT staffid FROM staff")
        sdata=scur.fetchall()
        data = cur.fetchall()
        if data:   
            return render_template("addevent.html",data=data,sdata=sdata)
    else:

        name = request.form['name']
        gamename = request.form['gameid']
        venue = request.form['venue']
        type = request.form['type']
        rules = request.form['rules']
        staff = request.form['staff']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        time = request.form['time']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO special_event (specialname,gameid,venue,type,specialeventrules,staffid,startdate,enddate,starttime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (name,gamename, venue, type,rules,staff,startdate,enddate,time,))
        mysql.connection.commit()
        flash(' successfully added')
        return render_template("specialevent.html")

@app.route('/updateevent', methods=['GET','POST'])
def updateevent():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM special_event")
    data = cur.fetchall()
    return render_template("updateevent.html", data=data)

@app.route('/editt/<eventid>/', methods=["POST", "GET"])
def editt(eventid):
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM special_event WHERE eventid=%s", (eventid,))
        mysql.connection.commit()
        data = cur.fetchone()
        return render_template("editevent.html", value=data)


@app.route('/updatee/<eventid>/', methods=["GET", "POST"])
def updatee(eventid):
    if request.method == 'POST':
        eventid = request.form.get('eventid')
        name = request.form.get('name')
        # gameid = request.form.get('gameid')
        venue = request.form.get('venue')
        type = request.form.get('type')
        rules = request.form.get('rules')
        staff = request.form.get('staff')
        startdate = request.form.get('startdate')
        enddate = request.form.get('enddate')
        starttime = request.form.get('time')
        cur = mysql.connection.cursor()
        cur.execute("UPDATE special_event SET specialname=%s,venue=%s,type=%s,specialeventrules=%s,staffid=%s,startdate=%s,enddate=%s,starttime=%s WHERE eventid=%s",
        (name,venue, type, rules,staff,startdate,enddate,starttime, eventid,))
        mysql.connection.commit()
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM special_event")
        data = cur.fetchall()
        if data:
            flash('successfully updated')
            return redirect(url_for('.updateevent'))
    else:
            return render_template("editevent.html")

@app.route('/deleteeventt/<eventid>/', methods=["POST", "GET"])
def deleteeventt(eventid):
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM special_event WHERE eventid=%s", (eventid,))
        mysql.connection.commit()
        flash('successfully deleted')
        return redirect(url_for('.updateevent'))


@app.route('/viewsplregstud', methods=['GET','POST'])
def viewsplregstud():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM special_reg")
    data = cur.fetchall()
    return render_template("viewspecialstud.html",data=data)


#sportsday
@app.route('/sportsdayevent', methods=['GET','POST'])
def sportsdayevent():
    return render_template("sportsdayevent.html")

@app.route('/addspevent', methods=["GET", "POST"])
def addspevent():
    if request.method == 'GET':
        return render_template("addspevent.html")
    else:
        name = request.form['sname']
        type = request.form['type']
        rules = request.form['rules']        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO sports_event (sportsname,type,rule) VALUES (%s,%s,%s)",(name, type,rules,))
        mysql.connection.commit()
        flash(' successfully added')
        return render_template("sportsdayevent.html")



@app.route('/updatespevent')
def updatespevent():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM sports_event")
        data = cur.fetchall()
        if data:
            return render_template("updatespevent.html", data=data)


@app.route('/sedit/<sports_eventid>/', methods=["POST", "GET"])
def sedit(sports_eventid):
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM sports_event WHERE sports_eventid=%s", (sports_eventid,))
        mysql.connection.commit()
        data = cur.fetchone()
        return render_template("editsevent.html", value=data)


@app.route('/supdate/<sports_eventid>/', methods=["GET", "POST"])
def supdate(sports_eventid):
    if request.method == 'POST':
        sports_eventid = request.form.get('sports_eventid')
        name = request.form.get('sname')
        type = request.form.get('type')
        rules = request.form.get('rule')
        cur = mysql.connection.cursor()
        cur.execute("UPDATE sports_event SET sportsname=%s,type=%s,rule=%s WHERE sports_eventid=%s",(name, type, rules, sports_eventid,))
        mysql.connection.commit()
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM sports_event")
        data = cur.fetchall()
        if data:
            flash('successfully updated')
            # return render_template("adminpanel.html", data=data)
            return redirect(url_for('.updatespevent'))
    else:
        return render_template("editsevent.html")


@app.route('/sdeleteevent/<sports_eventid>/', methods=["POST", "GET"])
def sdeleteevent(sports_eventid):
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM sports_event WHERE sports_eventid=%s", (sports_eventid,))
        mysql.connection.commit()
        flash('successfully deleted')
        return redirect(url_for('.updatespevent'))


@app.route('/createevent')
def createevent():
    if request.method == 'GET':
        dcur = mysql.connection.cursor()
        dcur.execute("SELECT * FROM sports_event")
        ddata = dcur.fetchall()
        print(ddata)
        dcur.close() 
        if ddata:
            return render_template("creategames.html",ddata=ddata)

@app.route('/create', methods=["GET", "POST"])
def create():   
    if request.method == 'POST':
        grules=request.form['rules']
        date=request.form['date']
        time=request.form['time']
        venue=request.form['venue']
        sportsid=request.form['sportsid']
        games=[]
        for games in request.form.getlist('games'):
            print(games)
            cur = mysql.connection.cursor()
            cur.execute("UPDATE sports_event SET  sportsevents='1' WHERE  sportsname='{}'".format(games))
            mysql.connection.commit()  
            acur = mysql.connection.cursor()
        acur.execute("UPDATE sports_event SET sportsid=%s,grules=%s,date=%s,time=%s,venue=%s  WHERE sportsevents='1'",(sportsid,grules,date,time,venue,))
        mysql.connection.commit()             
        dcur = mysql.connection.cursor()
        fcur = mysql.connection.cursor()
        gcur=mysql.connection.cursor()
        dcur.execute("SELECT DISTINCT type FROM sports_event")
        fcur.execute("SELECT staffid FROM staff")
        gcur.execute("SELECT staffid FROM staff")
        ddata = dcur.fetchall()
        fdata = fcur.fetchall()
        gdata = gcur.fetchall()
        dcur.close() 
        if ddata:
            return render_template("assignstaff.html",ddata=ddata,fdata=fdata,gdata=gdata)

@app.route('/assign', methods=["GET", "POST"])    
def assign():
    if request.method == 'POST':
        type=request.form['type']
        linejudge=request.form['linejudge']
        scorejudge=request.form['scorejudge']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE sports_event SET linejudge=%s,scorejudge=%s WHERE type=%s",(linejudge,scorejudge,type))
        mysql.connection.commit()
        flash('event created successfully')
        return render_template("sportsdayevent.html")
    
@app.route('/viewspregstud')
def viewspregstud():
     if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM sports_reg")
        data = cur.fetchall()
        return render_template("viewsportsstud.html",data=data)
    


#staff
@app.route('/viewsplevent/<staffid>/', methods=["POST", "GET"])
def viewsplevent(staffid):
      if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM special_event where staffid=%s", (staffid,))
        data = cur.fetchall()
        if data:
            return render_template("viewsplevent.html",data=data)      
        else:
             flash('NO RECORDS')
             return render_template("viewsplevent.html")
            

@app.route('/viewspecialregstud/<staffid>/', methods=['GET', 'POST'])
def viewspecialregstud(staffid):
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT *  FROM special_reg WHERE staff=%s", (staffid,))
        mysql.connection.commit()
        data = cur.fetchall()
        print(data)
        if data:
            return render_template("viewsplregstud.html", data=data)
        else:
             flash('NO RECORDS')
             return render_template("viewsplregstud.html")

@app.route('/viewsportsdayevent/<staffid>/')
def viewsportsdayevent(staffid):
      if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM sports_event where linejudge=%s OR scorejudge=%s", (staffid,staffid))
        data = cur.fetchall()
        if data:
            return render_template("viewsportsdayevent.html",data=data)
        else:
            flash('NO RECORDS')
            return render_template("viewsportsdayevent.html")

@app.route('/viewsportsregstud/<staffid>/', methods=['GET', 'POST'])
def viewsportsregstud(staffid):
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT *  FROM sports_reg WHERE linejudge=%s OR scorejudge=%s", (staffid,staffid))
        mysql.connection.commit()
        data = cur.fetchall()
        print(data)
        if data:
            return render_template("viewspregstud.html", data=data)
        else:
            flash('NO RECORDS')
            return render_template("viewspregstud.html")

#student
@app.route('/viewregular/<rollno>/', methods=["GET", "POST"])
def viewregular(rollno):
    rollno = int(session['rollno'])
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM regulardb")
        data = cur.fetchall()
        if data:
            return render_template("vregulargames.html", value=data,rollno=rollno)   
   

@app.route('/gregister/<rollno>/<gameid>/', methods=["POST", "GET"])
def gregister(rollno,gameid):

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM regulardb WHERE gameid=%s", (gameid,))
    data = cur.fetchone()
    
    print(data['doubles'])
    print(data['singles'])
    mcur=mysql.connection.cursor()
    mcur.execute("SELECT rollno FROM student WHERE rollno=%s", (rollno,))
    mdata=mcur.fetchone()
    

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student")
    stud = cur.fetchall()
    print(stud)
    

        # print(mdata)

    if data['singles']=="yes":
        return render_template("slotbook1.html", value=data,mvalue=mdata,students=stud)
    else:
        return render_template("slotbook.html", value=data,mvalue=mdata,students=stud)
      

    # if request.method == 'GET':
    #     cur = mysql.connection.cursor()
    #     cur.execute("SELECT * FROM regulardb WHERE gameid=%s", (gameid,))
    #     data = cur.fetchone()

    #     print(data['doubles'])
    #     print(data['singles'])
    #     mcur=mysql.connection.cursor()
    #     mcur.execute("SELECT rollno FROM student WHERE email=%s", (studmail,))
    #     mdata=mcur.fetchone()
    #     # print(mdata)

    #     if data['singles']=="yes":
    #         return 'Singles Form'
    #     else:
    #         return 'Doublesa Form'
    # return render_template("slotbook.html", value=data,mvalue=mdata)

@app.route('/sgregister/', methods=["POST"])
def sgregister():
    gameid=request.form['gameid']
    rollno=request.form['rollno']
    teammember1=request.form['r1']
    teammember2=request.form['r2']
    teammember3=request.form['r3']
    
    if (rollno!=teammember1 and rollno!=teammember2 and rollno!= teammember3):
        if(teammember1!=teammember2 and teammember1!=teammember3):
            if(teammember2!=teammember3):
                srcur=mysql.connection.cursor()
                qry = f"INSERT INTO `regulargamebooking` (`gameid`, `rollno`, `teammember1`, `teammember2`, `teammember3`) VALUES ('{gameid}', '{rollno}', '{teammember1}', '{teammember2}', '{teammember3}')"
                # "INSERT INTO regulargamebooking (gameid,rollno,teammember1,teammember2,teammember3) VAlUES(%s,%s,%s,%s,%s) ", (gameid,rollno,teammember1,teammember2,teammember3)
                res = srcur.execute(qry)  
                mysql.connection.commit()
                if res:
                    return render_template('success.html', msg="Booking Done")
                else:
                    return render_template('failure.html', msg="Booking failed")
            else:
                return render_template('failure.html', msg="Roll no sho")
        else:
            return render_template('failure.html', msg="Roll no should be different")
    else:
         return render_template('failure.html', msg="Roll no should be different")
    # if request.method == 'POST':
    #     gameid=request.form['gameid']
    #     rollno=request.form['rollno']
    #     teammember1=request.form['r1']
    #     teammember2=request.form['r2']
    #     teammember3=request.form['r3']


    #     srcur=mysql.connection.cursor()
    #     qry = f"INSERT INTO `regulargamebooking` (`gameid`, `rollno`, `teammember1`, `teammember2`, `teammember3`) VALUES ('{gameid}', '{rollno}', '{teammember1}', '{teammember2}', '{teammember3}')"
    #     # "INSERT INTO regulargamebooking (gameid,rollno,teammember1,teammember2,teammember3) VAlUES(%s,%s,%s,%s,%s) ", (gameid,rollno,teammember1,teammember2,teammember3)
    #     srcur.execute(qry)          
    #     mysql.connection.commit()

    #     return render_template("studpanel.html")
    #     # indata = [teammember1,teammember2,teammember3]
    #     # rcur=mysql.connection.cursor()
    #     # rcur.execute("SELECT rollno FROM student")
    #     # rdata = rcur.fetchall()

    #     # print(rdata)
    #     # print(list(rdata))
    #     # if(len(rdata)>0):
    #     #     for x in indata:
    #     #         for y in rdata:
    #     #             print(x,y) 
    #     #             if(x==y):
    #     #                 srcur=mysql.connection.cursor()
    #     #                 srcur.execute("INSERT INTO regulargamebooking (games,rollno,teammember1,teammember2,teammember3) VAlUES(%s,%s,%s,%s,%s) ", (games,rollno,teammember1,teammember2,teammember3,))          
                       
    # return render_template("studpanel.html")


@app.route('/sgregisterr/', methods=["POST"])
def sgregisterr():
    
    gameid=request.form['gameid']
    rollno=request.form['rollno']
    teammember1=request.form['r1']

    if rollno != teammember1:
        rcur=mysql.connection.cursor()
        qry = f"INSERT INTO `regulargamebooking` (`gameid`, `rollno`, `teammember1`) VALUES ('{gameid}', '{rollno}', '{teammember1}')"
        res = rcur.execute(qry)  
        mysql.connection.commit()
        if res:
            return render_template('success.html', msg="Booking Done")
        else:
            return render_template('failure.html', msg="Booking Failed")
    else:
        return render_template('failure.html', msg="Booking Failed ")


@app.route('/viewspecial/<rollno>/', methods=["GET", "POST"])
def viewspecial(rollno):
    rollno = int(session['rollno'])
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM special_event")
        data = cur.fetchall()
        if data:
            return render_template("vspecial.html", value=data, rollno=rollno)

@app.route('/splregister/<rollno>/<eventid>/', methods=["POST", "GET"])
def splregister(rollno,eventid):

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM special_event WHERE eventid=%s", (eventid,))
    data = cur.fetchone()
    
    # print(data['doubles'])
    # print(data['singles'])
    mcur=mysql.connection.cursor()
    mcur.execute("SELECT rollno FROM student WHERE rollno=%s", (rollno,))
    mdata=mcur.fetchone()
    

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student")
    stud = cur.fetchall()
    print(stud)

        # print(mdata)

    if data['type']=="singles":
        return render_template("specialreg1.html", value=data,mvalue=mdata,students=stud)
    else:
        return render_template("specialreg.html", value=data,mvalue=mdata,students=stud)
      

# @app.route('/splregister/<rollno>/<eventid>/', methods=["POST", "GET"])
# def splregister(rollno,eventid):
#     if request.method == 'GET':
#         cur = mysql.connection.cursor()
#         cur.execute("SELECT * FROM special_event WHERE eventid=%s", (eventid,))
#         data = cur.fetchall()
#         mcur=mysql.connection.cursor()
#         mcur.execute("SELECT rollno FROM student WHERE rollno=%s", (rollno,))
#         mdata=mcur.fetchone()
#     return render_template("specialreg.html", value=data,mvalue=mdata)

@app.route('/specialregister/', methods=["POST"])
def specialregister():
    eventid=request.form['eventid']
    rollno=request.form['rollno']
    teammember1=request.form['r1']
    teammember2=request.form['r2']
    teammember3=request.form['r3']
    if (rollno!=teammember1 and rollno!=teammember2 and rollno!= teammember3):
        if(teammember1!=teammember2 and teammember1!=teammember3):
            if(teammember2!=teammember3):
                srcur=mysql.connection.cursor()
                qry = f"INSERT INTO `special_reg` (`eventid`, `rollno`, `teammember1`, `teammember2`, `teammember3`) VALUES ('{eventid}', '{rollno}', '{teammember1}', '{teammember2}', '{teammember3}')"
                # "INSERT INTO regulargamebooking (gameid,rollno,teammember1,teammember2,teammember3) VAlUES(%s,%s,%s,%s,%s) ", (gameid,rollno,teammember1,teammember2,teammember3)
                res = srcur.execute(qry)  
                mysql.connection.commit()
                if res:
                    return render_template('success.html', msg="Booking Done")
                else:
                    return render_template('failure.html', msg="Booking failed")
            else:
                return render_template('failure.html', msg="Roll no sho")
        else:
            return render_template('failure.html', msg="Roll no should be different")
    else:
         return render_template('failure.html', msg="Roll no should be different")


@app.route('/specialregister1/', methods=["POST"])
def specialregister1():
    
    gameid=request.form['eventid']
    rollno=request.form['rollno']
    teammember1=request.form['r1']

    if rollno != teammember1:
        rcur=mysql.connection.cursor()
        qry = f"INSERT INTO `special_reg` (`gameid`, `rollno`, `teammember1`) VALUES ('{gameid}', '{rollno}', '{teammember1}')"
        res = rcur.execute(qry)  
        mysql.connection.commit()
        if res:
            return render_template('success.html', msg="Booking Done")
        else:
            return render_template('failure.html', msg="Booking Failed")
    else:
        return render_template('failure.html', msg="Booking Failed ")


# @app.route('/specialregister/<eventid>/<rollno>/<staffid>/', methods=["GET", "POST"])
# def specialregister(eventid,rollno,staffid):
#     if request.method == 'POST':
#         eventid=request.form['eventid']
#         rollno=request.form['rollno']
#         teammember1=request.form['r1']
#         teammember2=request.form['r2']
#         teammember3=request.form['r3']
#         staffid=request.form['staffid']
#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO special_reg (eventid,rollno,teammember1,teammember2,teammember3,staff) VAlUES(%s,%s,%s,%s,%s,%s) ", (eventid,rollno,teammember1,teammember2,teammember3,staffid,))
#         mysql.connection.commit()
#     return "successfully registered"

@app.route('/viewsports/<rollno>/', methods=["GET", "POST"])
def viewsports(rollno):
    rollno = int(session['rollno'])
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM sports_event")
        data = cur.fetchall()
        if data:
            return render_template("vsports.html", value=data, rollno=rollno)


@app.route('/spregister/<rollno>/<sports_eventid>/', methods=["POST", "GET"])
def spregister(rollno,sports_eventid):
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM sports_event WHERE sports_eventid=%s", (sports_eventid,))
        data = cur.fetchone()
        mcur=mysql.connection.cursor()
        mcur.execute("SELECT rollno FROM student WHERE rollno=%s", (rollno,))
        mdata=mcur.fetchone()
        return render_template("sportsreg.html", value=data,mvalue=mdata)

@app.route('/sportsregister/<sports_eventid>/<rollno>/', methods=["GET", "POST"])
def sportsregister(sports_eventid,rollno):
    if request.method == 'POST':
        sports_eventid=request.form['sports_eventid']
        rollno=request.form['rollno']
        teammember1=request.form['r1']
        teammember2=request.form['r2']
        teammember3=request.form['r3']
        lstaff=request.form['linejudge']
        sstaff=request.form['scorejudge']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO sports_reg (sports_eventid,rollno,teammember1,teammember2,teammember3,linejudge,scorejudge) VAlUES(%s,%s,%s,%s,%s,%s,%s) ", (sports_eventid,rollno,teammember1,teammember2,teammember3,lstaff,sstaff,))
        mysql.connection.commit()
    return "successfully registered"

#sportsdayresult
@app.route('/addsresult')
def addsresult():
    return render_template("addsresult.html")

@app.route('/sportsresult')
def sportsresult():
    return render_template("sportsresult.html")

#specialresult
@app.route('/addresult')
def addresult():
    return render_template("addsplresult.html")

@app.route('/specialresult')
def specialresult():
    return render_template("result.html")

@app.route('/back')
def back():
    return render_template("adminpanel.html")



@app.route('/logout')
def logout():
    session.clear()
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
