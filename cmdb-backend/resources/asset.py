from flask import Flask, request, render_template, redirect, url_for, session, g, abort, flash, make_response, jsonify, Response
from datetime import timedelta, datetime
from models   import IDC, Asset,Asset_offline , User, db
from common.utility import  auth_login_required, hashpass, login_required
from common.util import dbdel, abort_if_id_doesnt_exist
from common.restful import  Serialization
from common.token_manage import Token_Manager
from app import app
from config import cross_origin


task = Serialization()
tokenauth = Token_Manager()

@app.route('/api/v1/asset',methods=['GET'])
@cross_origin()
@auth_login_required
def assetall():
    if request.method == 'GET':
        '''
           查询所有服务器信息
        '''
        #data = [{'idc':'天地祥云','address':'北京某地','manager':'Mr 张','contacts':'1234567'},{'idc':'济南某机房','address':'济南某地','manager':'Mr 张','contacts':'1234567'}]
        #data = [ {'System_Ip':'172.16.1.2','System_Hostname':'jira','idc':'QCLOUD','Device_type':'VM'},{'System_Ip':'172.16.1.3','System_Hostname':'wiki','idc':'QCLOUD','Device_type':'VM'},{'System_Ip':'172.16.1.4','System_Hostname':'sso','idc':'QCLOUD','Device_type':'VM'} ]
        data =[ {'host_id':asset.host_id,'system_ip':asset.system_ip,'system_hostname':asset.system_hostname,'idc':asset.idc_id,'device_type':asset.device_type} for asset in Asset.query.all() ]
        return task.json_message_200(data), 200


@app.route('/api/v1/assetphy',methods=['GET'])
@cross_origin()
@auth_login_required
def assetphy():
    if request.method == 'GET':
        '''
           查询所有物理服务器信息
        '''
        #data = [ {'System_Ip':'172.16.1.2','System_Hostname':'jira','idc':'QCLOUD','Device_type':'VM'},{'System_Ip':'172.16.1.3','System_Hostname':'wiki','idc':'QCLOUD','Device_type':'VM'},{'System_Ip':'172.16.1.4','System_Hostname':'sso','idc':'QCLOUD','Device_type':'VM'} ]
        data =[ {'host_id':asset.host_id,'system_ip':asset.system_ip,'system_hostname':asset.system_hostname,'idc':asset.idc_id,'device_type':asset.device_type} for asset in Asset.query.filter_by(device_type='PHY').all() ]
        return task.json_message_200(data), 200


@app.route('/api/v1/assetvm',methods=['GET'])
@cross_origin()
@auth_login_required
def assetvm():
    if request.method == 'GET':
        '''
           查询所有VM服务器信息
        '''
        #data = [ {'System_Ip':'172.16.1.2','System_Hostname':'jira','idc':'QCLOUD','Device_type':'VM'},{'System_Ip':'172.16.1.3','System_Hostname':'wiki','idc':'QCLOUD','Device_type':'VM'},{'System_Ip':'172.16.1.4','System_Hostname':'sso','idc':'QCLOUD','Device_type':'VM'} ]
        data =[ {'host_id':asset.host_id,'system_ip':asset.system_ip,'system_hostname':asset.system_hostname,'idc':asset.idc_id,'device_type':asset.device_type} for asset in Asset.query.filter_by(device_type='VM').all() ]
        return task.json_message_200(data), 200


@app.route('/api/v1/asset/',methods=['POST'])
@cross_origin()
@auth_login_required
def add_asset():
    '''
       新增服务器信息
        { "Device_type": "VM", "System_Hostname": "sso.jinu.tech", "System_Ip": "172.16.1.4", "IDC_Id": "QCLOUD" , "Physical_Memory": "2" }
    '''
    if request.method == 'POST':
        data  = request.json
        #host = Asset.query.filter_by(Host_Id=id).first()
        #data = {'System_Ip': host.System_Ip, 'System_Hostname': host.System_Hostname, 'idc': host.IDC_Id,'Device_type': host.Device_type}
        #data = {'System_Ip': 'host.System_Ip', 'System_Hostname': 'host.System_Hostname', 'idc': 'host.IDC_Id','Device_type': 'host.Device_type'}
        host = Asset(**data)
        db.session.add(host)
        db.session.commit()
        result = {'host_id': host.host_id, 'system_ip': host.system_ip, 'system_hostname': host.system_hostname,'idc': host.idc_id, 'device_type': host.device_type}
        mes = 'HOST add is success , ID is %s .' %  host.host_id
        return task.json_message_200(data=result,info=mes), 200



@app.route('/api/v1/batchasset/',methods=['POST'])
@cross_origin()
@auth_login_required
def batch_asset():
    '''
        批量新增服务器信息
         [
 	     { "device_type": "VM", "system_hostname": "git.jinu.tech", "system_ip": "172.16.1.5", "idc_id": "QCLOUD" , "physical_memory": "2" }
 	      ,
 	     { "device_type": "VM", "system_hostname": "jk.jinu.tech", "system_ip": "172.16.1.6", "idc_id": "QCLOUD" , "physical_memory": "2" }
         ]
    '''
    if request.method == 'POST':
        hostlist  = request.json
        mes = []
        for data in hostlist:
            host = Asset(**data)
            db.session.add(host)
            mes.append({ host.system_ip:host.host_id})
        db.session.commit()
        return task.json_message_200('HOST add is success , ID is %s .' %  mes), 200




