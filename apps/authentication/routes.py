from flask import render_template, redirect, url_for, flash, request
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from flask_dance.contrib.github import github

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm, ForgotPasswordForm, UpdatePasswordForm
from apps.authentication.models import Users
from apps.authentication.util import *
from itsdangerous import URLSafeTimedSerializer
from .email import send_reset_password_email


@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))

# Login & Registration

@blueprint.route("/github")
def login_github():
    if not github.authorized:
        return redirect(url_for("github.login"))

    res = github.get("/user")
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        user_id  = request.form['username'] # we can have here username OR email
        password = request.form['password']

        # Locate user
        user = Users.find_by_username(user_id)

        # if user not found
        if not user:

            user = Users.find_by_email(user_id)

            if not user:
                return render_template( 'accounts/login.html',
                                        msg='Unknown User or Email',
                                        form=login_form)

        # Check the password
        if verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()

        return render_template('accounts/register.html',
                               msg='User created successfully.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login')) 

# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500

# Configura la clave secreta para generar tokens
SECRET_KEY = 'tu_clave_secreta'
serializer = URLSafeTimedSerializer(SECRET_KEY)

# Ruta para solicitar el restablecimiento de contraseña
@blueprint.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        user = Users.find_by_email(email)
        if user:
            # Generar token
            token = serializer.dumps(email, salt='reset-password')

            # Construir URL para restablecimiento de contraseña
            reset_url = url_for('authentication_blueprint.update_password', token=token, _external=True)

            # Enviar correo electrónico
            send_reset_password_email(email, reset_url)

            flash('Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña.', 'success')
            return redirect(url_for('authentication_blueprint.login'))
        else:
            flash('No se encontró ningún usuario con ese correo electrónico.', 'danger')
    return render_template('accounts/forgot_password.html', form=form)

@classmethod
def find_by_email(cls, email: str) -> "Users":
    return cls.query.filter_by(email=email).first()

@blueprint.route('/update_password/<token>', methods=['GET', 'POST'])
def update_password(token):
    try:
        # Verifica el token y obtiene el correo electrónico del usuario
        email = serializer.loads(token, salt='reset-password', max_age=3600)  # Expira después de 1 hora
    except:
        print('El enlace de restablecimiento de contraseña es inválido o ha expirado.')
        return redirect(url_for('authentication_blueprint.forgot_password'))

    user = Users.find_by_email(email)
    if not user:
        print('No se obtuvo el username del email.')
        return redirect(url_for('authentication_blueprint.forgot_password'))

    form = UpdatePasswordForm()
    return render_template('accounts/update_password.html', form=form, username=user.username)


@blueprint.route('/process_update_password', methods=['POST'])
def process_update_password():
    # Obtener los datos del formulario enviado
    email_or_username = request.form.get('email_or_username')
    new_password = request.form.get('password')  # Cambio aquí

    try:
        # Buscar el usuario por su correo electrónico
        user = Users.find_by_email(email_or_username)
        print(user)  # Agregar esta línea para verificar si el usuario se encuentra correctamente
        email_or_username = request.form.get('email_or_username')
        if user:
            hashed_password = hash_pass(new_password)  # Encripta la nueva contraseña
            user.password = hashed_password
            db.session.commit()  # Guarda los cambios en la base de datos

            print('Tu contraseña ha sido actualizada con éxito. Por favor, inicia sesión con tu nueva contraseña.')
            return redirect(url_for('authentication_blueprint.login'))
        else:
            print('No se encontró ningún usuario con ese correo electrónico.')
            return redirect(url_for('authentication_blueprint.forgot_password'))
    except Exception as e:
        print('Se produjo un error al actualizar la contraseña. Por favor, inténtalo de nuevo más tarde.')
        return redirect(url_for('authentication_blueprint.forgot_password'))