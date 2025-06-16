from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin

# --------------------------------------------------
#  A. Flask initialisation
# --------------------------------------------------
app = Flask(__name__)
app.secret_key = "change-me-to-a-really-secret-string"   # production में .env या Render Secret में रखें

# --------------------------------------------------
#  B. Login manager (सबसे सरल ver.)
# --------------------------------------------------
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Demo in-memory user (आगे चलकर DB वाले यूज़र से replace कर सकते हैं)
class User(UserMixin):
    def __init__(self, id):
        self.id = id

USERS = {"admin": User("admin")}

@login_manager.user_loader
def load_user(user_id):
    return USERS.get(user_id)

# --------------------------------------------------
#  C. Routes
# --------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # 👉 TODO: असली password check DB से
        if username in USERS:
            login_user(USERS[username])
            return redirect(url_for("dashboard"))
        return "Invalid creds", 401
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# --------------------------------------------------
#  D. Render / Gunicorn के लिये entry-point
# --------------------------------------------------
if __name__ == "__main__":                 # dev पर python app.py चलाने के लिये
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)# Full Flask app with routing, database and user auth
