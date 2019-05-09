from utils import log
from routes import (
    current_user,
    login_required,
    weibo_owner_required,
    comment_owner_required,
)
from models.weibo import Weibo
from models.comment import Comment

from flask import (
    request,
    redirect,
    jsonify,
    Blueprint,
    current_app
)

# endpoint
bp = Blueprint('api_weibo', __name__)


# 本文件只返回 json 格式的数据
# 而不是 html 格式的数据
# 添加对应的评论内容
@bp.route('/api/weibo/all')
@login_required
def all():
    weibos = Weibo.all()
    for w in weibos:
        comments = w.comments()
        if comments is not None:
            l = []
            for c in comments:
                l.append((c.id, c.content))
            w.comment = dict(l)
    js = [w.json() for w in weibos]
    return jsonify(js)


@bp.route('/api/weibo/add', methods=['POST'])
@login_required
def add():
    # 得到浏览器发送的表单, 浏览器用 ajax 发送 json 格式的数据过来
    # 所以这里我们用新增加的 json 函数来获取格式化后的 json 数据
    form = request.json
    # 创建一个 weibo
    u = current_user()
    w = Weibo.add(form, u.id)
    # 把创建好的 weibo 返回给浏览器
    return jsonify(w.json())


@bp.route('/api/weibo/delete')
@weibo_owner_required
def delete():
    weibo_id = int(request.args['id'])
    Weibo.delete(weibo_id)
    comments = Comment.find_all(weibo_id=weibo_id)
    log('要删除的评论', comments)
    for c in comments:
        Comment.delete(c.id)
    d = dict(
        message="成功删除 weibo"
    )
    return jsonify(d)


@bp.route('/api/weibo/update', methods=['POST'])
@weibo_owner_required
def update():
    form: dict = request.json
    weibo_id = int(form.pop('id'))
    w = Weibo.update(weibo_id, **form)
    return jsonify(w.json())


@bp.route('/api/weibo/comment_add', methods=['POST'])
@login_required
def comment_add():
    u = current_user()
    form: dict = request.json
    weibo = Weibo.find_by(id=int(form['id']))
    c = Comment(form)
    c.user_id = u.id
    c.weibo_id = weibo.id
    c.content = form['comment']
    c.save()
    log('comment add', c, u, form)
    return jsonify(c.json())


@bp.route('/api/weibo/comment_delete')
@comment_owner_required
def comment_delete():
    log('删除评论的请求', request.args)
    comment = request.args['comment']
    Comment.delete('content' == comment)
    d = dict(
        message="成功删除 weibo 评论"
    )
    return jsonify(d)


# @bp.route('/api/comment/edit')
# @comment_owner_required
# def comment_edit():
#     comment_id = request.args['id']
#     c = Comment.find_by(id=comment_id)
#     log('comment edit', comment_id, c)
#     d = dict(
#         message="编辑 weibo 评论",
#     )
#     return jsonify(d)


# 更新评论的路由
@bp.route('/api/weibo/comment_update', methods=['POST'])
@comment_owner_required
def comment_update():
    form: dict = request.json
    log('更新评论的请求', form)
    comment = form['comment']
    weibo_id = int(form.pop('id'))
    c = Comment.find_by(content=comment, weibo_id=weibo_id)
    log('要修改的comment', c, weibo_id)
    c.content = form['newComment']
    c.save()
    log('comment update', comment, form['newComment'])
    return jsonify(c.json())