from flask import Flask,render_template
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

# Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"

# Create Form Class
class NamerForm(FlaskForm):
	name = StringField("What's Your Name?", validators=[DataRequired()])
	submit = SubmitField("Submit")

	## Fields
	# BooleanField
	# DateField
	# DateTimeField
	# DecimalField
	# FileField
	# HiddenField
	# MultipleFIeld
	# FIeldList
	# FloatField
	# FormFIeld
	# IntegerField
	# PasswordField
	# RadioField
	# SelectField
	# SelectMultipleField
	# SubmitField
	# StringField
	# TextAreaField

	##Validators
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

# Filters:-
# 1.safe
# 2.capitalise
# 3.lower
# 4.upper
# 5.title
# 6.trim
# 7.striptags


# Localhost
@app.route('/')
def index():
	first_name = "Nakul"
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


# Create custom Error Pages

# Invalid URL Error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

# localhost:5000/user/John
@app.route('/name', methods=["POST", "GET"])
def name():
	name = None
	form = NamerForm()
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ''
	return render_template("name.html",
							name=name,
							form=form)