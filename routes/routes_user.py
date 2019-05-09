from urllib.parse import unquote_plus

from werkzeug.datastructures import ImmutableMultiDict

from models.session import Session
from routes import (
    current_user,
    random_string,
)

from utils import log
from models.user import User


# 不要这么 import
# from xx import a, b, c, d, e, f

from flask import (
    request,
    redirect,
    Blueprint,
    render_template,
    current_app)

# endpoint
bp = Blueprint('routes_user', __name__)


@bp.route('/user/login', methods=['POST'])
def login():
    """
    登录页面的路由函数
    """
    form = request.form

    u, result = User.login(form)
    # session 会话
    # token 令牌
    # 设置一个随机字符串来当令牌使用
    session_id = random_string()
    form = dict(
        session_id=session_id,
        user_id=u.id,
    )
    Session.new(form)

    redirect_to_login_view = redirect('/user/login/view?result={}'.format(result))
    response = current_app.make_response(redirect_to_login_view)
    response.set_cookie('session_id', value=session_id)
    response.set_cookie('path', value='/')
    return response


@bp.route('/user/login/view')
def login_view():
    u = current_user()
    result = request.args.get('result', '')
    result = unquote_plus(result)

    return render_template(
        'login.html',
        username=u.username,
        result=result,
    )


@bp.route('/user/register', methods=['POST'])
def register():
    """
    注册页面的路由函数
    """
    form: ImmutableMultiDict = request.form

    u, result = User.register(form.to_dict())
    log('register post', result)

    return redirect('/user/register/view?result={}'.format(result))


@bp.route('/user/register/view')
def register_view():
    result = request.args.get('result', '')
    result = unquote_plus(result)

    return render_template('register.html', result=result)


# RESTFul
# GET /login
# POST /login
# UPDATE /user
# DELETE /user
#
