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


SECRET_KEY = '\xa8H\xe4;R@pi:Mo\x92\xe4M\xa7*E\x80\n\x8d\xfav3\xd8'

RedisHost='127.0.0.1'
RedisPost='6000'

TIMEOUT = 7200










