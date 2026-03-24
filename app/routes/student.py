## ── Imports ──────────────────────────────────────────────

import os
from datetime import datetime
from app.utils import student_required
from werkzeug.utils import secure_filename
from flask import (Blueprint, render_template, redirect,


                   url_for, flash, request, current_app)


from flask_login import login_required, current_user


from app import db


from app.models import Placement, Application, Document, Notification


 


## ── Blueprint & upload settings ──────────────────────────


student = Blueprint('student', __name__)


ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'docx'}


ALLOWED_TYPES = ['cv', 'motivation', 'id', 'matric', 'proof_of_address']


 


def allowed_file(filename):


    return ('.' in filename and


            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)


 


## ── Dashboard ────────────────────────────────────────────


@student.route('/dashboard')


@login_required
@student_required

def dashboard():


    applications  = Application.query.filter_by(


                        student_id=current_user.id).all()


    documents     = Document.query.filter_by(


                        user_id=current_user.id).all()


    unread_count  = Notification.query.filter_by(


                        user_id=current_user.id, is_read=False).count()


    now           = datetime.utcnow()


    return render_template('student/dashboard.html',


                           applications=applications,


                           documents=documents,


                           unread_count=unread_count,


                           now=now)


 


## ── Search placements ────────────────────────────────────


@student.route('/search')


@login_required
@student_required

def search():


    query = request.args.get('q', '')


    if query:


        placements = Placement.query.filter(


            Placement.is_active == True,


            Placement.title.ilike(f'%{query}%')


        ).all()


    else:


        placements = Placement.query.filter_by(is_active=True).all()


    return render_template('student/search.html',


                           placements=placements, query=query)


 


## ── Apply for placement ──────────────────────────────────


@student.route('/apply/<int:placement_id>', methods=['POST'])


@login_required
@student_required

def apply(placement_id):


    placement = Placement.query.get_or_404(placement_id)


    existing  = Application.query.filter_by(


                    student_id=current_user.id,


                    placement_id=placement_id).first()


    if existing:


        flash('You have already applied for this placement.', 'warning')


        return redirect(url_for('student.search'))


    if placement.deadline < datetime.utcnow():


        flash('The deadline for this placement has passed.', 'danger')


        return redirect(url_for('student.search'))


    app_obj = Application(student_id=current_user.id,


                          placement_id=placement_id)


    db.session.add(app_obj)


    db.session.commit()


    flash('Application submitted successfully!', 'success')


    return redirect(url_for('student.dashboard'))


 


## ── Upload document ──────────────────────────────────────


@student.route('/upload', methods=['GET', 'POST'])


@login_required
@student_required

def upload_document():


    if request.method == 'POST':


        doc_type = request.form.get('doc_type')


        file     = request.files.get('document')


        if doc_type not in ALLOWED_TYPES:


            flash('Invalid document type.', 'danger')


            return redirect(url_for('student.upload_document'))


        if not file or not allowed_file(file.filename):


            flash('Only PDF, PNG, JPG, DOCX files allowed.', 'danger')


            return redirect(url_for('student.upload_document'))


        ext      = file.filename.rsplit('.', 1)[1].lower()


        filename = secure_filename(


            f"{current_user.id}_{doc_type}_"


            f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.{ext}"


        )


        upload_folder = current_app.config['UPLOAD_FOLDER']


        os.makedirs(upload_folder, exist_ok=True)


        file.save(os.path.join(upload_folder, filename))


        old = Document.query.filter_by(


                  user_id=current_user.id,


                  doc_type=doc_type).first()


        if old:


            old_path = os.path.join(upload_folder, old.filename)


            if os.path.exists(old_path):


                os.remove(old_path)


            db.session.delete(old)


        doc = Document(user_id=current_user.id,


                       doc_type=doc_type, filename=filename)


        db.session.add(doc)


        db.session.commit()


        flash('Document uploaded successfully.', 'success')


        return redirect(url_for('student.dashboard'))


    docs = Document.query.filter_by(user_id=current_user.id).all()


    return render_template('student/upload.html',


                           docs=docs, allowed_types=ALLOWED_TYPES)


 


## ── Notifications ────────────────────────────────────────


@student.route('/notifications')


@login_required
@student_required

def notifications():


    notifs = Notification.query.filter_by(


                 user_id=current_user.id).order_by(


                 Notification.created_at.desc()).all()


    for n in notifs:


        n.is_read = True


    db.session.commit()


    return render_template('student/notifications.html', notifs=notifs)

# ── Delete document ───────────────────────────────────────
@student.route('/document/delete/<int:doc_id>', methods=['POST'])
@login_required
@student_required
def delete_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    if doc.user_id != current_user.id:
        flash('You do not have permission to delete this document.', 'danger')
        return redirect(url_for('student.upload_document'))
    old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], doc.filename)
    if os.path.exists(old_path):
        os.remove(old_path)
    db.session.delete(doc)
    db.session.commit()
    flash('Document deleted successfully.', 'success')
    return redirect(url_for('student.upload_document'))

# ── Change password ──────────────────────────────────────
@student.route('/settings', methods=['GET', 'POST'])
@login_required
@student_required
def settings():
    from app import bcrypt
    if request.method == 'POST':
        current_pw  = request.form.get('current_password')
        new_pw      = request.form.get('new_password')
        confirm_pw  = request.form.get('confirm_password')
        if not bcrypt.check_password_hash(
                current_user.password_hash, current_pw):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('student.settings'))
        if len(new_pw) < 8:
            flash('New password must be at least 8 characters.', 'danger')
            return redirect(url_for('student.settings'))
        if new_pw != confirm_pw:
            flash('New passwords do not match.', 'danger')
            return redirect(url_for('student.settings'))
        current_user.password_hash = bcrypt.generate_password_hash(
                                         new_pw).decode('utf-8')
        db.session.commit()
        flash('Password updated successfully.', 'success')
        return redirect(url_for('student.settings'))
    return render_template('student/settings.html')