from routes import current_user
from models.todo import Todo

from flask import (
    request,
    redirect,
    jsonify,
    Blueprint,
    current_app
)

# endpoint
bp = Blueprint('api_todo', __name__)


# 本文件只返回 json 格式的数据
# 而不是 html 格式的数据
@bp.route('/api/todo/all')
def all():
    todos = Todo.all_json()
    return jsonify(todos)


@bp.route('/api/todo/add', methods=['POST'])
def add():
    # 得到浏览器发送的表单, 浏览器用 ajax 发送 json 格式的数据过来
    # 所以这里我们用新增加的 json 函数来获取格式化后的 json 数据
    form = request.json
    # 创建一个 todo
    u = current_user()
    t = Todo.add(form, u.id)
    # 把创建好的 todo 返回给浏览器
    return jsonify(t.json())


@bp.route('/api/todo/delete')
def delete():
    todo_id = int(request.args['id'])
    Todo.delete(todo_id)
    d = dict(
        message="成功删除 todo"
    )
    return jsonify(d)


@bp.route('/api/todo/update', methods=['POST'])
def update():
    form: dict = request.json
    todo_id = int(form.pop('id'))
    t = Todo.update(todo_id, **form)
    return jsonify(t.json())
