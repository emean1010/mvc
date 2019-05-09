from flask import Flask

from models import todo
from routes.routes_todo import bp as todo_routes
from routes.api_todo import bp as todo_api
from routes.routes_weibo import bp as weibo_routes
from routes.api_weibo import bp as weibo_api
from routes.routes_user import bp as user_routes
from routes.routes_public import bp as public_routes

app = Flask(__name__)
app.register_blueprint(public_routes)
app.register_blueprint(user_routes)
app.register_blueprint(todo_routes)
app.register_blueprint(todo_api)
app.register_blueprint(weibo_routes)
app.register_blueprint(weibo_api)

if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        debug=True,
        host='127.0.0.1',
        port=3000,
    )
    app.run(**config)
