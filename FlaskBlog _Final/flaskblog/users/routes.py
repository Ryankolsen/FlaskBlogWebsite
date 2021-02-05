# Users blueprint - all user related routes and functions
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

# instance of blueprint object:
users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST']) #used to be @app.route. change to users because that is the name of blueprint in above ode
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.honme'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.honme'))
    form = LoginForm()
    if form.validate_on_submit():    #Does the form validate when submitted? Send one time alert. Must import flash from flask
        user = User.query.filter_by(email=form.email.data).first()  #does the user exist?
        if user and bcrypt.check_password_hash(user.password, form.password.data):   #is there an existing user, is password right?
            login_user(user, remember=form.remember.data)   #login user
            next_page = request.args.get('next')    #takes next parameter (address initially trying to access like account page...or none)
            return redirect(next_page) if next_page else redirect(url_for('main.home'))  #redirect to next page if it exists, if none, return home page redirect
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
@login_required     #can only view page if youre logged in
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:       #if the form has a picture...do something with it
            picture_file = save_picture(form.picture.data)    #save picture and return filename
            current_user.image_file = picture_file          #allows user to set new picture file
        current_user.username = form.username.data  #allows user to revise username
        current_user.email = form.email.data        #allows user to revise email
        db.session.commit()                         #commit to database
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))     #redirect to account page
    elif request.method =='GET':                #else if the request is to get...populate form with current info
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file,
        form=form)

#show all posts for a specific username
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)      #set default page to 1, page number must be an int
    user = User.query.filter_by(username=username).first_or_404()   #get first user, if none return 404 error
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5) #prints only 5 posts per page, order by post date in descending, broken up by \
    return render_template('user_posts.html', posts=posts, user=user) #returns page source, posts added

#allow user to input email to reset password
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit(): #if email is valid:
        user = User.query.filter_by(email=form.email.data).first()  #identify valid email
        send_reset_email(user)
        flash('An email has been sent with instructions to reset password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

#allows user to actually reset password. Need to verify token.
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token,' 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
