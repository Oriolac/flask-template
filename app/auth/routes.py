from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import login_manager
from . import auth_bp
from .forms import SignupForm, LoginForm
from .models import User

@auth_bp.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        #Comprobació que no hi ha usuari amb email
        user = User.get_by_email(email)
        if user is not None:
            error = f'El email {email} ja està utilitzat per un altre usuari.'
        else:
            # Crear l'usuari i guardar-lo
            user = User(name=name, email=email)
            user.set_password(password)
            user.save()
            # Deixar l'usuari loguejat
            login_user(user, remember=True)
            next = request.args.get('next', None)
            if not next or url_parse(next).netloc != '':
                next = url_for('main.index')
            return redirect(next)
    return render_template("auth/signup_form.html", form=form, error=error)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)
    return render_template('auth/login_form.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))