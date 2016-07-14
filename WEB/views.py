#-*- encoding=UTF-8 -*-

from WEB import app,db
from models import Image,User
from flask import render_template,redirect,request,flash,get_flashed_messages
from flask_login import login_user,logout_user,login_required,current_user
import random,hashlib
@app.route('/')
def index():
    image=Image.query.order_by('id desc').limit(10).all()
    return render_template('index.html',images=image)

@app.route('/image/<int:image_id>')
def image(image_id):
    image=Image.query.get(image_id)
    print image
    if image==None:
        return redirect('/')
    return render_template('pageDetail.html',image=image)
@app.route('/profile/<int:profile_id>')
@login_required
def profile(profile_id):
    user=User.query.get(profile_id)
    if image==None:
        return redirect('/')
    return render_template('profile.html',user=user)

@app.route('/reloginpage/')
def reloginpage():
    msg=''
    for m in get_flashed_messages(with_categories=False,category_filter='relogin'):
        msg+=m
    print msg
    return render_template('login.html',msg=msg)

def redirct_with_msg(target,msg,category):
    if msg != None:
        flash(msg,category=category)
    return redirect(target)

@app.route('/reg/', methods={'get','post'})
def reg():
    username=request.values.get('username').strip()
    password=request.values.get('username').strip()
    user=User.query.filter_by(username=username).first()
    if username=='' or password=='':
       return redirct_with_msg('/reloginpage',u'请输入用户名和密码','relogin')
    if user!=None:
        return redirct_with_msg('/reloginpage',u'用户名已存在','relogin')
    salt='.'.join(random.sample('12345678abcdefgABCDEFG',5))
    m=hashlib.md5()
    m.update(password+salt)
    password=m.hexdigest()
    user=User(username,password,salt)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return redirect('/')

@app.route('/login/',methods={'get','post'})
def login():
    username=request.values.get('username').strip()
    password=request.values.get('username').strip()
    print password
    if username=='' or password=='':
        return redirct_with_msg('/reloginpage',u'请输入用户名和密码','relogin')
    user=User.query.filter_by(username=username).first()
    if user == None:
         return redirct_with_msg('/reloginpage',u'用户名不存在','relogin')
    m=hashlib.md5()
    m.update(password+user.salt)
    print user.salt
    print m.hexdigest()
    if(m.hexdigest()!=user.password):
         return redirct_with_msg('/reloginpage',u'密码错误','relogin')
    login_user(user)
    return redirect('/')

@app.route('/loginout/')
def logout():
    logout_user()
    return redirect('/')