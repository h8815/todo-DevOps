from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dotenv import load_dotenv
import os
import time
from flask import g

# Import Prometheus libraries
from prometheus_client import generate_latest, Counter, Histogram

# Load environment variables
load_dotenv()
secret_key = os.getenv("SECRET_KEY")

# Flask app configuration
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret_key"

# Database initialization
db = SQLAlchemy(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "warning"


# Prometheus Metrics
REQUESTS = Counter('flask_app_requests_total', 'Total number of requests to the Flask app.')
REQUEST_LATENCY = Histogram('flask_app_request_latency_seconds', 'Request latency in seconds.')


# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Routes
@app.route("/metrics")
def metrics():
    from prometheus_client import CONTENT_TYPE_LATEST
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")
        if title and desc:
            todo = Todo(title=title, desc=desc, user_id=current_user.id)
            db.session.add(todo)
            db.session.commit()
            flash("Task added successfully!", "success")
        else:
            flash("Title and description cannot be empty!", "danger")

    search_query = request.args.get("q")
    if search_query:
        allTodo = Todo.query.filter(
            Todo.user_id == current_user.id, Todo.title.ilike(f"%{search_query}%")
        ).all()
    else:
        allTodo = Todo.query.filter_by(user_id=current_user.id).all()

    return render_template(
        "index.html", allTodo=allTodo, username=current_user.username
    )


@app.before_request
def before_request_metric():
    REQUESTS.inc()
    g.start_time = time.time()


@app.after_request
def after_request_metric(response):
    if hasattr(g, "start_time"):
        latency = time.time() - g.start_time
        REQUEST_LATENCY.observe(latency)
    return response


# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    todos = db.relationship("Todo", backref="owner", lazy=True)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


@app.route("/update/<int:sno>", methods=["GET", "POST"])
@login_required
def update(sno):
    todo = Todo.query.filter_by(sno=sno, user_id=current_user.id).first_or_404()
    if request.method == "POST":
        todo.title = request.form.get("title")
        todo.desc = request.form.get("desc")
        db.session.commit()
        flash("Task updated successfully!", "info")
        return redirect(url_for("home"))
    return render_template("update.html", todo=todo)


@app.route("/delete/<int:sno>")
@login_required
def delete(sno):
    todo = Todo.query.filter_by(sno=sno, user_id=current_user.id).first_or_404()
    db.session.delete(todo)
    db.session.commit()
    flash("Task deleted successfully!", "danger")
    return redirect(url_for("home"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Username and password are required!", "danger")
            return redirect(url_for("register"))

        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "warning")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password!", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))