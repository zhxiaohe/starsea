# -*- coding: utf-8 -*-
from app import app
from resources.login import *
from resources.idc import *
from resources.role import *
from resources.asset import *
from resources.application import *
#from resources.appgroup import *
app.run(host='0.0.0.0', port=8000,debug='true')