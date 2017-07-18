from flask import Flask, request, render_template, redirect, url_for, session, g, abort, flash, make_response, jsonify, Response
from datetime import timedelta, datetime
from models import IDC, Asset, User, app_host, application, App_product, db
from common.utility import  auth_login_required, hashpass, login_required
from common.util import dbdel, abort_if_id_doesnt_exist
from common.restful import  Serialization
from common.token_manage import Token_Manager
from app import app
from config import cross_origin


task = Serialization()
tokenauth = Token_Manager()


@app.route('/api/v1/product',methods=['GET'])
@cross_origin()
@auth_login_required
def product():
    if request.method == 'GET':
        '''
           查询产品线信息
           {  "info": "product 1 add success!",   "message": "OK",   "result": {    "product_name": "jltest",     "product_note": "note",     "product_user": "zhxiaohe"  },   "status": "200"}
        '''
        data =[ {'product_id':pduct.product_id,'product_name': pduct.product_name,'product_user':pduct.product_user,'product_note':pduct.product_note} for pduct in App_product.query.all() ]
        return task.json_message_200(data), 200


@app.route('/api/v1/product',methods=['POST'])
@cross_origin()
@auth_login_required
def product_add():
    if request.method == 'POST':
        '''
           新增产品线
        '''
        args = request.json
        data = App_product(**args)
        db.session.add(data)
        db.session.commit()
        mes = {'product_name':data.product_name,'product_note':data.product_note,'product_user':data.product_user}
        info = 'product %s add success!' % data.product_name
        return task.json_message_200(data=mes,info=info), 200



@app.route('/api/v1/product/<int:id>',methods=['GET'])
@cross_origin()
@auth_login_required
def product_app(id):
    '''
        查询产品线下的应用
       { "info": "", "message": "OK", "result": [ { "appname": "JGdepository", "appnote": "backend", "asset": [ "172.16.1.5", "172.16.1.6", "172.16.1.5" ] }
    '''
    if request.method == 'GET':
        appli = App_product.query.filter_by(product_id=id).first()
        data = [ {'app_id':i.app_id,'appname':i.app_name,'appnote':i.app_note,'asset':[ ass.system_ip for ass in i.app_asset]} for i in appli.app_product ]
        return task.json_message_200(data), 200


@app.route('/api/v1/product/<all>',methods=['GET'])
@cross_origin()
@auth_login_required
def product_all(all):
    '''
        all==all：
            查询所有产品线下的应用及IP信息
            { "info": "", "message": "OK", "result": [ { "appname": "JGdepository", "appnote": "backend", "asset": [ "172.16.1.5", "172.16.1.6", "172.16.1.5" ] }
        all=charts:
            highcharts 出图
    '''
    if request.method == 'GET':
        if all == 'all':

            #data = [ {'app_id':i.app_id,'appname':i.app_name,'appnote':i.app_note,'asset':[ ass.system_ip for ass in i.app_asset]} for i in appli.app_product ]
            data = [ {'name':pduct.product_name,'children':[ {'name':appli.app_name, 'children':[{'name':ass.system_ip} for ass in appli.app_asset ] }  for appli in pduct.app_product]} for pduct in App_product.query.all()]
            return task.json_message_200(data), 200
        if all == 'charts':
            data = []
            subdata = []
            for i in App_product.query.all():
                d = {'name': i.product_name, 'id': i.product_name}
                d['data'] = []
                p_asset = 0
                for app in i.app_product:
                    c = 0
                    for ass in app.app_asset:
                        c += 1
                        p_asset += 1
                    d['data'].append([app.app_name, c])
                subdata.append(d)
                data.append({'name': i.product_name, 'y': p_asset, 'drilldown': i.product_name})


            #return task.json_message_200({'productdata':data,'drilldown':subdata}), 200
            return task.json_message_200({'productdata':data,'drilldown':subdata}), 200
        else:
            return task.json_message_404(), 404



@app.route('/api/v1/apps/',methods=['GET'])
@cross_origin()
@auth_login_required
def apps_listall():
    '''
       查询所有应用信息

    '''
    if request.method == 'GET':
        data = [ {'app_id':i.app_id,'appname':i.app_name,'appnote':i.app_note,'asset':[ass.system_ip for ass in i.app_asset]} for i in application.query.all() ]
        return task.json_message_200(data), 200


@app.route('/api/v1/apps/<int:id>',methods=['GET'])
@cross_origin()
@auth_login_required
def apps_list(id):
    '''
       查询某个应用信息
       {"info": "", "message": "OK", "result": {"appname": "test", "appnote": "test", "app_product": "", "asset": {"10.88.20.3": 20}}, "status": "200"}
    '''
    if request.method == 'GET':
        i = application.query.filter_by(app_id=id).first()
        #product =  {i.app_product.product_name:i.app_product.product_id}
        if i.appproduct:
            product = {i.appproduct.product_name:i.app_product}
        else:
            product = ""

        data = {'app_id':i.app_id,'app_name':i.app_name,'app_note':i.app_note,'app_product':product,'asset':{ass.system_ip:ass.host_id for ass in i.app_asset}}
        return task.json_message_200(data), 200


