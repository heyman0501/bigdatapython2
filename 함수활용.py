# fitness_rewards_webapp.py

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_mail import Mail, Message
from datetime import datetime, timedelta
from twilio.rest import Client
from collections import defaultdict
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Mail config (for Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'
app.config['MAIL_USE_TLS'] = True

# Twilio config (if using SMS)
TWILIO_SID = 'your_twilio_sid'
TWILIO_TOKEN = 'your_twilio_token'
TWILIO_NUMBER = '+1234567890'

mail = Mail(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
client = Client(TWILIO_SID, TWILIO_TOKEN)

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    points = db.Column(db.Integer, default=0)
    goals = db.relationship('Goal', backref='user')

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    is_done = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Gym(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and user.password == request.form['password']:
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', goals=goals)

@app.route('/add-goal', methods=['POST'])
@login_required
def add_goal():
    new_goal = Goal(content=request.form['content'], user_id=current_user.id)
    db.session.add(new_goal)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/complete-goal/<int:goal_id>')
@login_required
def complete_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.user_id != current_user.id:
        return redirect(url_for('dashboard'))
    if not goal.is_done:
        goal.is_done = True
        goal.completed_at = datetime.utcnow()
        current_user.points += 10
        db.session.commit()

        # Send email
        msg = Message('운동 목표 달성!', sender='your_email@gmail.com', recipients=[current_user.email])
        msg.body = f"축하합니다! '{goal.content}' 목표를 완료하고 10포인트를 획득했습니다."
        mail.send(msg)

        # Send SMS (optional)
        # client.messages.create(body=f"🎉 목표 완료: {goal.content}", from_=TWILIO_NUMBER, to='+821012345678')

    return redirect(url_for('dashboard'))

@app.route('/gyms')
@login_required
def gyms():
    gym_list = Gym.query.all()
    return render_template('gym_map.html', gyms=gym_list)

@app.route('/admin/add-gym', methods=['GET', 'POST'])
@login_required
def add_gym():
    if current_user.email != 'admin@example.com':
        flash("관리자만 접근 가능합니다.")
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        gym = Gym(name=request.form['name'], lat=float(request.form['lat']), lng=float(request.form['lng']))
        db.session.add(gym)
        db.session.commit()
        flash("제휴처가 등록되었습니다.")
        return redirect(url_for('gyms'))
    return render_template('admin_add_gym.html')

@app.route('/stats')
@login_required
def stats():
    base = datetime.utcnow().date()
    date_counts = defaultdict(int)
    goals = Goal.query.filter_by(user_id=current_user.id, is_done=True).all()
    for goal in goals:
        if goal.completed_at:
            day = goal.completed_at.date()
            date_counts[day] += 1
    labels = [(base - timedelta(days=i)).strftime('%Y-%m-%d') for i in reversed(range(7))]
    values = [date_counts.get(datetime.strptime(d, '%Y-%m-%d').date(), 0) for d in labels]
    return render_template('stats.html', labels=labels, values=values)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
