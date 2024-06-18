from flask import Flask,render_template

# Flask Instance
app = Flask(__name__)

# Filters:-
# 1.safe
# 2.capitalise
# 3.lower
# 4.upper
# 5.title
# 6.trim
# 7.striptags

# Localhost
@app.route("/")
def index():
    return "<h1>Hello, World!</h1>"


# Localhost/user
@app.route("/user/<name>")
def user(name):
    return f"<h1>Hello {name}</h1>"

# Create custom Error Pages

# Invalid URL Error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500