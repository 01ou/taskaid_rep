from . import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    subject_tag = db.Column(db.String, nullable=False)
    submission_target = db.Column(db.DateTime)
    single_task = db.Column(db.Boolean, nullable=False, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))

class Page(db.Model):
    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True)
    submission_datetime = db.Column(db.DateTime)
    page_number = db.Column(db.Integer)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    page_state = db.Column(db.String, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    task = db.relationship("Task", backref="pages")

class Schedule(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True)
    target_submission_date = db.Column(db.Date)
    page_range = db.Column(db.String)
    time_per_page = db.Column(db.Integer, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    task = db.relationship("Task", backref="schedules")

class ImplementationDate(db.Model):
    __tablename__ = 'implementation_dates'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id', ondelete='CASCADE'), nullable=False)
    schedule = db.relationship("Schedule", backref="implementation_dates")
