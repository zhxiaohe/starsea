from flask.ext.sqlalchemy import SQLAlchemy
from app import db
import datetime


app_host = db.Table('cmdb_app_host',
    db.Column('app_id', db.Integer, db.ForeignKey('cmdb_application.app_id')),
    db.Column('host_id', db.Integer, db.ForeignKey('cmdb_asset.host_id'))
)

user_role = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)

role_url = db.Table('role_urls',
    db.Column('url_id', db.Integer, db.ForeignKey('urls.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


class Role(db.Model):
    __tablename__ = 'roles'
    id  = db.Column(db.Integer, primary_key=True)
    rolename  = db.Column(db.String(64))
    #userid  = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_role = db.relationship('User', secondary=user_role, backref=db.backref('roles', lazy='dynamic'))
    role_url = db.relationship('Url', secondary=role_url, backref=db.backref('roles', lazy='dynamic'))


class Url(db.Model):
    __tablename__ = 'urls'
    id  = db.Column(db.Integer, primary_key=True)
    urlname  = db.Column(db.String(64))
    urltype  = db.Column(db.String(64))  #menu  submenu or api
    urlmenu  = db.Column(db.String(256))
    method   = db.Column(db.String(64))
    parentmenu = db.Column(db.Integer)


class IDC(db.Model):
    __tablename__ = 'cmdb_idc'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(50))
    contact = db.Column(db.String(30))
    phone = db.Column(db.String(30))


class Asset(db.Model):
    __tablename__ = 'cmdb_asset'
    host_id = db.Column(db.Integer, primary_key=True)
    system_hostname = db.Column(db.String(50))
    system_ip = db.Column(db.String(256))
    device_type = db.Column(db.String(64))
    device_model = db.Column(db.String(64))
    father_id = db.Column(db.String(64))
    system_network_card = db.Column(db.String(164))
    system_user = db.Column(db.String(256))
    system_userpass = db.Column(db.String(256))
    idc_id = db.Column(db.String(50))
    system_note = db.Column(db.String(256))

    system_kernel = db.Column(db.String(256))
    system_version = db.Column(db.String(256))
    system_mac = db.Column(db.String(256))
    physical_memory = db.Column(db.String(64))
    system_swap = db.Column(db.String(64))
    memory_slots_number = db.Column(db.String(30))
    logical_cpu_cores = db.Column(db.String(64))
    physical_cpu_cores = db.Column(db.String(64))
    physical_cpu_model = db.Column(db.String(64))
    hard_disk = db.Column(db.String(64))
    ethernet_interface = db.Column(db.String(1000))
    device_sn = db.Column(db.String(164))

    idrac_ip = db.Column(db.String(256))
    idrac_user = db.Column(db.String(256))
    idrac_userpass = db.Column(db.String(256))

    group_id = db.Column(db.String(256))
    system_status = db.Column(db.String(64))
    idc_cabinet = db.Column(db.String(64))
    idc_un = db.Column(db.String(64))
    models = db.Column(db.String(64))
    father_ip = db.Column(db.String(64))

    create_time = db.Column(db.DateTime())
    guarantee_date = db.Column(db.String(100))

    application_server = db.Column(db.String(64))
    application_status = db.Column(db.String(64))   #(free use)


class Asset_offline(db.Model):
    __tablename__ = 'cmdb_asset_offline'
    host_id = db.Column(db.Integer, primary_key=True)
    system_hostname = db.Column(db.String(50))
    system_ip = db.Column(db.String(256))
    device_type = db.Column(db.String(64))
    device_model = db.Column(db.String(64))
    father_id = db.Column(db.String(64))
    system_network_card = db.Column(db.String(164))
    system_user = db.Column(db.String(256))
    system_userpass = db.Column(db.String(256))
    idc_id = db.Column(db.String(50))
    system_note = db.Column(db.String(256))

    system_kernel = db.Column(db.String(256))
    system_version = db.Column(db.String(256))
    system_mac = db.Column(db.String(256))
    physical_memory = db.Column(db.String(64))
    system_swap = db.Column(db.String(64))
    memory_slots_number = db.Column(db.String(30))
    logical_cpu_cores = db.Column(db.String(64))
    physical_cpu_cores = db.Column(db.String(64))
    physical_cpu_model = db.Column(db.String(64))
    hard_disk = db.Column(db.String(64))
    ethernet_interface = db.Column(db.String(1000))
    device_sn = db.Column(db.String(164))

    idrac_ip = db.Column(db.String(256))
    idrac_user = db.Column(db.String(256))
    idrac_userpass = db.Column(db.String(256))

    group_id = db.Column(db.String(256))
    system_status = db.Column(db.String(64))
    idc_cabinet = db.Column(db.String(64))
    idc_un = db.Column(db.String(64))
    models = db.Column(db.String(64))
    father_ip = db.Column(db.String(64))

    create_time = db.Column(db.DateTime())
    guarantee_date = db.Column(db.String(100))
    offline_time = db.Column(db.DateTime())
    app_name = db.Column(db.String(64))



class App_product(db.Model):
    __tablename__ = 'cmdb_product'
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(64))
    product_user = db.Column(db.String(64))
    product_note = db.Column(db.String(64))
    app_product = db.relationship('application', backref='appproduct', lazy='dynamic')


class application(db.Model):
    __tablename__ = 'cmdb_application'
    app_id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(64))
    app_note = db.Column(db.String(64))
    app_version = db.Column(db.String(64))
    app_user = db.Column(db.String(64))
    app_product = db.Column(db.Integer, db.ForeignKey('cmdb_product.product_id'))
    app_asset = db.relationship('Asset', secondary=app_host, backref=db.backref('cmdb_application', lazy='dynamic'))




'''
class app_host(db.Model):
    __tablename__ = 'cmdb_app_host'
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.String(64))
    host_id = db.Column(db.String(64))
'''


if __name__ == '__main__':
    def create_all():
        # u = user(email='john@example.com', username='john', password_hash='cat')
        db.create_all()
        # u = Role(id='1',rolename='testxx',userid='1')
        # db.session.add(u)
        # db.session.commit()


    create_all()