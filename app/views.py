from flask import render_template, flash, redirect, request, url_for, g
from flask_login import login_user, logout_user, current_user, login_required

from app import app, db, login_manager

from .forms import LoginForm, RegistrationForm
from .models import User


@app.route('/')
@app.route('/index')
def index():
    user = g.user
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)


@app.before_request
def before_request():
    g.user = current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if user is already logged in
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        flash('Login requested for Username="%s", remember_me=%s' %
              (str(form.username.data), str(form.remember_me.data)))

        registered_user = User.query.filter_by(username=form.username.data,
                                               password=form.password.data).first()
        if registered_user is None:
            flash('Username or Password is Invalid', 'error')
            return redirect(url_for('login'))

        login_user(registered_user, remember=form.remember_me.data)
        flash('Logged in successfully')
        return redirect('/index')

    return render_template('login.html',
                           title="Sign In",
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST' and form.validate():
        user = User(form.username.data,
                    form.password.data,
                    form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
