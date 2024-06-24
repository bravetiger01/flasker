from flask import Flask, render_template, flash,request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from werkzeug.security import generate_password_hash,check_password_hash

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from datetime import datetime


# Create a Flask Instance
app = Flask(__name__)

## Add Database
# SQLite Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# MySQL Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:nakuldesai2510@localhost/our_users'


# Secret Key
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"

# Initialize Database
db = SQLAlchemy(app)
app.app_context().push()

migrate = Migrate(app, db)

# Create Model
class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(120), nullable=False, unique=True)
	field = db.Column(db.String(120))
	date_added = db.Column(db.DateTime, default=datetime.now)

	# Password Stuff
	password_hash = db.Column(db.String(128))

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')
	
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self,password):
		return check_password_hash(self.password_hash, password)

	# Create String
	def __repr__(self):
		return "<Name %r>" % self.name
	
# Create a Form Class
class UserForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired()])
	field = StringField("Field")
	submit = SubmitField("Submit")


# Create a Form Class
class NamerForm(FlaskForm):
	name = StringField("What's Your Name", validators=[DataRequired()])
	submit = SubmitField("Submit")

	## Form Fields
	# BooleanField
	# DateField
	# DateTimeField
	# DecimalField
	# FileField
	# HiddenField
	# MultipleField
	# FieldList
	# FloatField
	# FormField
	# IntegerField
	# PasswordField
	# RadioField
	# SelectField
	# SelectMultipleField
	# SubmitField
	# StringField
	# TextAreaField

	## Validators
	# DataRequired
	# Email
	# EqualTo
	# InputRequired
	# IPAddress
	# Length
	# MacAddress
	# NumberRange
	# Optional
	# Regexp
	# URL
	# UUID
	# AnyOf
	# NoneOf



# FILTERS!!!
#safe
#capitalize
#lower
#upper
#title
#trim
#striptags


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

# Create Custom Error Pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500

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

# Add User
@app.route('/user/add', methods=["GET", "POST"])
def add_user():
	name = None
	form = UserForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None:
			user = Users(name=form.name.data, email=form.email.data, field=form.field.data)
			db.session.add(user)
			db.session.commit()
		name = form.name.data
		form.name.data = ''
		form.email.data = ''
		form.field.data = ''
		flash("User Added Successfully")
	our_users = Users.query.order_by(Users.date_added).all()
	return render_template("add_user.html", 
							form=form,
							name=name,
							our_users=our_users)

# Update User
@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
	form = UserForm()
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		name_to_update.field = request.form['field']
		try:
			db.session.commit()
			flash("User Updated Successfully")
			return render_template("update.html",
						  			form=form,
									name_to_update=name_to_update)
		except:
			flash("Error!! Looks Like there was an problem!!")
			return render_template("update.html",
						  			form=form,
									name_to_update=name_to_update,
									id=id)
	else:
		return render_template("update.html",
						  			form=form,
									name_to_update=name_to_update)
	
# Delete User
@app.route('/delete/<int:id>', methods=["GET", "POST"])
def delete_user(id):
	user_to_delete = Users.query.get_or_404(id)
	name = None
	form = UserForm()
	try:
		db.session.delete(user_to_delete)
		db.session.commit()
		flash("User Deleted Successfully")
		our_users = Users.query.order_by(Users.date_added).all()
		return render_template("add_user.html",form=form,name=name,our_users=our_users)
	except:
		flash("There was an error deleting the user!!!")
		our_users = Users.query.order_by(Users.date_added).all()
		return render_template("add_user.html",form=form,name=name,our_users=our_users)