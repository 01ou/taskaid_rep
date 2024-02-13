import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_TRACK_MODIFICATIONS=False  # 不要なトラッキングを無効化
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # SQLiteデータベースのURIを設定

    db = SQLAlchemy(app)

    if test_config is None:
        # テストしていない場合は、インスタンス構成をロード
        app.config.from_pyfile('config.py', silent=True)
    else:
        # テストの場合は、テスト構成をロード
        app.config.from_mapping(test_config)

    # インスタンスフォルダーが存在することを確認
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # モデルの定義
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        password = db.Column(db.String(120), nullable=False)

    class Post(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(120), nullable=False)
        body = db.Column(db.Text, nullable=False)
        author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        author = db.relationship('User', backref=db.backref('posts', lazy=True))

    # データベースの初期化
    with app.app_context():
        db.create_all()

    # ブループリントの登録
    from . import taskaid
    app.register_blueprint(taskaid.bp)

    # トップページのURLに対してビュー関数を指定する
    app.add_url_rule('/', endpoint='index')

    return app