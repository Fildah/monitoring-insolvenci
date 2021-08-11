from flask import render_template, url_for, flash, redirect, request, Blueprint, Markup, abort
from flask_login import login_user, current_user, logout_user, login_required

from monitorinsolvenci.emails.email_sender import send_email
from monitorinsolvenci.extensions import db
from monitorinsolvenci.users.forms import RegistrationForm, LoginForm, UpdateUserForm, GenerateApiTokenForm
from monitorinsolvenci.users.models import User

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
        send_email(user.email, 'Úspěšná registrace', 'email/register_email')
        login_user(user)
        return redirect(url_for('partners.user_partners'))
    return render_template('form_register.html', title='Registrace', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.password_check(form.password.data):
            if user.active:
                login_user(user)
                next_page = request.args.get('next')
                if next_page is None or not next_page[0] == '/':
                    next_page = url_for('core.index')
                flash('Byly jste úspěšně přihlášeni.', 'success')
                return redirect(next_page)
            else:
                flash(Markup('Účet je zablokován, požádejte administrátora o aktivaci!'), 'danger')
        else:
            flash(Markup(
                'Chybný email nebo heslo! Pokud ještě účet nemáte, neváhejte se <a href="{}" '
                'class="alert-link">registrovat</a>!'.format(
                    url_for('users.register'))), 'danger')
    return render_template('form_login.html', title='Přihlášení', form=form)


@users.route('/logout', methods=['GET', 'POST'])
@login_required
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
    return render_template('form_account.html',
                           title='Uživatelský účet: {} {}'.format(current_user.first_name, current_user.last_name),
                           form=form)


@users.route('/apitoken', methods=['GET', 'POST'])
@login_required
def api_token():
    form = GenerateApiTokenForm()
    if form.validate_on_submit():
        token = current_user.token
        flash('API Token je zobrazen, překopírujte si ho.', 'success')
        form.token.data = token
    elif request.method == 'GET':
        form.token.data = '********************************'
    return render_template('form_apitoken.html', form=form)


@users.route('/administration', methods=['GET'])
@login_required
def administration():
    if not current_user.admin:
        abort(403)
    return render_template('user_administration.html', title='Administrace uživatelů')


@users.post('/detail/<int:user_id>/toogle_admin')
@login_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    if not current_user.admin or current_user is user or user.id == 1:
        abort(403)
    user.toggle_admin()
    if user.admin:
        flash('Uživatel {} {} nastaven administrátorem.'.format(user.first_name, user.last_name), 'success')
    else:
        flash('Uživatel {} {} odebrán z administrátorů.'.format(user.first_name, user.last_name), 'success')
    return redirect(url_for('users.administration'))


@users.post('/detail/<int:user_id>/toogle_active')
@login_required
def toogle_active(user_id):
    user = User.query.get_or_404(user_id)
    if not current_user.admin or current_user is user or user.id == 1:
        abort(403)
    user.toggle_active()
    if user.admin:
        flash('Uživatel {} {} zaktivněn.'.format(user.first_name, user.last_name), 'success')
    else:
        flash('Uživatel {} {} zneaktivněn.'.format(user.first_name, user.last_name), 'success')
    return redirect(url_for('users.administration'))
