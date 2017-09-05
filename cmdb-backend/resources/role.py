from flask import Flask, request, render_template, redirect, url_for, session, g, abort, flash, make_response, jsonify, Response
from datetime import timedelta
from models   import  User, Role, Url, db
from common.utility import  auth_login_required, hashpass, login_required
from common.util import abort_if_id_doesnt_exist
from common.restful import  Serialization
from common.token_manage import Token_Manager
from app import app
from config import cross_origin


task = Serialization()
tokenauth = Token_Manager()


@app.route('/api/v1/menu',methods=['GET','POST'])
@cross_origin()
@auth_login_required
def menu():
    if request.method == 'POST':
        t = request.headers.get('Authorization')
        auth = tokenauth.verify_auth_token(t)
        data ={'username': auth['username'],'menu':[
             {'menu':'Dashboard','url':'index','ifsubmenu':'no','id':'index'},
             {'menu':'IDC','url':'idc','ifsubmenu':'no','id':'idc'},
             {'menu':'Asset',
             'url':'',
             'ifsubmenu':'yes',
             'id':'asset',
             'submenu':[
                 {'submenu_name':'physical','submenu_url':'physic','id':'physic'},
             	 {'submenu_name':'vm','submenu_url':'asset','id':'vm'},
                 {'submenu_name':'recycle','submenu_url':'recycle','id':'recycle'},
             	]
             },
             {'menu':'application',
             'url':'',
             'ifsubmenu':'yes',
            'id': 'appli',
             'submenu':[
                 {'submenu_name':'product','submenu_url':'product'},
             	 {'submenu_name':'appcation','submenu_url':'app'},
             	]
             },
            {'menu': 'management',
             'url': '',
             'ifsubmenu': 'yes',
             'id': 'users',
             'submenu': [
                 {'submenu_name': 'user', 'submenu_url': 'user'},
                 {'submenu_name': 'role', 'submenu_url': 'role'},
                 {'submenu_name': 'url', 'submenu_url': 'url'},
             ]
             }
        ]}

        return task.json_message_200(data), 200

@app.route('/api/v1/role',methods=['GET','POST'])
@cross_origin()
#@auth_login_required
def role():
    '''
     {"rolename":"admin"}

    '''
    if request.method == 'POST':
        args = request.json
        if args:
            abort = abort_if_id_doesnt_exist(Role,rolename=args['rolename'])
            if abort:
                data='rolename is exist'
                return task.json_message_401(mes=data),401
            else:
                db.session.add(Role(**args))
                db.session.commit()
                data='ok'
                return task.json_message_200(data=data,info='Role add ok, rolename :%s ' % args )
        else:
            return task.json_message_401(mes='please check '),401

@app.route('/api/v1/role_url',methods=['GET','POST'])
@cross_origin()
#@auth_login_required
def role_url():
    '''
        {'url':urlid,'role':roleid}
        or
        {'url':[urlid,urlid],'role':roleid}

    :return:
    '''
    if request.method == 'POST':
        args = request.json
        urlid = args['urlid']
        roleid = args['roleid']
        role = Role.query.get(int(roleid))
        for i in urlid:
            url = User.query.get(int(i))
            role.role_url=url
        db.session.add(role)
        db.session.commit()
        return task.json_message_200('ok'), 200



@app.route('/api/v1/user',methods=['GET','POST'])
@cross_origin()
#@auth_login_required
def user():
    if request.method == 'POST':
        args = request.json
        email = args['email']
        username = args['username']
        password_hash = hashpass(args['password'])
        user = User.query.filter(User.username == username).first()
        mail = User.query.filter(User.email == email).first()
        if user and mail:
            return task.json_message_401(mes='user or email is exist!'), 401
        else:
            try:
                data = User(email=email, username=username, password_hash=password_hash)
                db.session.add(data)
                db.session.commit()
                return task.json_message_200(data), 200
            except:
                return task.json_message_401(mes='user or email is exist!'), 401

@app.route('/api/v1/user_role',methods=['GET','POST'])
@cross_origin()
#@auth_login_required
def user_role():
    '''
        {'user':userid,'role':roleid}
        {'user':userid,'role':[roleid,roleid]}

    :return:
    '''
    if request.method == 'POST':
        args = request.json
        userid = args['userid']
        roleid = args['role']
        user = User.query.get(int(userid))
        role = Role.query.get(int(roleid))
        role.user_role=user
        db.session.add(role)
        db.session.commit()
        return task.json_message_200('data'), 200



@app.route('/api/v1/url',methods=['GET','POST'])
@cross_origin()
#@auth_login_required
def url():
    """
     #按urltype类型,
         menu  带url的一级菜单
         parentmenu  一级导航菜单,无url
         submenu   子菜单,需要关联一级菜单
         api   api
     #前端菜单
        {"urlname":"IDC","urltype":"menu","urlmenu":"idc","parentmenu":"","method":""}
        {"urlname":"application","urltype":"parentmenu","urlmenu":"","parentmenu":"","method":""}
        {"urlname":"product","urltype":"submenu","urlmenu":"","parentmenu":"application","method":""}

     #后端api
        {"urlname":"get_url","urltype":"api","urlmenu":"/api/v1/url","method":"GET"}

    :return:
    """
    if request.method == 'POST':
        args = request.json
        if ('urlname' and 'urltype' ) in args.keys():
            if args['urltype'] == 'api':
                data=Url(urlname=args['urlname'],urltype=args['urltype'],urlmenu=args['urlmenu'],method=args['method'])
                db.session.add(data)
                db.session.commit()

            elif args['urltype'] == 'menu':
                data =Url(urlname=args['urlname'],urltype=args['urltype'],urlmenu=args['urlmenu'])
                db.session.add(data)
                db.session.commit()

            elif args['urltype'] == 'parentmenu':
                data =Url(urlname=args['urlname'],urltype=args['urltype'])
                db.session.add(data)
                db.session.commit()

            elif args['urltype'] == 'submenu':
                if 'parentmenu' in args.keys():
                    parentmenuid=Url.query.get(int(args['parentmenu']))
                    if parentmenuid:
                        if not parentmenuid.urltype == 'parentmenu':
                            return task.json_message_401(mes='parentmenu not parentmenu'), 401
                    else:
                        return task.json_message_401(mes='parentmenu not found!'), 401
                else:
                    return task.json_message_401(mes='parentmenu not found!'), 401

                data =Url(urlname=args['urlname'],urltype=args['urltype'],urlmenu=args['urlmenu'],parentmenu=parentmenuid.id)
                db.session.add(data)
                db.session.commit()
            else:
                return task.json_message_401(mes='urltype not found!'), 401

        else:
            return task.json_message_401(mes='urlname or urltype not found!'), 401
        return task.json_message_200(data='url add success'), 200
