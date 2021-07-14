from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from sledovacinsolvenci import db
from sledovacinsolvenci.users.models import User
from sledovacinsolvenci.users.forms import RegistrationForm, LoginForm, UpdateUserForm

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Dekujeme za registraci')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))
