from flask import render_template, url_for, flash, redirect, request
from mypython import app, db, login_manager, mail
from flask_bcrypt import Bcrypt
from mypython.forms import SignUpForm, SignInForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from mypython.forms import User
from flask_login import login_required, login_user, logout_user, current_user
from urllib.parse import urlparse, urljoin
from flask_mail import Message

bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/') # For the Home Page
def index():
    return render_template('index.html', title='Home')

@app.route('/about') # For the about page
def about():
    return render_template('about.html', title='About US')

@app.route('/contact') # For the contact Page
def contact():
    return render_template('contact.html', title='Contact US')

@app.route('/faq') # For the FAQ Page
def faq():
    return render_template('faq.html', title='FAQ')

@app.route('/pricing') # For the Pricing Page
def pricing():
    return render_template('pricing.html', title='Pricing')

@app.route('/signup', methods=['GET', 'POST']) # For the Sign Up Page
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account Created for {form.firstname.data}!', 'success')
        return redirect(url_for('signin'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')

            if not next_page or urljoin(request.host_url, next_page) != next_page:
                return redirect(url_for('dashboard'))

            return redirect(next_page)
        else:
            flash('Incorrect Username or password', 'danger')
    return render_template('signin.html', title='Sign In', form=form)



@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.email.data = current_user.email

    return render_template('account.html', title="Account", form=form)

def send_reset_email(user):
    token = user.get_reset_token().decode('utf-8')  # Decode bytes to string
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''
    To reset your password, visit the following link:
    {url_for('reset_token', token=token, _external=True)}

    If you did not make this request, please ignore this email and consider changing your email and password.
    '''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Reset password email has been send', 'info')
        return redirect(url_for('signin'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated', 'success')
        return redirect(url_for('signin'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404