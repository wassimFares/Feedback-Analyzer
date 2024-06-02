from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import smtplib
import random

app = Flask(__name__)
app.secret_key = 'PROJECTMAIL'

def generate_random_code():
    return str(random.randint(30000, 90000))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()

        mail = request.form['mail']
        password = request.form['password']

        query = "SELECT name,password FROM users WHERE name=? AND password=?" 
        cursor.execute(query, (mail, password))
        results = cursor.fetchall()

        if len(results) == 0:
            print("incorrect infos")
        else:
            return render_template("home.html")

    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']
        age = request.form['age']
        random_code = generate_random_code()
        session['random_code'] = random_code

        session['name'] = mail
        session['password'] = password
        session['age'] = age
        msg = random_code
        email = "projectmail695@gmail.com"
 


        subject = "confirmation code "

  
        text = f"{subject}\n {msg}"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email , "zmxrlotzngrawlfx")
        server.sendmail(email,mail, text)
        print("code send")
 

        return redirect(url_for('regcode'))
    
    return render_template("register.html")

@app.route('/regcode', methods=['GET','POST'])
def regcode():
    if request.method == 'POST':
        code = request.form['code']
        if code == session.get('random_code'):
            name = session.get('name')
            password = session.get('password')
            age = session.get('age')
            connection = sqlite3.connect('users.db')
            cursor = connection.cursor()

            query = "INSERT INTO users (name, password, age) VALUES (?, ?, ?)"
            cursor.execute(query, (name, password, age))
            connection.commit()
            connection.close()

            session.pop('random_code', None)
            session.pop('name', None)
            session.pop('password', None)
            session.pop('age', None)
            
            return redirect(url_for('login'))
        else:
            error = "Invalid code, please try again."
            return render_template("regcode.html", error=error)

    return render_template("regcode.html")

if __name__ == "__main__":
    app.run(debug=True)
