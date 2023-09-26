import click
from flask import Flask
from markupsafe import escape  # 为了返回安全
from flask import url_for  # 自动生成路径
from flask import render_template
from flask_sqlalchemy import SQLAlchemy  #
import os
import sys
from flask import request
from flask import redirect
from flask import flash


WIN = sys.platform.startswith('win')
if WIN:  # 如果是windows 系统 使用三个斜线
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + \
    os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化之前加载配置
db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app


class User(db.Model):  # 表名 将会是 user (自动生成，小写处理)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


@app.cli.command()  # 注册为命令， 可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop')  # 设置选项
def initdb(drop):
    """Initialize the database"""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("Initialized databases")  # 输出提示信息


@app.cli.command()
def forge():
    """Generate fake data"""
    db.create_all()

    # 全局的两个变量 移动到这个函数内
    # 虚拟数据
    user = "brucechen"
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

    user = User(name=user)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')


@app.context_processor  # 上下文处理器
def inject_user():
    user = User.query.first()
    return dict(user=user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')

        # 验证数据
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input')  # 显示错误提示
            return redirect(url_for('index'))

        # 保存表单到数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created')  # 显示创建成功的提示
        return redirect(url_for('index'))  # 重定向回主页

    movies = Movie.query.all()
    return render_template("index.html", movies=movies)


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


@app.route('/movie/edit/<int:movie_id>', methods=['POST', 'GET'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == "POST":  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash("Item updated")
        return redirect(url_for('index'))  # 重定向到 主页
    return render_template("edit.html", movie=movie)  # 传入被编辑的 电影记录


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()
    flash('Item deleted')
    return redirect(url_for('index'))
