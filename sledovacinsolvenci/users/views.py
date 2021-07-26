from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from sledovacinsolvenci.extensions import db
from sledovacinsolvenci.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from sledovacinsolvenci.users.models import User

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Děkujeme za registraci.', 'success')
        login_user(user)
        return redirect(url_for('partners.user_partners'))
    return render_template('register.html', title='Registrace', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.password_check(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if next_page is None or not next_page[0] == '/':
                next_page = url_for('core.index')
            flash('Byly jste úspěšně přihlášeni.', 'success')
            return redirect(next_page)
        else:
            flash('Chybný email nebo heslo!', 'warning')
    return render_template('login.html', title='Přihlášení', form=form)


@users.route('/logout')
def logout():
    logout_user()
    flash('Byly jste úspěšně odhlášeni.', 'success')
    return redirect(url_for('core.index'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.commit()
        flash('Uživatelský účet byl aktualizován.', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
    return render_template('account.html',
                           title='Uživatelský účet: {} {}'.format(current_user.first_name, current_user.last_name),
                           form=form)
