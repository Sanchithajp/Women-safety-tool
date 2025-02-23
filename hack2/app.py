from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Change if using another DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Store hashed password in real use

# Create the database tables
with app.app_context():
    db.create_all()

# Route for login page
@app.route('/')
def login_page():
    return render_template('login.html')

# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    # Create a new user and add it to the database
    new_user = User(email=email, password=password)  # Store hashed passwords in production!
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login_page'))  # Redirect to the login page after storing

if __name__ == '__main__':
    app.run(debug=True)
