# ── Imports ─────────────────────────────────────────────


from flask import (Blueprint, render_template, redirect,


                   url_for, flash, request)


from flask_login import login_user, logout_user, login_required


from app import db, bcrypt


from app.models import User


 


# ── Blueprint ────────────────────────────────────────────


auth = Blueprint('auth', __name__)

@auth.route('/')
def home():
    return render_template('home.html')
 


# ── Register ───────────────────────────────────────────── 


@auth.route('/register', methods=['GET', 'POST'])


def register():


    if request.method == 'POST':


        name       = request.form.get('name')


        email      = request.form.get('email')


        password   = request.form.get('password')


        role       = request.form.get('role')


        
        student_num = request.form.get('student_num') or None

 


        existing = User.query.filter_by(email=email).first()


        if existing:


            flash('That email is already registered. Please log in.', 'danger')


            return redirect(url_for('auth.register'))

        if len(password) < 8:
            

            flash('Password must be at least 8 characters long.', 'danger')


            return redirect(url_for('auth.register'))
 


        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')


        user = User(name=name, email=email, password_hash=hashed_pw,


                    role=role, student_num=student_num)


        db.session.add(user)


        db.session.commit()


        flash('Account created! Please log in.', 'success')


        return redirect(url_for('auth.login'))


 


    return render_template('auth/register.html')


 


# ── Login ────────────────────────────────────────────────


@auth.route('/login', methods=['GET', 'POST'])


def login():


    if request.method == 'POST':


        email    = request.form.get('email')


        password = request.form.get('password')


        user = User.query.filter_by(email=email).first()


 


        if user and bcrypt.check_password_hash(user.password_hash, password):


            login_user(user)


            if user.role == 'admin':


                return redirect(url_for('admin.dashboard'))


            elif user.role == 'coordinator':


                return redirect(url_for('coordinator.dashboard'))


            else:


                return redirect(url_for('student.dashboard'))


 


        flash('Incorrect email or password. Please try again.', 'danger')


        return redirect(url_for('auth.login'))


 


    return render_template('auth/login.html')


 


# ── Logout ───────────────────────────────────────────────


@auth.route('/logout')


@login_required


def logout():


    logout_user()


    flash('You have been logged out.', 'info')


    return redirect(url_for('auth.login'))