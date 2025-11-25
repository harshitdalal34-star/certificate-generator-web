from flask import Flask, render_template, request, send_file, redirect, url_for, session, flash
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
import json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key in production
OUTPUT_FOLDER = "output"
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users:
            flash('Username already exists')
        else:
            users[username] = generate_password_hash(password)
            save_users(users)
            flash('Account created successfully. Please log in.')
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_certificate():
    if 'username' not in session:
        return redirect(url_for('login'))
    try:
        name = request.form['name']
        date = request.form['date']

        if not name or not date:
            return render_template("index.html", error="All fields are required!")

        # Load image
        template_path = "static/certificate_template.png"  # or .jpeg if you're using JPEG
        img = Image.open(template_path)
        draw = ImageDraw.Draw(img)


        # Load two different font sizes
        font_path = "fonts/ITCEDSCR.TTF"
        font_large = ImageFont.truetype(font_path, size=120)
        font_small = ImageFont.truetype(font_path, size=50)

        # Draw name with large font
        draw.text((725, 635), name, fill="black", font=font_large)
        # Draw date with small font
        draw.text((1250, 1020), date, fill="black", font=font_small)


        # Save image temporarily
        image_path = f"{OUTPUT_FOLDER}/{name}_certificate.png"
        img.save(image_path)

        # Generate PDF with original image dimensions
        pdf_path = f"{OUTPUT_FOLDER}/{name}_certificate.pdf"
        img_width, img_height = img.size
        dpi = 96
        width_pt = img_width * 72 / dpi
        height_pt = img_height * 72 / dpi

        c = canvas.Canvas(pdf_path, pagesize=(width_pt, height_pt))
        c.drawImage(image_path, 0, 0, width=width_pt, height=height_pt)
        c.save()


        return send_file(pdf_path, as_attachment=True)

    except Exception as e:
        return render_template("index.html", error=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

