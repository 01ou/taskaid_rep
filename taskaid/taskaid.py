from flask import Blueprint
from . import create_app

# ブループリントの作成
bp = Blueprint('taskaid_bp', __name__)

# ブループリントにルートを追加
@bp.route('/')
def index():
    return 'Hello from my blueprint!'