@app.route('/api/v1/apps/<int:id>',methods=['PUT'])
@cross_origin()
@auth_login_required
def apps_update(id):
    '''
       更新某个应用信息
       {"info": "", "message": "OK", "result": {"appname": "test", "appnote": "test", "app_product": "", "asset": []}, "status": "200"}
    '''
    if request.method == 'PUT':
        args = request.json
        appli = application.query.filter_by(app_id=id).first()

        appli.app_name=args['app_name']
        appli.app_note=args['app_note']
        appli.app_user=args['app_user']

        assetid = args['app_asset']
        appproduct = args['app_product']
        if appli.appproduct:
            oldproduct = appli.app_product
        else:
            oldproduct = ""

        if appproduct:
            if not oldproduct == int(appproduct):
                pduct = App_product.query.get(int(appproduct))
                appli.appproduct=pduct
                pductname = appli.app_product
            else:
                pductname = oldproduct
        else:
            pductname = oldproduct

        oldasset = [ass.host_id for ass in appli.app_asset]
        oldassetid_poor = set(oldasset) - set(assetid)
        if oldassetid_poor:
            for poor in oldassetid_poor:
                host = Asset.query.get(int(poor))
                host.application_status = 'free'
                appli.app_asset.remove(host)
        assetid_poor = set(assetid) - set(oldasset)
        if assetid_poor:
            for Assetid in assetid_poor:
                host = Asset.query.get(int(Assetid))
                host.application_status = 'use'
                appli.app_asset.append(host)

        db.session.add(appli)
        db.session.commit()
        data = {'app_id':appli.app_id,'app_name':appli.app_name,'app_note':appli.app_note,'app_product':pductname,'asset':[ ass.system_ip for ass in appli.app_asset]}
        return task.json_message_200(data=data,info='success!'), 200\


@app.route('/api/v1/apps/<int:id>',methods=['DELETE'])
@cross_origin()
@auth_login_required
def apps_del(id):
    '''
       del某个应用信息，取消与asset的多对多
    '''
    if request.method == 'DELETE':
        appli = application.query.filter_by(app_id=id).first()


        oldasset = [ass.host_id for ass in appli.app_asset]
        if oldasset:
            for poor in oldasset:
                host = Asset.query.get(int(poor))
                host.application_status = 'free'
                appli.app_asset.remove(host)

        db.session.delete(appli)
        db.session.commit()
        return task.json_message_200(data='remove success!',info='remove success!'), 200


@app.route('/api/v1/apps/',methods=['POST'])
@cross_origin()
@auth_login_required
def apps():
    '''
       新增应用并且绑定产品线
       {"app_name":"JGfinance","app_note":"JGfinance","app_product":1}  #productid为产品线主键
        or新增应用并且绑定产品线并且绑定服务器
       {'app_product': '1', 'app_user': 'CFCA', 'app_note': '%E7%94%B5%E5%AD%90%E7%AD%BE%E7%AB%A0', 'app_name': 'CFCA', 'app_asset': ['3', '4']}
    '''
    if request.method == 'POST':
        args = request.json
        pid=args['app_product']
        del args['app_product']

        #try:
        if  args['app_asset']:
            assetid = args['app_asset']
            del args['app_asset']
            if pid:
                appli = App_product.query.get(int(pid))
                data = application(**args, appproduct=appli)
            else:
                data = application(**args)
            for Assetid in assetid:
                host = Asset.query.get(int(Assetid))
                host.application_status = 'use'
                data.app_asset.append(host)
            db.session.add(data)
            db.session.commit()
            info = 'application %s add success' % data.app_name
            mes = {'appname': data.app_name, 'appnote': data.app_note, 'asset': [ass.system_ip for ass in data.app_asset]}
            return task.json_message_200(data=mes,info=info), 200
        #except:
        #   appli = App_product.query.get(pid)
        #    data = application(**args,appproduct=appli)
        #    db.session.add(data)
        #   db.session.commit()
        #    return task.json_message_200(args), 200



@app.route('/api/v1/apps_host/',methods=['POST'])
@cross_origin()
@auth_login_required
def apps_host():
    '''
       应用绑定asset
       {"app_id":1,"host_id":[1,2,3]}
    '''
    if request.method == 'POST':
        args = request.json
        a=application.query.get(args['app_id'])
        #print(host.host_id)
        if a:
            for hostid in args['host_id']:
                a.app_asset.append(Asset.query.get(hostid))
            db.session.add(a)
            db.session.commit()
            return task.json_message_200(args), 200
        else:
            return task.json_message_404(mes=args['app_id']), 404



@app.route('/api/v1/apps_host/<int:id>',methods=['GET'])
@cross_origin()
@auth_login_required
def appget_host(id):
    '''
    通过app查询主机
    '''
    if request.method == 'GET':
        apps = application.query.get(id)
        ip = [ i.system_ip for i in apps.app_asset]
        data = {'apps':apps.app_name,'ip':ip}
        return task.json_message_200(data),200


@app.route('/api/v1/product_host/',methods=['GET'])
@cross_origin()
@auth_login_required
def product_host():
    '''
    新增app时需要查询可用主机和产品线
    { "info": "", "message": "OK", "result": { "ip": { "10.88.19.2": 5, "172.16.1.6": 4 }, "product": { "\u91d1\u8c37\u4e13\u4eab": 2, "\u91d1\u8c37\u8d22\u884c": 1 } }, "status": "200" }
    '''
    if request.method == 'GET':
        pd = {}
        ip = {}
        for pduct in App_product.query.all():
            pd[pduct.product_name]= pduct.product_id
        for asset in Asset.query.filter_by(models='app',application_status='free'):
            ip[asset.system_ip]=asset.host_id
        data = {'product':pd,'ip':ip}
        return task.json_message_200(data),200
