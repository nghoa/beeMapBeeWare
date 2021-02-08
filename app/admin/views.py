from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

from app.admin.forms import LoginForm, ChangePasswordForm
from app.admin.models import User
from . import admin_blueprint
from app.services.database import get_suggestions, delete_suggestion, update_suggestion_status

import json
import logging

logger = logging.getLogger()


"""
    Admin dashboard landing page after successful login
"""
@admin_blueprint.route('/')
@login_required
def profile():
    return render_template('profile.html', title='Home')


@admin_blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    print('dashboard')
    suggestions = get_suggestions()
    """
        Structure:
            suggestion.id
            suggestion.location.(longitude | latitude)
            suggestion.firstname
            suggestion.lastname
            suggestion.datetime
            suggestion.confirmed
    """
    return render_template('dashboard.html', title='Dashboard', suggestions=suggestions)


"""
    render Leaflet map
"""
@admin_blueprint.route('/map')
@login_required
def show_map():
    lon = request.args.get('lon')
    lat = request.args.get('lat')
    id = request.args.get('id')
    # return "Longitude: {} and Latitude: {} and Id: {}".format(lon, lat, id)       # just for checking data
    return render_template('dashboard_map.html', id = id, longitude = lon, latitude = lat)


"""
    Delete Suggestion by google Datastore ID
"""
@admin_blueprint.route('/dashboard/delete/<int:id>')
def del_suggestion(id):
    try:
        delete_suggestion(id)
        logger.debug("Suggestion ID:{} successfully deleted".format(id))
        return redirect(url_for('admin.dashboard'))
    except:
        logger.warn("There was a problem with deleting the Suggestion")
        return 'There was a problem with deleting the Suggestion'

"""
    Update Suggestion confirmed status (true | false)
"""
@admin_blueprint.route('/dashboard/update-status', methods=['POST'])
def update_suggestion():
    try:
        data = request.get_json()
        id = int(data['id'])
        # Transcode status to True | False
        status = status_transcode(data['status'])
        update_suggestion_status(id, status)
        logger.debug("Status of ID: {} successfully changed".format(id))
        return redirect(url_for('admin.dashboard'))
    except:
        logger.warn("There was a problem with updating the Suggestion")
        return 'There was a problem with updating the Suggestion'

"""
    Round about way for transmitting status of Suggestion
"""
def status_transcode(status_json):
    if status_json == '1':
        return True
    elif status_json == '0':
        return False
    else:
        logger.warn("Suggestion Status has a type problem")

"""
    Change Password of current user
"""
@admin_blueprint.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        old_password = form.old_password.data
        new_password = form.new_password.data
        user = User().get_obj('Username', current_user.Username)
        if user.check_password(old_password) and old_password != new_password:
            user.set_password(new_password)
            user.save()
            flash('Password successfully changed')
            logger.debug("Password successfully changed")
        else:
            flash('Invalid password')

    return render_template('settings.html', title='Settings', form=form)


@admin_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    # flask login handles the current_user object
    if current_user.is_authenticated:
        logger.debug("Show admin profile")
        return redirect(url_for('admin.profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User().get_obj('Username', form.username.data)
        # check for correct password
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            logger.warn("Invalid username or password inputed")

            return redirect(url_for('admin.login'))

        logger.debug("User logged in")
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':

            logger.debug("Show admin profile page")

            next_page = url_for('admin.profile')
        return redirect(next_page)
    return render_template('login.html', title="Login", form=form)


@admin_blueprint.route('/logout')
def logout():
    logger.debug("User logged out.")
    logout_user()
    return redirect(url_for('admin.profile'))