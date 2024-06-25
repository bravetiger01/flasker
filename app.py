from flask import Flask, render_template, flash, redirect,url_for,request
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

import uuid as uuid
import os

from flask_login import UserMixin, login_user, LoginManager,login_required, logout_user, current_user

from webforms import LoginForm,PostForms,UserForm,PasswordForm,NamerForm,SearchForm

from flask_ckeditor import CKEditor

# Create a Flask Instance
app = Flask(__name__)

UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Add CKEditor
ckeditor = CKEditor(app)
# Add Database

# Old SQLite DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# New MySQL DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:nakuldesai2510@localhost/our_users'
# Secret Key!
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"
# Initialize The Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Flask Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

# Pass stuff to Navbar
@app.context_processor
def base():
	form = SearchForm()
	return dict(form=form)

# Create Admin Page
@app.route('/admin')
@login_required
def admin():
	id = current_user.id
	if id == 1:
		return render_template("admin.html")
	else:
		flash("Sorry You can't access this page.......")
		return redirect(url_for('dashboard'))
		

# Search Function
@app.route('/search', methods=["POST"])
def search():
	form = SearchForm()
	posts = Posts.query
	if form.validate_on_submit():
		# Get Data from submitted form
		post.searched = form.searched.data
		# Query the database
		posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
		posts = posts.order_by(Posts.title).all()

		return render_template("search.html", form=form, searched=post.searched, posts=posts)


# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(username=form.username.data).first()
		if user:
			# Check the hash
			if check_password_hash(user.password_hash, form.password.data):
				login_user(user)
				flash("Login Success")
				return redirect(url_for('dashboard'))
			else:
				flash("Wrong Credentials - Try Again!")
		else:
			flash("User Does Not Exist!")
	return render_template('login.html', form=form)

# Logout Page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	flash("You Have Been Logged Out!")
	return redirect(url_for('login'))

# Login Page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
	form = UserForm()
	id = current_user.id
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		name_to_update.field = request.form['field']
		name_to_update.username = request.form['username']
		name_to_update.about_author = request.form['about_author']
		name_to_update.profile_pic = request.files['profile_pic']
		
		
		# Grab File Name
		pic_filename = secure_filename(name_to_update.profile_pic.filename)
		# Set UUID
		pic_name = str(uuid.uuid1()) + '_' + pic_filename
		# Save the file
		saver = request.files['profile_pic']
		

		# Change it to a string to save to db
		name_to_update.profile_pic = pic_name
		try:
			db.session.commit()
			saver.save(os.path.join(app.config['UPLOAD_FOLDER']), pic_name)
			flash("User Updated Successfully!")
			return render_template("dashboard.html", 
				form=form,
				name_to_update = name_to_update)
		except:
			flash("Error!  Looks like there was a problem...try again!")
			return render_template("dashboard.html", 
				form=form,
				name_to_update = name_to_update)
	else:
		return render_template("dashboard.html", 
				form=form,
				name_to_update = name_to_update,
				id = id)

# Json Thing
@app.route('/date')
def get_current_date():
	favorite_pizza = {
		"John": "Pepperoni",
		"Mary": "Mushroom",
		"David": "Cheese",

	}
	return favorite_pizza







@app.route('/posts')
def posts():
	# Grab all the post from database
	posts = Posts.query.order_by(Posts.date_posted)
	return render_template('posts.html', posts=posts)

@app.route('/posts/<int:id>')
def post(id):
	post = Posts.query.get_or_404(id)
	return render_template('post.html', post=post)

@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_post(id):
	post = Posts.query.get_or_404(id)
	form = PostForms()

	if form.validate_on_submit():
		post.title = form.title.data
		# post.author = form.author.data
		post.content = form.content.data
		post.slug = form.slug.data

		# Update database
		db.session.add(post)
		db.session.commit()

		flash("Blog Post has been Updated Successfully!!")
	
		# Redirect Webpage
		return redirect(url_for('post', id=id))
	
	if current_user.id == post.poster_id:
		form.title.data = post.title
		# form.author.data = post.author
		form.content.data= post.content
		form.slug.data = post.slug
		return render_template('edit_post.html', form=form)
	
	else:
		flash("You are not authorized to edit this post")
		return redirect(url_for('posts'))

@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
	post_to_delete = Posts.query.get_or_404(id)
	id1 = current_user.id

	if id1 == post_to_delete.poster.id:
		try:
			db.session.delete(post_to_delete)
			db.session.commit()

			flash("Blog Deleted Successfully!!")

			# Grab all the post from database
			posts = Posts.query.order_by(Posts.date_posted)
			return redirect(url_for('posts'))
		
		except:
			flash("Whoops!! There was an error deleting blog")

			# Grab all the post from database
			posts = Posts.query.order_by(Posts.date_posted)
			return redirect(url_for('posts'))
	else:
		flash("You Aren't Authorized to delete that post")

		# Grab all the post from database
		posts = Posts.query.order_by(Posts.date_posted)
		return redirect(url_for('posts'))