@app.route('/api/v1/asset/<int:id>',methods=['GET'])
@cross_origin()
@auth_login_required
def asset(id):
    '''
       查询单台服务器信息
    '''
    if request.method == 'GET':
        asset = Asset.query.filter_by(host_id=id).first()
        #data = {'system_ip': host.system_ip, 'system_hostname': host.system_hostname, 'idc': host.idc_id,'device_type': host.device_type}
        if asset:
            data = {"host_id":asset.host_id,
                 "system_hostname":asset.system_hostname,
                 "system_ip":asset.system_ip,
                 "device_type":asset.device_type,
                 "device_model":asset.device_model,
                 "father_id":asset.father_id,
                 "system_network_card":asset.system_network_card,
                 "system_user":asset.system_user,
                 "system_userpass":asset.system_userpass,
                 "idc_id":asset.idc_id,
                 "system_note":asset.system_note,
                 "system_kernel":asset.system_kernel,
                 "system_version":asset.system_version,
                 "system_mac":asset.system_mac,
                 "physical_memory":asset.physical_memory,
                 "system_swap":asset.system_swap,
                 "memory_slots_number":asset.memory_slots_number,
                 "logical_cpu_cores":asset.logical_cpu_cores,
                 "physical_cpu_cores":asset.physical_cpu_cores,
                 "physical_cpu_model":asset.physical_cpu_model,
                 "hard_disk":asset.hard_disk,
                 "ethernet_interface":asset.ethernet_interface,
                 "device_sn":asset.device_sn,
                 "idrac_ip":asset.idrac_ip,
                 "idrac_user":asset.idrac_user,
                 "idrac_userpass":asset.idrac_userpass,
                 "group_id":asset.group_id,
                 "system_status":asset.system_status,
                 "idc_cabinet":asset.idc_cabinet,
                 "idc_un":asset.idc_un,
                 "models":asset.models,
                 "father_ip":asset.father_ip,
                 "create_time":asset.create_time,
                 "guarantee_date":asset.guarantee_date}

            return task.json_message_200(data), 200
        else:
            return task.json_message_404(), 404

@app.route('/api/v1/asset/<int:id>',methods=['PUT'])
@cross_origin()
@auth_login_required
def up_asset(id):
    '''
       更新单台服务器信息
    '''
    if request.method == 'PUT':
        data = request.json

        #host = Asset.query.filter_by(Host_Id=id).first()
        host = Asset.query.filter_by(host_id=id).update(data)
        db.session.commit()
        return task.json_message_200(data), 200


@app.route('/api/v1/asset/<int:id>',methods=['DELETE'])
@cross_origin()
@auth_login_required
def del_asset(id):
    '''
       删除单台服务器信息,移除至回收表,更改状态,并且停监控
    '''
    if request.method == 'DELETE':
        host = abort_if_id_doesnt_exist(Asset,host_id=id)
        if host:
            #将data新增到回收表中
            data = {'idrac_user': host.idrac_user
                , 'logical_cpu_cores': host.logical_cpu_cores
                , 'idrac_userpass': host.idrac_userpass
                , 'system_version': host.system_version
                , 'idc_un': host.idc_un
                , 'father_ip': host.father_ip
                , 'models': host.models
                , 'system_note': host.system_note
                , 'device_model': host.device_model
                , 'hard_disk': host.hard_disk
                , 'create_time': host.create_time
                , 'father_id': host.father_id
                , 'device_type': host.device_type
                , 'ethernet_interface': host.ethernet_interface
                , 'physical_memory': host.physical_memory
                , 'metadata': host.metadata
                , 'idc_cabinet': host.idc_cabinet
                , 'system_network_card': host.system_network_card
                , 'system_hostname': host.system_hostname
                , 'system_status': host.system_status
                , 'memory_slots_number': host.memory_slots_number
                , 'system_userpass': host.system_userpass
                , 'device_sn': host.device_sn
                , 'physical_cpu_cores': host.physical_cpu_cores
                , 'physical_cpu_model': host.physical_cpu_model
                , 'system_mac': host.system_mac
                , 'system_ip': host.system_ip
                , 'group_id': host.group_id
                , 'system_user': host.system_user
                , 'system_kernel': host.system_kernel
                , 'idrac_ip': host.idrac_ip
                , 'idc_id': host.idc_id
                , 'system_swap': host.system_swap
                , 'guarantee_date': host.guarantee_date
                , 'offline_time': datetime.now()}
            #montior_stop(host.System_Ip)
            dbdel(asset,host_id=id)
            db.session.add(Asset_offline(**data))
            db.session.commit()
            #for i   in dir(host):
            #    data[i] =  i #eval('host.%s' % i)
            #print(data)
            return task.json_message_200('Sucess'), 200
        else:
            return task.json_message_404(),404


@app.route('/api/v1/assetmodels/<models>',methods=['GET'])
@cross_origin()
@auth_login_required
def get_assetmodels(models):
    '''
       根据类型获取服务器信息
       {'host_id': host.host_id, 'system_ip': host.system_ip, 'system_hostname': host.system_hostname,'idc': host.idc_id, 'device_type': host.device_type}
    '''
    if request.method == 'GET':
        if models=='father':
            data = [{'host_id': host.host_id, 'system_ip': host.system_ip, 'system_hostname': host.system_hostname,
                     'idc': host.idc_id, 'device_type': host.device_type} for host in
                    Asset.query.filter_by(models=models,device_type='PHY').all()]
            return task.json_message_200(data), 200
        if models=='app':
            data = [{'host_id': host.host_id, 'system_ip': host.system_ip, 'system_hostname': host.system_hostname,
                     'idc': host.idc_id, 'device_type': host.device_type} for host in
                    Asset.query.filter_by(models=models).all()]
            return task.json_message_200(data), 200
        else:
            return task.json_message_404(),404
