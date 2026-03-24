# ── Imports ──────────────────────────────────────────────


from flask import (Blueprint, render_template, redirect,


                   url_for, flash, request)


from flask_login import login_required, current_user


from app import db


from app.models import Application, Notification, Document, User


from app.utils import coordinator_required


 


# ── Blueprint ────────────────────────────────────────────


coordinator = Blueprint('coordinator', __name__)


 


# ── Dashboard ────────────────────────────────────────────


@coordinator.route('/dashboard')


@login_required


@coordinator_required


def dashboard():


    all_applications = Application.query.order_by(


                           Application.submitted_at.desc()).all()


    total     = len(all_applications)


    pending   = sum(1 for a in all_applications


                    if a.status in ['Submitted', 'Pending'])


    approved  = sum(1 for a in all_applications


                    if a.status == 'Approved')


    rejected  = sum(1 for a in all_applications


                    if a.status == 'Rejected')


    return render_template('coordinator/dashboard.html',


                           applications=all_applications,


                           total=total, pending=pending,


                           approved=approved, rejected=rejected)


 


# ── Review single application ────────────────────────────


@coordinator.route('/review/<int:app_id>')


@login_required


@coordinator_required


def review(app_id):


    application = Application.query.get_or_404(app_id)


    documents   = Document.query.filter_by(


                      user_id=application.student_id).all()


    return render_template('coordinator/review.html',


                           application=application,


                           documents=documents)


 


# ── Submit decision ──────────────────────────────────────


@coordinator.route('/decide/<int:app_id>', methods=['POST'])


@login_required


@coordinator_required


def decide(app_id):


    application = Application.query.get_or_404(app_id)


    new_status  = request.form.get('status')


    feedback    = request.form.get('feedback', '')


    valid_statuses = ['Approved', 'Rejected',


                      'More Info Needed', 'Pending']


    if new_status not in valid_statuses:


        flash('Invalid status selected.', 'danger')


        return redirect(url_for('coordinator.dashboard'))


    application.status      = new_status


    application.feedback    = feedback


    application.reviewed_by = current_user.id


    msg = (


        f"Your application for '{application.placement.title}'"


        f" at {application.placement.company.name}"


        f" has been updated: {new_status}."


    )


    if feedback:


        msg += f" Note: {feedback}"


    notification = Notification(


        user_id=application.student_id,


        message=msg


    )


    db.session.add(notification)


    db.session.commit()


    flash(f'Application marked as {new_status} and student notified.',


          'success')


    return redirect(url_for('coordinator.dashboard'))

# ── Account settings ─────────────────────────────────────
@coordinator.route('/settings', methods=['GET', 'POST'])
@login_required
@coordinator_required
def settings():
    from app import bcrypt
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'change_email':
            new_email = request.form.get('new_email')
            existing  = User.query.filter_by(
                            email=new_email).first()
            if existing and existing.id != current_user.id:
                flash('That email is already in use.', 'danger')
            else:
                current_user.email = new_email
                db.session.commit()
                flash('Email updated successfully.', 'success')
        elif action == 'change_password':
            current_pw = request.form.get('current_password')
            new_pw     = request.form.get('new_password')
            confirm_pw = request.form.get('confirm_password')
            if not bcrypt.check_password_hash(
                    current_user.password_hash, current_pw):
                flash('Current password is incorrect.', 'danger')
            elif len(new_pw) < 8:
                flash('New password must be at least 8 characters.', 'danger')
            elif new_pw != confirm_pw:
                flash('New passwords do not match.', 'danger')
            else:
                current_user.password_hash = bcrypt.generate_password_hash(
                                                 new_pw).decode('utf-8')
                db.session.commit()
                flash('Password updated successfully.', 'success')
        return redirect(url_for('coordinator.settings'))
    return render_template('coordinator/settings.html')