# Add Post Page
@app.route('/add-post', methods=["GET", "POST"])
@login_required
def add_post():
	form = PostForms()

	if form.validate_on_submit():
		poster = current_user.id
		post = Posts(title=form.title.data,poster_id=poster,content=form.content.data,slug=form.slug.data,)
		# Clear The Form
		form.title.data = ''
		# form.author.data = ''
		form.content.data = ''
		form.slug.data = ''

		# Add Post Data to Database
		db.session.add(post)
		db.session.commit()

		flash("Blog Post Submitted Successfully!!")
	
	# Return Webpage
	return render_template('add_post.html', form=form)



@app.route('/delete/<int:id>')
def delete(id):
	user_to_delete = Users.query.get_or_404(id)
	name = None
	form = UserForm()

	try:
		db.session.delete(user_to_delete)
		db.session.commit()
		flash("User Deleted Successfully!!")

		our_users = Users.query.order_by(Users.date_added).all()
		return render_template("add_user.html", 
		form=form,
		name=name,
		our_users=our_users)

	except:
		flash("Whoops! There was a problem deleting user, try again...")
		return render_template("add_user.html", 
		form=form, name=name,our_users=our_users)



# Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
	form = UserForm()
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		name_to_update.field = request.form['field']
		name_to_update.username = request.form['username']
		try:
			db.session.commit()
			flash("User Updated Successfully!")
			return render_template("update.html", 
				form=form,
				name_to_update = name_to_update)
		except:
			flash("Error!  Looks like there was a problem...try again!")
			return render_template("update.html", 
				form=form,
				name_to_update = name_to_update)
	else:
		return render_template("update.html", 
				form=form,
				name_to_update = name_to_update,
				id = id)




#def index():
#	return "<h1>Hello World!</h1>"

# FILTERS!!!
#safe
#capitalize
#lower
#upper
#title
#trim
#striptags


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
	name = None
	form = UserForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None:
			# Hash the password!!!
			hashed_pw = generate_password_hash(form.password_hash.data)
			user = Users(username=form.username.data,name=form.name.data, email=form.email.data, field=form.field.data, password_hash=hashed_pw)
			db.session.add(user)
			db.session.commit()
		name = form.name.data
		form.name.data = ''
		form.username.data = ''
		form.email.data = ''
		form.field.data = ''
		form.password_hash.data = ''

		flash("User Added Successfully!")
	our_users = Users.query.order_by(Users.date_added).all()
	return render_template("add_user.html", 
		form=form,
		name=name,
		our_users=our_users)

# Create a route decorator
@app.route('/')
def index():
	first_name = "John"
	stuff = "This is bold text"

	favorite_pizza = ["Pepperoni", "Cheese", "Mushrooms", 41]
	return render_template("index.html", 
		first_name=first_name,
		stuff=stuff,
		favorite_pizza = favorite_pizza)

# localhost:5000/user/John
@app.route('/user/<name>')
def user(name):
	return render_template("user.html", user_name=name)

## Create Custom Error Pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500

# Create Password Test Page
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
	email = None
	password = None
	pw_to_check = None
	passed = None
	form = PasswordForm()


	# Validate Form
	if form.validate_on_submit():
		email = form.email.data
		password = form.password_hash.data
		# Clear the form
		form.email.data = ''
		form.password_hash.data = ''

		# Lookup User By Email Address
		pw_to_check = Users.query.filter_by(email=email).first()
		
		# Check Hashed Password
		passed = check_password_hash(pw_to_check.password_hash, password)

	return render_template("test_pw.html", 
		email = email,
		password = password,
		pw_to_check = pw_to_check,
		passed = passed,
		form = form)


# Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
	name = None
	form = NamerForm()
	# Validate Form
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ''
		flash("Form Submitted Successfully!")
		
	return render_template("name.html", 
		name = name,
		form = form)

# Create Model
class Users(db.Model,UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(120), nullable=False, unique=True)
	field = db.Column(db.String(120))
	about_author = db.Column(db.Text(500), nullable=True)
	date_added = db.Column(db.DateTime, default=datetime.now)
	profile_pic = db.Column(db.String, nullable=True)
	# Do some password stuff!
	password_hash = db.Column(db.String(200))

	# User can have many posts
	posts = db.relationship('Posts', backref='poster')

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute!')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	# Create A String
	def __repr__(self):
		return '<Name %r>' % self.name
	
class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), nullable=False)
	content = db.Column(db.Text, nullable=False)
	# author = db.Column(db.String(255), nullable=False)
	date_posted = db.Column(db.DateTime, default=datetime.now())
	slug = db.Column(db.String(255), nullable=False)

	# Foreign Key To Link Users (refers to the primary key of user)
	poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
