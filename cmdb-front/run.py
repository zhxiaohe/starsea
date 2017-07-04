from flask import Flask,jsonify,render_template,request

app = Flask(__name__)

class aa(object):
    def js(self,data='hellow'):
        return data

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        a=request.headers.get('Authorization')
        print(request.form)
        print(request.json)
        return jsonify({'status':'200'})
    return render_template('index.html')


@app.route('/idc',methods=['GET','POST'])
def idc():
    return render_template('idc.html')

@app.route('/physic')
def physic():
    return render_template('physic.html')

@app.route('/asset')
def asset():
    return render_template('asset.html')

@app.route('/recycle')
def recycle():
    return render_template('recycle.html')

@app.route('/ws')
def ws():
    return render_template('websocket.html')

@app.route('/socketio')
def socketio():
    return render_template('socketio.html')

@app.route('/wstor')
def wstor():
    return render_template('wstor.html')

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/app')
def appli():
    return render_template('appli.html')

if __name__ == '__main__':
    app.run()
