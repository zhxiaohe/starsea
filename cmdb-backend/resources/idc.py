from flask import Flask, request, render_template, redirect, url_for, session, g, abort, flash, make_response, jsonify, Response
from datetime import timedelta
from models   import IDC, User, db
from common.utility import  auth_login_required, hashpass, login_required
from common.restful import  Serialization
from common.token_manage import Token_Manager
from app import app
from config import cross_origin


task = Serialization()
tokenauth = Token_Manager()

@app.route('/api/v1/idc',methods=['GET','POST'])
@cross_origin()
@auth_login_required
def idc():
    '''
       查询所有IDC信息
    '''
    if request.method == 'POST':
        #data = [{'idc':'天地祥云','address':'北京某地','manager':'Mr 张','contacts':'1234567'},{'idc':'济南某机房','address':'济南某地','manager':'Mr 张','contacts':'1234567'}]
        data = [ {'idc': idc.name, 'address': idc.address,'manager': idc.contact,  'contacts':idc.phone}   for idc in IDC.query.all() ]
        return task.json_message_200(data), 200