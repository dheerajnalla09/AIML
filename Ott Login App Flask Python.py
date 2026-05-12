from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Dummy user database
users = {
    "admin": "password123",
    "user": "ott123"
}

# Login Page HTML
login_page = """
<!DOCTYPE html>
<html>
<head>
    <title>OTT Platform Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #141414;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .login-box {
            background: #222;
            padding: 30px;
            border-radius: 10px;
            width: 300px;
            text-align: center;
        }

        input {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: none;
            border-radius: 5px;
        }

        button {
            width: 100%;
            padding: 10px;
            background: #e50914;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }

        button:hover {
            background: #ff1f1f;
        }

        .error {
            color: red;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>OTT Login</h2>
        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
"""

# Dashboard Page HTML
home_page = """
<!DOCTYPE html>
<html>
<head>
    <title>OTT Dashboard</title>
    <style>
        body {
            background-color: #141414;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
            padding-top: 100px;
        }

        a {
            color: #e50914;
            text-decoration: none;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <h1>Welcome to OTT Platform</h1>
    <h2>Hello, {{ username }} 👋</h2>
    <p>You are successfully logged in.</p>
    <a href="{{ url_for('logout') }}">Logout</a>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password'

    return render_template_string(login_page, error=error)


@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template_string(home_page, username=session['username'])


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
