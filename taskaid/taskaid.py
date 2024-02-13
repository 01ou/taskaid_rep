from flask import Blueprint
from db import User

# ブループリントの作成
bp = Blueprint('my_blueprint', __name__)

# ブループリントにルートを追加
@bp.route('/')
def index():
    return 'Hello from my blueprint!'

# アプリケーションにブループリントを登録する関数
def register_blueprint(app):
    app.register_blueprint(bp)

# ブループリントを単独で実行するためのデバッグコード
if __name__ == '__main__':
    from flask import Flask

    app = Flask(__name__)
    register_blueprint(app)
    app.run(debug=True)
