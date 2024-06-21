import os 
import json
from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_required,current_user
from flask_mail import Mail
from flask import Flask
import os

# Get the absolute path of the current file
current_file_path = os.path.abspath(__file__)

# Get the directory containing the current file
current_directory = os.path.dirname(current_file_path)

# Create a Flask app and provide the path to the directory containing the templates directory
app = Flask(__name__, template_folder=current_directory + '/templates')
#db connection
app=Flask(__name__)
app.secret_key='sjbit'

# Get the absolute path of the current file
current_file_path = os.path.abspath(__file__)

# Get the directory containing the current file
current_directory = os.path.dirname(current_file_path)

# Create the path for the database file
database_file_path = os.path.join(current_directory, 'test.db')

# Use the path for the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_file_path

db=SQLAlchemy(app)

login_manager=LoginManager(app)
login_manager.login_view='login'

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    collectionDate = db.Column(db.String(50))
    collectionTime = db.Column(db.String(50))
    imagePath = db.Column(db.String(50))

class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rest of your code...
class Complaints(db.Model):
    cid=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(50))
    message=db.Column(db.String(50))
    date=db.Column(db.String(50),nullable=False)
    image=db.Column(db.String(50))

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    message = db.Column(db.String(50))
    date = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(50))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email Already Exist", "warning")
            return render_template('/signup.html')

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Signup Successful. Please Login", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login Successful", "success")
            return redirect(url_for('index'))

        else:
            flash("Invalid credentials", "danger")

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout Succesful","warning")
    return redirect(url_for('login'))   

@app.route('/admin')
@login_required
def admin():
    system = {
        'uptime': 'Your system uptime value',
        'response_time': 'Your system response time value'
    }
    collections = Collection.query.all()  # Assuming you have a Collection model
    return render_template('admin.html', system=system, collections=collections)
    
@app.route('/schedule', methods=['POST', 'GET'])
@login_required
def schedule():
    if request.method == 'POST':
        email=request.form.get('email')
        message=request.form.get('message')
        date=request.form.get('date')
        image=request.form.get('image')
        new_schedule = Schedule(email=email, message=message, date=date, image=image)
        db.session.add(new_schedule)
        db.session.commit()
        flash("Schedule created successfully", "success")
        return redirect(url_for('index'))
    return render_template('schedule.html')

@app.route('/schedules')
@login_required
def schedules():
    schedules = Schedule.query.all()
    return render_template('schedules.html', schedules=schedules)

@app.route('/areadetails')
@login_required
def area():
    return render_template('areadetails.html')

@app.route("/edit/<string:cid>",methods=['POST','GET'])
@login_required
def edit(cid):
    posts=Complaints.query.filter_by(cid=cid).first()
    if request.method=="POST":
        email=request.form.get('email')
        message=request.form.get('message')
        date=request.form.get('date')
        image=request.form.get('image')
        posts.email = email
        posts.message = message
        posts.date = date
        posts.image = image
        db.session.commit()
        flash("Slot is Updates","success")
        return redirect('/complaint')

    return render_template('edit.html',query=posts)

app.run(debug=True)