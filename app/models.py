from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime


# Tells Flask-Login how to load a user from the database
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ── TABLE 1: Users ──────────────────────────────────────
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role          = db.Column(db.String(20),  nullable=False)
    student_num   = db.Column(db.String(20),  unique=True, nullable=True)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    applications  = db.relationship('Application', backref='student',
                        lazy=True, foreign_keys='Application.student_id')
    documents     = db.relationship('Document',    backref='owner', lazy=True)
    notifications = db.relationship('Notification', backref='user',  lazy=True)

    def __repr__(self):
        return f"User('{self.email}', '{self.role}')"


# ── TABLE 2: Companies ──────────────────────────────────
class Company(db.Model):
    __tablename__ = 'companies'
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(150), nullable=False)
    industry = db.Column(db.String(100))
    location = db.Column(db.String(150))
    contact  = db.Column(db.String(120))
    website  = db.Column(db.String(200))

    placements = db.relationship('Placement', backref='company', lazy=True)


# ── TABLE 3: Placements (Internship Opportunities) ──────
class Placement(db.Model):
    __tablename__ = 'placements'
    id          = db.Column(db.Integer, primary_key=True)
    company_id  = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    title       = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    duration    = db.Column(db.String(50))
    deadline    = db.Column(db.DateTime, nullable=False)
    slots       = db.Column(db.Integer, default=1)
    is_active   = db.Column(db.Boolean, default=True)
    posted_by   = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship('Application', backref='placement', lazy=True)


# ── TABLE 4: Applications ───────────────────────────────
class Application(db.Model):
    __tablename__ = 'applications'
    id           = db.Column(db.Integer, primary_key=True)
    student_id   = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    placement_id = db.Column(db.Integer, db.ForeignKey('placements.id'), nullable=False)
    status       = db.Column(db.String(20), default='Submitted')
    feedback     = db.Column(db.Text)
    reviewed_by  = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at   = db.Column(db.DateTime, onupdate=datetime.utcnow)


# ── TABLE 5: Documents ──────────────────────────────────
class Document(db.Model):
    __tablename__ = 'documents'
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doc_type    = db.Column(db.String(50),  nullable=False)
    filename    = db.Column(db.String(200), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


# ── TABLE 6: Notifications ──────────────────────────────
class Notification(db.Model):
    __tablename__ = 'notifications'
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message    = db.Column(db.Text, nullable=False)
    is_read    = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

