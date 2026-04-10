#login pages and sign up pages
from flask import Blueprint, flash, render_template,redirect
from .forms import LoginForm, SignUpForm
from .models import Customer
from . import db
auth = Blueprint('auth', __name__)
from flask_login import login_user, logout_user, login_required
# so basically wheneber the user reaches either of these urls these functions will run so this is the logic of those pages
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = Customer.query.filter_by(email=email).first()
        if user:
            if user.verify_password(password=password):
                login_user(user, remember=True)
                flash('Logged in successfully, Welcome')
                #take us to home page
                return redirect('/')

            else:
                flash('Incorrect password')
        else:
            flash('Acount does not exist')
    return render_template('login.html', form=form)
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        # make sure login is correct
        email=  form.email.data
        username = form.username.data
        pasword1 = form.password1.data
        pasword2 = form.password2.data
        if pasword1 == pasword2:
            # add user to database
            new_user = Customer()
            new_user.email = email
            new_user.username = username
            new_user.password = pasword2

            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Account created successfully Log in now !')
                return redirect('/login')
            except Exception as e:
                flash('Account could not be created: ')
                print(e)  # Log the error for debugging purposes
            form.email.data = ''
            form.username.data = ''
            form.password1.data = ''
            form.password2.data = ''


    return render_template('signup.html', form=form)

@auth.route('/logout')
@login_required
def log_out():
    logout_user()
    flash('Logged out successfully')
    return redirect('/login')
    
@auth.route('/cartprofile/<int:user_id>')
@login_required
def view_cart(user_id):
    user = Customer.query.get(user_id)
    return render_template('cartprofile.html', customer=user)
