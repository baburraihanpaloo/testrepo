from flask import Flask, render_template, url_for, request, redirect
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
import secrets
key = secrets.token_hex(16)

app = Flask(__name__)
app.secret_key = key  # Needed for session management

# Initialize the flask_login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # This sets the default redirect route for unauthenticated access

# Create a dummy User class (for now, no database)
class User(UserMixin): # User class is a child class of UserMixin now
    def __init__(self, id):
        self.id = id

# Hardcoded users dictionary
users = {'alice': {'password': 'password123'}, 'bob': {'password': 'mypassword'}, 'reyan': {'password': '222'}}

# User loader (to get User object from ID)
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
@app.route('/home')
def home():
    return "🏠 Welcome! <a href='/dashboard'>Dashboard</a> | <a href='/login'>Login</a>"

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = users.get(username)     # checks for a user key based on what the user name is as per our dict
        if user_data and user_data['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('dashboard'))
        return "Invalid credentials. <a href='/login'>Try again</a>"
    return '''
    <form method="POST">
        <h1>Login User</h1>
        Username: <input type="text" name="username"/><br/>
        Password: <input type="password" name="password"/><br/>
        <input type="submit" value="Login"/>
    </form>
    '''

@app.route('/dashboard')
@login_required
def dashboard():
    return f"Welcome {current_user.id}! <a href='/logout'>Logout</a>"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)