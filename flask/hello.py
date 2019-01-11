
from flask import Flask, render_template
# from flask import redirect
from flask import abort
from flask_script import Manager


app = Flask(__name__)
manager = Manager(app)


@app.route('/')
def index():
    # return '<h1>Hello World!</h1>'
    # return redirect('http://www.baidu.com')
    return render_template('index.html', content="大家好呀", title="这是我的测试")


@app.route('/user/<name>')
def user(name):
    if not name:
        abort(404)
    return '<h1>Hello, %s!</h1>' % name


if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()
