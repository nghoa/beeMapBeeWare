from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

from app.admin.forms import LoginForm, ChangePasswordForm
from app.admin.models import User
from . import admin_blueprint

"""
    Admin dashboard landing page after successful login
"""
@admin_blueprint.route('/')
@login_required
def profile():
    return render_template('profile.html', title='Home')

@admin_blueprint.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

@admin_blueprint.route('/settings')
@login_required
def settings():
    form = ChangePasswordForm()
    # print(current_user.check_password("test"))
    return render_template('settings.html', title='Settings', form=form)

@admin_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User().get_obj('Username', form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('admin.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('admin.profile')
        return redirect(next_page)
    return render_template('login.html', title="Login", form=form)

@admin_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin.profile'))