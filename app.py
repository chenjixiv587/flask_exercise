from flask import Flask
from markupsafe import escape  # 为了返回安全
from flask import url_for  # 自动生成路径

app = Flask(__name__)


@app.route('/')
def hello():
    return "hello world"


@app.route('/user/<name>')
def user_page(name):
    return f"<h1>hello {escape(name)}</h1>"


@app.route('/test')
def test_url_for():
    print(url_for("hello"))
    print(url_for("user_page", name="chen"))
    print(url_for("user_page", name="wei"))
    print(url_for('test_url_for'))
    # /test?num=1  下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test_url_for', num=1))
    return "test page"
