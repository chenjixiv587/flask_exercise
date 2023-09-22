from flask import Flask
from markupsafe import escape  # 为了返回安全
from flask import url_for  # 自动生成路径
from flask import render_template


app = Flask(__name__)


# 虚拟数据
username = "brucechen"
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]


@app.route('/')
def index():
    return render_template("index.html", name=username, movies=movies)


@app.route('/user/<name>')
def user_page(name):
    return f"<h1>hello {escape(name)}</h1>"


@app.route('/test')
def test_url_for():
    print(url_for("index"))
    print(url_for("user_page", name="chen"))
    print(url_for("user_page", name="wei"))
    print(url_for('test_url_for'))
    # /test?num=1  下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test_url_for', num=1))
    return "test page"
