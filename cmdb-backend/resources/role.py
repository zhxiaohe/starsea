from flask import Flask, request, render_template, redirect, url_for, session, g, abort, flash, make_response, jsonify, Response
from datetime import timedelta
from models   import db
from common.utility import  auth_login_required, hashpass, login_required
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
             }
        ]}

        return task.json_message_200(data), 200
