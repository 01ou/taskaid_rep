from flask import render_template, url_for, Blueprint, jsonify, request
from . import db
from .models import Task

bp = Blueprint('taskaid_bp', __name__)

@bp.route('/')
def index():
    print("////OK")
    return render_template("index.html")

@bp.route('/create_task', methods=['POST'])
def create_task():
    data = request.json
    name = data.get('name')
    subject_tag = data.get('subject_tag')
    submission_target = data.get('submission_target')
    user_id = data.get('user_id')

    if not name or not subject_tag or not submission_target or not user_id:
        return jsonify({'message': 'Missing required fields'}), 400

    new_task = Task(name=name, subject_tag=subject_tag, submission_target=submission_target, user_id=user_id)
    db.session.add(new_task)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

    return jsonify({'message': 'Task created successfully', 'task_id': new_task.id}), 201
