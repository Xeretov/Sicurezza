import sqlite3
import os

from flask import Flask, request, g, redirect, url_for, render_template, session, flash


DATABASE = 'users.db'
SECRET_KEY = 'AAA'  # Replace with your own secret key.

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

def get_db():
    """
    Open a new database connection if there is none yet for the current application context.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        # Return rows as dictionaries
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    """
    Closes the database connection at the end of the request.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """Create user table if it doesn't exist."""
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # create items table if not exists
    db.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    ''')

    db.commit()


@app.before_request
def initialize():
    """Initialize the database before the first request."""
    init_db()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()

        # Check if user already exists
        existing_user = db.execute(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        ).fetchone()

        if existing_user:
            flash("Username already taken, please choose another.", "error")
            return redirect(url_for('register'))

        # Hash and store the new user’s password
        db.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)',
            (username, password)
        )
        db.commit()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))

    # GET request -> Show registration form
    return render_template('register.html')

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if 'user_id' not in session:
        flash("You must be logged in to add items.", "warning")
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        db = get_db()
        db.execute("INSERT INTO items (name, description) VALUES (?, ?)", (name, description))
        db.commit()
        flash("Item added!", "success")
        return redirect(url_for('show_items'))

    return render_template('base.html', content="""
    <form method="POST">
        <label for="name">Item Name:</label>
        <input type="text" name="name" required><br><br>
        <label for="description">Description:</label>
        <textarea name="description"></textarea><br><br>
        <button type="submit">Add Item</button>
    </form>
    """)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()

        sql = 'SELECT * FROM users WHERE username = "' + username + '" and password="' + password + '"'
    
        print(request.form)
        print(sql)
        user = db.execute(sql).fetchone()

        # Validate user credentials
        if user: # and user['password']==password:
            # Store user info in session
            session['user_id'] = user['id']
            session['username'] = user['username']
            
            flash("Login successful!", "success")
            return redirect(url_for('protected_page'))

        flash("Invalid credentials. Please try again.", "error")
        return redirect(url_for('login'))

    # GET request -> Show login form
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))


# @app.route('/protected')
# def protected():
#     if 'user_id' not in session:
#         flash("You must be logged in to view this page.", "warning")
#         return redirect(url_for('login'))

#     # If logged in, render a protected page:
#     # This page could be an HTML template or a redirect to a static file
#     return render_template('base.html', content="This is a protected route!")

@app.route('/protected')
def protected_page():
    if 'user_id' not in session:
        flash("You must be logged in to access this page.", "warning")
        return redirect(url_for('login'))

    return render_template('protected_page.html')

@app.route('/protected_static')
def protected_static():
    if 'user_id' not in session:
        flash("You must be logged in to view this page.", "warning")
        return redirect(url_for('login'))
    
    # Return the static content from a file (or a template) only if logged in
    return app.send_static_file('protected_page.html')

@app.route('/public')
def public_page():
    return render_template('free_public_page.html')

@app.route('/')
def index():
    return render_template('index.html')


# La gestione dei dati applicativi
@app.route('/items')
def show_items():
    if 'user_id' not in session:
        flash("You must be logged in to view items.", "warning")
        return redirect(url_for('login'))

    db = get_db()
    items = db.execute("SELECT * FROM items").fetchall()

    return render_template('dynamic.html', items=items)


myip = "10.8.0.26"
myport = 8888

if __name__ == '__main__':
    with app.app_context():
        init_db()  # Ensure the database is initialized
    app.run(host=myip, port=myport, debug=False)
