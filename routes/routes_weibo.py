from models.comment import Comment
from models.weibo import Weibo

from routes import (
    current_user,
    login_required,
    same_user_required,
)
from utils import log

from flask import (
    request,
    redirect,
    Blueprint,
    render_template,
    current_app
)

# endpoint
bp = Blueprint('routes_weibo', __name__)


@bp.route('/weibo/index')
@login_required
def index():
    """
    weibo 首页的路由函数
    """
    u = current_user()
    weibos = Weibo.find_all(user_id=u.id)
    # 替换模板文件中的标记字符串
    return render_template('weibo_index.html', weibos=weibos, user=u)


@bp.route('/weibo/add', methods=['POST'])
@login_required
def add():
    """
    用于增加新 weibo 的路由函数
    """
    u = current_user()
    form = request.form
    Weibo.add(form, u.id)
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/weibo/index')


@bp.route('/weibo/delete')
@login_required
@same_user_required
def delete():
    weibo_id = int(request.args['id'])
    Weibo.delete(weibo_id)
    return redirect('/weibo/index')


@bp.route('/weibo/edit')
@login_required
@same_user_required
def edit():
    weibo_id = int(request.args['id'])
    w = Weibo.find_by(id=weibo_id)
    return render_template('weibo_edit.html', weibo=w)


@bp.route('/weibo/update', methods=['POST'])
@login_required
@same_user_required
def update():
    """
    用于增加新 weibo 的路由函数
    """
    form = request.form
    weibo_id = int(form['id'])
    content = form['content']
    Weibo.update(weibo_id, content=content)
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/weibo/index')