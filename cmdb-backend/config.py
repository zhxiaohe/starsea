from app import app
app.debug = True
from flask_cors import CORS,cross_origin
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Mysql Connect Config
MysqlHost = '10.88.20.197'
MysqlUser = 'root'
MysqlPass = '123456'
MysqlDB = 'jingu_v2'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s/%s' % (MysqlUser, MysqlPass, MysqlHost, MysqlDB)


#
SECRET_KEY = '\xa8H\xe4;R@pi:Mo\x92\xe4M\xa7*E\x80\n\x8d\xfav3\xd8'

#redis
RedisHost='127.0.0.1'
RedisPost='6000'

#timeout
TIMEOUT = 7200

#LADP
LDAP_URL = "ldap://10.19.35.24:389"
LDAP_BASE_DN = "OU=www,DC=inx,DC=com"
LDAP_USER = "ops"
LDAP_PASSWD = "qazQAZ2@"











