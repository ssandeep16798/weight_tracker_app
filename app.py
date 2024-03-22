from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
import logging

# Import for declarative base class
from sqlalchemy.orm import declarative_base

app = Flask(__name__)
app.secret_key = 'Sandy@8268'

engine = create_engine('postgresql://sandeep:@localhost/weights-db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal  # Assign SessionLocal to db for easier access
if db == True:
    logging.info("Connected to DB Successfully")
else:
    logging.error("Error connecting to db.")
# Create a base class for your models
Base = declarative_base()

class User(Base):
  __tablename__ = 'users'  # Specify the table name
  id = Column(Integer, primary_key=True)
  username = Column(String(80), unique=True, nullable=False)
  password_hash = Column(String(128), nullable=False)
  name = Column(String(100), nullable=False)
  email = Column(String(100), unique=True, nullable=False)
  date_of_birth = Column(String(100), nullable=False)

  def set_password(self, password):
      self.password_hash = generate_password_hash(password)

  def check_password(self, password):
      return check_password_hash(self.password_hash, password)

# ... rest of your code ...


# ... rest of your code ...

@app.route("/")
def home():
    return render_template('templates/login.html')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[Email(), Length(min=6, max=50)])  # Optional email field
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Register')

    def validate_confirm_password(self, confirm_password):
        if confirm_password.data != self.password.data:
            raise ValueError('Passwords must match')  # Use ValueError for Flask-WTF validation


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password,
            name=''  # Fill in the name field if needed
        )
        db.session.add(new_user)
        db.session.commit()
        logging.info(f'User created successfully: {form.username.data}')
        return redirect(url_for('login'))  # Redirect to login page after registration
    return render_template('templates/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Login form and logic would go here
    return render_template('templates/login.html')  # Replace with your login template name


if __name__ == '__main__':
    app.run(debug=True)  # Only one "if __name__ == '__main__'" block needed
