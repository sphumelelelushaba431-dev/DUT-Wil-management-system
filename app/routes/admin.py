# ── Imports ──────────────────────────────────────────────


from datetime import datetime


from flask import (Blueprint, render_template, redirect,


                   url_for, flash, request)


from flask_login import login_required, current_user


from app import db, bcrypt


from app.models import User, Company, Placement, Application


from app.utils import admin_required


 


# ── Blueprint ────────────────────────────────────────────


admin = Blueprint('admin', __name__)


 


# ── Dashboard ────────────────────────────────────────────


@admin.route('/dashboard')


@login_required


@admin_required


def dashboard():


    total_students     = User.query.filter_by(role='student').count()


    total_placements   = Placement.query.count()


    total_companies    = Company.query.count()


    total_applications = Application.query.count()


    recent_users       = User.query.order_by(


                             User.created_at.desc()).limit(5).all()


    return render_template('admin/dashboard.html',


                           total_students=total_students,


                           total_placements=total_placements,


                           total_companies=total_companies,


                           total_applications=total_applications,


                           recent_users=recent_users)


 


# ── Manage users ─────────────────────────────────────────


@admin.route('/users')


@login_required


@admin_required


def manage_users():


    users = User.query.order_by(User.created_at.desc()).all()


    return render_template('admin/users.html', users=users)


 


# ── Delete user ──────────────────────────────────────────


@admin.route('/users/delete/<int:user_id>', methods=['POST'])


@login_required


@admin_required


def delete_user(user_id):


    user = User.query.get_or_404(user_id)


    if user.id == current_user.id:


        flash('Cannot delete the primary admin account.', 'danger')


        return redirect(url_for('admin.manage_users'))


    db.session.delete(user)


    db.session.commit()


    flash(f'User {user.name} deleted.', 'success')


    return redirect(url_for('admin.manage_users'))


 


# ── Add company ──────────────────────────────────────────


@admin.route('/companies/new', methods=['GET', 'POST'])


@login_required


@admin_required


def new_company():


    if request.method == 'POST':


        c = Company(


            name    =request.form.get('name'),


            industry=request.form.get('industry'),


            location=request.form.get('location'),


            contact =request.form.get('contact'),


            website =request.form.get('website')


        )


        db.session.add(c)


        db.session.commit()


        flash('Company added successfully.', 'success')


        return redirect(url_for('admin.new_placement'))


    return render_template('admin/new_company.html')


 


# ── Post placement ───────────────────────────────────────


@admin.route('/placements/new', methods=['GET', 'POST'])


@login_required


@admin_required


def new_placement():


    if request.method == 'POST':


        deadline = datetime.strptime(


            request.form.get('deadline'), '%Y-%m-%d'


        )


        p = Placement(


            company_id =int(request.form.get('company_id')),


            title      =request.form.get('title'),


            description=request.form.get('description'),


            duration   =request.form.get('duration'),


            deadline   =deadline,


            slots      =int(request.form.get('slots', 1)),


            posted_by  =1


        )


        db.session.add(p)


        db.session.commit()


        flash('Placement posted successfully.', 'success')


        return redirect(url_for('admin.dashboard'))


    companies = Company.query.order_by(Company.name).all()


    return render_template('admin/new_placement.html',


                           companies=companies)


 


# ── Reports ──────────────────────────────────────────────


@admin.route('/reports')


@login_required


@admin_required


def reports():


    total_students   = User.query.filter_by(role='student').count()


    total_placements = Placement.query.count()


    total_companies  = Company.query.count()


    approved  = Application.query.filter_by(status='Approved').count()


    rejected  = Application.query.filter_by(status='Rejected').count()


    pending   = Application.query.filter_by(status='Pending').count()


    submitted = Application.query.filter_by(status='Submitted').count()


    more_info = Application.query.filter_by(


                    status='More Info Needed').count()


    placements = Placement.query.order_by(


                     Placement.deadline.asc()).all()


    return render_template('admin/reports.html',


                           total_students=total_students,


                           total_placements=total_placements,


                           total_companies=total_companies,


                           approved=approved, rejected=rejected,


                           pending=pending, submitted=submitted,


                           more_info=more_info,


                           placements=placements)

# ── Edit placement ───────────────────────────────────────
@admin.route('/placements/edit/<int:placement_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_placement(placement_id):
    p = Placement.query.get_or_404(placement_id)
    companies = Company.query.order_by(Company.name).all()
    if request.method == 'POST':
        p.title       = request.form.get('title')
        p.description = request.form.get('description')
        p.duration    = request.form.get('duration')
        p.slots       = int(request.form.get('slots', 1))
        p.company_id  = int(request.form.get('company_id'))
        p.is_active   = request.form.get('is_active') == '1'
        p.deadline    = datetime.strptime(
                            request.form.get('deadline'), '%Y-%m-%d')
        db.session.commit()
        flash('Placement updated successfully.', 'success')
        return redirect(url_for('admin.edit_placement',
                                   placement_id=placement_id))
    return render_template('admin/edit_placement.html',
                           placement=p, companies=companies)


# ── Delete placement ─────────────────────────────────────
@admin.route('/placements/delete/<int:placement_id>', methods=['POST'])
@login_required
@admin_required
def delete_placement(placement_id):
    from app.models import Application
    p = Placement.query.get_or_404(placement_id)
    Application.query.filter_by(placement_id=placement_id).delete()
    db.session.delete(p)
    db.session.commit()
    flash(f'Placement and all linked applications deleted.', 'success')
    return redirect(url_for('admin.reports'))


# ── Edit company ─────────────────────────────────────────
@admin.route('/companies/edit/<int:company_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_company(company_id):
    c = Company.query.get_or_404(company_id)
    if request.method == 'POST':
        c.name     = request.form.get('name')
        c.industry = request.form.get('industry')
        c.location = request.form.get('location')
        c.contact  = request.form.get('contact')
        c.website  = request.form.get('website')
        db.session.commit()
        flash('Company updated successfully.', 'success')
        return redirect(url_for('admin.edit_company',
                                   company_id=company_id))
    return render_template('admin/edit_company.html', company=c)


# ── Edit user ──────────────────────────────────────────── 
@admin.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.name       = request.form.get('name')
        user.email      = request.form.get('email')
        user.role       = request.form.get('role')
        user.student_num= request.form.get('student_num') or None
        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('admin.edit_user', user_id=user_id))
    return render_template('admin/edit_user.html', user=user)

# ── Manage companies ─────────────────────────────────────
@admin.route('/companies')
@login_required
@admin_required
def manage_companies():
    companies = Company.query.order_by(Company.name).all()
    return render_template('admin/manage_companies.html',
                           companies=companies)

# ── Admin account settings ────────────────────────────────
@admin.route('/settings', methods=['GET', 'POST'])
@login_required
@admin_required
def settings():
    from app import bcrypt
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'change_name':
            new_name = request.form.get('new_name', '').strip()
            if not new_name:
                flash('Name cannot be empty.', 'danger')
            else:
                current_user.name = new_name
                db.session.commit()
                flash('Name updated successfully.', 'success')

        elif action == 'change_email':
            new_email = request.form.get('new_email')
            existing  = User.query.filter_by(email=new_email).first()
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

        return redirect(url_for('admin.settings'))
    return render_template('admin/settings.html')

