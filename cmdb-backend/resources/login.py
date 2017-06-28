from flask import Flask, request, render_template, redirect, url_for, session, g, abort, flash,make_response
from datetime import timedelta
#from models   import User, db
from common.utility import hashpass, login_required
from common.restful import  Serialization
from common.token_manage import Token_Manager
from app import app

task = Serialization()

@app.errorhandler(404)
def not_found_error(error):
    return task.json_message_404(), 404

@app.errorhandler(500)
def internal_error(error):
    #db.session.rollback()
    return task.json_message_500(), 500
 

@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def hello():
    if not session.get('logged_in'):
        #abort(401)
        return redirect(url_for('login'))
    return redirect(url_for('idc'))
    #return render_template('index.html')


@app.route('/api/v1/login',methods=['POST'])
def login():
    '''
        通过用户名生成token,返回至前端
    '''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '123456':
            token = Token_Manager()
            tokendata = token.generate_auth_token({'username': username})
            rest_text = task.json_message({'status':'200', 'token':tokendata.decode('utf8'),'timeout':token.timeout})
            rst = make_response(rest_text)
            #rst.set_cookie('name',username)
            rst.headers['Access-Control-Allow-Origin'] = '*'
            return rst,200
        else:
            rest_text =  task.json_message_404()
            rst = make_response(rest_text)
            rst.headers['Access-Control-Allow-Origin'] = '*'
            return rst, 404

'''
@app.route('/user.html', methods=['GET', 'POST'])
def tables():
    if request.method  == 'POST':
        return 'yes'
    else:
        i=User.query.all()   
        x=[ [m.id,m.email,m.username ]  for m in i]
        return render_template('user.html',data=x)




@app.route('/test', methods=['GET', 'POST'])
def te():
    if session.get('logged_in'):
        #return  str(session.get('logged_in'))
        return  session.get('user_id')


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)
    if request.method  == 'POST':
        username = request.form['username']
        password = request.form['password']
        passwoed = hashpass(password)
        user=User.query.filter_by(username=username).first()
        try:
            if username == user.username  and  passwoed == user.password_hash:
                session['logged_in'] = True
                session['user_id'] = user.id
                return redirect(url_for('hello'))
            else:
                flash('username or password  is  error!')
        except AttributeError :
            flash('username or password  is  error!')
    return render_template('login.html')




@app.route('/logout.html', methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', None)
    #flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/reg.html', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['repassword']
        phonemail = request.form['phonemail']
        user=User.query.filter(User.username==username).first()
        mail=User.query.filter(User.email==phonemail).first()
        if password == repassword:
            passwd = hashpass(password)
            if   user  and  mail:
                flash('user or phone/mail is exist')
            else:
                try:
                    u = User(email=phonemail, username=username, password_hash=passwd)
                    db.session.add(u)
                    db.session.commit()
                    return redirect(url_for('login'))

                except:
                    flash('user or phone/mail is exist')
                
        else:
            flash('Passwords don\'t match')
    return render_template('reg.html')


@app.route('/account.html', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        username = request.form['username']
        oldpassword = request.form['oldpassword']
        newpassword = request.form['newpassword']
        repassword = request.form['repassword']
        oldpassword_hash = hashpass(oldpassword)

        user=User.query.filter(User.username==username).first()
        if user.password_hash == oldpassword_hash:

            if newpassword == repassword:
                passwd = hashpass(newpassword)
                try:
                    user.password_hash=passwd
                    db.session.commit()
                    flash('Passwords update ok ,please login! ')
                    return redirect(url_for('login'))

                except Exception :
                    return('error')
                    
            else:
                flash('Passwords don\'t match')
        else:
            flash('old passwords is error!')
    userid = session.get('user_id')
    user = User.query.filter_by(id=userid).first()
    username = user.username
    return render_template('account.html',username = username)

'''







