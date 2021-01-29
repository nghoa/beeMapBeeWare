from flask import Blueprint, render_template, redirect, url_for, request

from . import admin_blueprint

@admin_blueprint.route('/')
def profile():
    return render_template('profile.html')

@admin_blueprint.route('/login')
def login():
    return render_template('login.html')

@admin_blueprint.route('/logout')
def logout():
    return 'Logout'

@admin_blueprint.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # user = User.query.filter_by(email=email).first()

    # # check if the user actually exists
    # # take the user-supplied password, hash it, and compare it to the hashed password in the database
    # if not user or not check_password_hash(user.password, password):
    #     flash('Please check your login details and try again.')
    #     return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('admin.profile'))