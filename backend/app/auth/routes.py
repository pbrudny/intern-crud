"""Authentication routes."""
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import auth
from app.auth.forms import LoginForm, RegistrationForm
from app.models.user import User


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if this is the first user (auto-admin)
        user_count = User.query.count()
        is_first_user = user_count == 0

        # Create new user
        user = User(
            email=form.email.data.lower(),
            is_admin=is_first_user
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        # Log the user in
        login_user(user)

        if is_first_user:
            flash('Registration successful! You are the first user and have been granted administrator privileges.', 'success')
        else:
            flash('Registration successful! You can now create your intern profile.', 'success')

        return redirect(url_for('index'))

    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password. Please try again.', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        flash(f'Welcome back, {user.email}!', 'success')

        # Redirect to next page or home
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('index'))

    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    """User logout route."""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

