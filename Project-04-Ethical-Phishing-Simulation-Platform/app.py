import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images')

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS campaigns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    template TEXT NOT NULL,
                    recipients TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    sent_at TEXT
                )''')
    conn.commit()
    cur.execute('SELECT * FROM users WHERE username = ?', ('Admin',))
    if not cur.fetchone():
        cur.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                    ('Admin', generate_password_hash('Admin123')))
    conn.commit()
    conn.close()

@app.before_request
def before_request_func():
    if not hasattr(app, 'db_initialized'):
        init_db()
        app.db_initialized = True

@app.route('/static/images/<filename>')
def custom_static(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET'])
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    campaigns_db = conn.execute('SELECT * FROM campaigns ORDER BY id DESC').fetchall()
    conn.close()
    campaigns = []
    for c in campaigns_db:
        # status and sent_at logic
        is_sent = bool(c['sent_at'])
        campaigns.append({
            'id': c['id'],
            'name': c['name'],
            'created_at': c['created_at'],
            'status': 'Sent' if is_sent else 'Not sent',
            'sent_at': c['sent_at'] if is_sent else '',
            'actions': True,  # Always show "View"
            'can_send': not is_sent  # Only show "Send" if not sent
        })
    return render_template('dashboard.html', campaigns=campaigns)

@app.route('/campaign/new', methods=['GET', 'POST'])
def campaign_new():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    error = None
    template_files = [f for f in os.listdir('phishing_templates') if f.endswith('.html')]
    if request.method == 'POST':
        name = request.form['name']
        template = request.form['template']
        recipients = request.form['recipients']
        if not name or not template or not recipients:
            error = "All fields are required!"
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO campaigns (name, template, recipients, created_at) VALUES (?, ?, ?, ?)',
                         (name, template, recipients, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            conn.close()
            flash('Campaign created successfully!', 'success')
            return redirect(url_for('dashboard'))
    return render_template('campaign_new.html', template_files=template_files, error=error)

@app.route('/campaign/<int:campaign_id>')
def campaign_view(campaign_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    campaign = conn.execute('SELECT * FROM campaigns WHERE id = ?', (campaign_id,)).fetchone()
    conn.close()
    if not campaign:
        return render_template('error.html', error="Campaign not found."), 404
    return render_template('campaign_view.html', campaign=campaign)

@app.route('/campaign/send/<int:campaign_id>', methods=['POST'])
def campaign_send(campaign_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    sent_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db_connection()
    conn.execute('UPDATE campaigns SET sent_at = ? WHERE id = ? AND sent_at IS NULL', (sent_at, campaign_id))
    conn.commit()
    conn.close()
    flash('Campaign sent successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/analytics')
def analytics():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    campaigns = conn.execute('SELECT * FROM campaigns').fetchall()
    conn.close()
    return render_template('analytics.html', campaigns=campaigns)

@app.route('/educate')
def educate():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('educate.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error="Page not found."), 404

if __name__ == '__main__':
    app.run(debug=True)