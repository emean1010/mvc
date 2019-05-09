import os.path
from functools import wraps

from flask import (
    request,
    redirect,
    jsonify,
)
from jinja2 import (
    Environment,
    FileSystemLoader,
)

from models.session import Session
from models.user import User
from utils import log

import random
import json
from models.weibo import Weibo
from models.comment import Comment


def random_string():
    """
    生成一个随机的字符串
    """
    seed = 'bdjsdlkgjsklgelgjelgjsegker234252542342525g'
    s = ''
    for i in range(16):
        # 这里 len(seed) - 2 是因为我懒得去翻文档来确定边界了
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def initialized_environment():
    parent = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(parent, 'templates')
    # 创建一个加载器, jinja2 会从这个目录中加载模板
    loader = FileSystemLoader(path)
    # 用加载器创建一个环境, 有了它才能读取模板文件
    e = Environment(loader=loader)
    return e


class MvcTemplate:
    e = initialized_environment()

    @classmethod
    def render(cls, filename, *args, **kwargs):
        # 调用 get_template() 方法加载模板并返回
        template = cls.e.get_template(filename)
        # 用 render() 方法渲染模板
        # 可以传递参数
        return template.render(*args, **kwargs)


def current_user():
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        s = Session.find_by(session_id=session_id)
        if s is None or s.expired():
            return User.guest()
        else:
            user_id = s.user_id
            u = User.find_by(id=user_id)
            return u
    else:
        return User.guest()


def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    # 之前上课我说过不要用数字来作为字典的 key
    # 但是在 HTTP 协议中 code 都是数字似乎更方便所以打破了这个原则
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def formatted_header(headers, code=200):
    """
    Content-Type: text/html
    Set-Cookie: user=mvc
    """
    header = 'HTTP/1.1 {} OK Hello\r\n'.format(code)
    header += ''.join([
        '{}: {}\r\n'.format(k, v) for k, v in headers.items()
    ])
    return header


def login_required(route_function):
    """
    这个函数看起来非常绕，所以你不懂也没关系
    就直接拿来复制粘贴就好了
    """

    @wraps(route_function)
    def f():
        log('login_required')
        u = current_user()
        if u.is_guest():
            log('游客用户')
            return redirect('/user/login/view')
        else:
            log('登录用户', route_function)
            return route_function()

    return f


def same_user_required(route_function):
    """
    这个函数看起来非常绕，所以你不懂也没关系
    就直接拿来复制粘贴就好了
    """

    @wraps(route_function)
    def f():
        log('same_user_required')
        u = current_user()
        if 'id' in request.args:
            weibo_id = request.args['id']
        else:
            weibo_id = request.form['id']
        w = Weibo.find_by(id=int(weibo_id))

        if w.user_id == u.id:
            return route_function()
        else:
            return redirect('/weibo/index')

    return f


# 微博的删改请求带有微博的id，验证这个id
def weibo_owner_required(route_function):

    @wraps(route_function)
    def f():
        log('weibo_owner_required')
        u = current_user()
        data = []
        if request.method == 'GET':
            data = request.args
        else:
            data: dict = request.json
        log('要验证的请求', data)
        weibo_id = int(data['id'])
        w = Weibo.find_by(id=weibo_id)
        if u.id == w.user_id:
            log('这是微博作者')
            return route_function()
        else:
            log('不是微博作者')
            d = dict(
                message="不是微博作者没有权限"
            )
            return jsonify(d)

    return f


# 评论的删改请求带有评论内容和微博id，分别验证微博用户id和评论用户id
def comment_owner_required(route_function):

    @wraps(route_function)
    def f():
        log('comment_owner_required')
        u = current_user()
        data = []
        if request.method == 'GET':
            data = request.args
        else:
            data: dict = request.json
        log('要验证的请求', data)
        comment_id = int(data['id'])
        c = Comment.find_by(id=comment_id)
        log('验证comment内容', c)
        weibo_id = c.weibo_id
        w = Weibo.find_by(id=weibo_id)
        if u.id == c.user_id or u.id == w.user_id:
            log('这是评论或者微博作者', u.id, c.user_id, w.user_id)
            return route_function()
        else:
            log('不是评论或者微博作者', u.id, c.user_id, w.user_id)
            d = dict(
                message="不是评论或者微博作者没有权限"
            )
            return jsonify(d)

    return f