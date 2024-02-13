from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

TITLE_LENGTH = 50
BODY_LENGTH = 500
USERNAME_LENGTH = 30
PASSWORD_LENGTH = 20

# データベース接続情報を設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'

# SQLAlchemyオブジェクトを作成
db = SQLAlchemy(app)

# データベースのモデルを定義
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(TITLE_LENGTH), nullable=False)
    body = db.Column(db.String(BODY_LENGTH), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return '<Post %r>' % self.id
    

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(USERNAME_LENGTH), nullable=False, unique=True)
    password = db.Column(db.String(PASSWORD_LENGTH), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        error = check_signup(username, password)
        if error is not None:
            flash(error)
            return redirect(url_for('signup'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('このユーザー名は既に使用されています。別のユーザー名を選択してください。')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha512')
        user = User(username=username, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        # ユーザーをログインする
        return login_and_display_blog(user)

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash('ユーザー名またはパスワードが正しくありません。')
            return redirect(url_for('login'))

        return login_and_display_blog(user)
    
    return render_template('login.html')


def login_and_display_blog(user):
    login_user(user)
    if current_user.is_authenticated:
        return redirect(url_for('blog'))
    else:
        flash('ログインに失敗しました。再度お試しください。')
        return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/blog')
@login_required
def blog():
    posts = Post.query.all()
    return render_template('blog.html', posts=posts)


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        
        error = check_post(title, body)
        if error is not None:
            flash(error)
            return redirect(url_for('create'))

        post = Post(title=title, body=body)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog'))
    
    return render_template('create.html')


@app.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    post = Post.query.get(id)

    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')

        error = check_post(title, body)
        if error is not None:
            flash(error)
            return redirect(url_for('update', id=post.id))

        post.title = title
        post.body = body
        db.session.commit()
        flash('投稿が更新されました。')
        return redirect(url_for('blog'))
    
    return render_template('update.html', post=post)


@app.route('/<int:id>/delete', methods=['GET'])
@login_required
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    flash('投稿が削除されました。')
    return redirect(url_for('blog'))


def check_post(title, body):
    if not title or not body:
        return 'タイトルと本文は必須です'
    elif len(title) > TITLE_LENGTH:
        return f'タイトルは{TITLE_LENGTH}字以内の長さに納めてください。現在 : {len(title)}字。'
    elif len(body) > BODY_LENGTH:
        return f'本文は{BODY_LENGTH}字以内の長さに納めてください。現在 : {len(body)}字。'
    return None


def check_signup(username, password):
    if not username or not password:
        return 'ユーザー名とパスワードは必須です'
    elif len(username) > USERNAME_LENGTH:
        return f'ユーザー名は{USERNAME_LENGTH}字以内の長さに納めてください。現在 : {len(username)}字。'
    elif len(password) > PASSWORD_LENGTH:
        return f'パスワードは{PASSWORD_LENGTH}字以内の長さに納めてください。現在 : {len(password)}字。'
    return None


if __name__ == '__main__':
    # アプリケーションを実行する前にデータベースを作成
    print('executed.')
    with app.app_context():
        db.create_all()
        print('created database.')
    
    app.run(debug=True)
