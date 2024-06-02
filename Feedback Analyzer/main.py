from flask import Flask, render_template, request, redirect, url_for, jsonify, session, json
from flask import session
from model import comment_analysis
from scrapper import get_reviews, get_name
from yt_search import search_videos, get_data
import sqlite3
import smtplib
import random


app = Flask(__name__)
app.secret_key = 'PROJECTMAIL'
def generate_random_code():
    return str(random.randint(30000, 90000))

def create_history_table():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS history (
    UserID INTEGER,
    YTBiD TEXT,
    POSITIVE INTEGER,
    NEGATIVE INTEGER,
    NEUTRAL INTEGER,
    UNKOWN INTEGER,
    FOREIGN KEY(UserID) REFERENCES user(id)
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    connection.close()

# Call the function when the application starts
create_history_table()

# The rest of your code goes here



@app.route('/')
def index():
    return render_template('index.html')
@app.route('/loggedin')
def loggedin():
    return render_template('loggedin.html')
@app.route('/home')
def home():
    return render_template('confirmeacc.html')

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()

        mail = request.form['emaill']
        password = request.form['passwordl']

        query = "SELECT email,password FROM user WHERE email=? AND password=?" 
        cursor.execute(query, (mail, password))
        results = cursor.fetchall()

        if len(results) == 0:
            # return a message to the user
            error="Incorrect login information"
        else:
            session['user_id'] = results[0][0]
            return render_template("loggedin.html")

    return render_template("login.html", error=error)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['email']
        password = request.form['password']
        random_code = generate_random_code()
        session['random_code'] = random_code

        session['name'] = name
        session['mail'] = mail
        session['password'] = password
    
        msg = random_code
        email = "projectmail695@gmail.com"
 


        subject = "confirmation code "

  
        text = f"{subject}\n {msg}"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email , "zmxrlotzngrawlfx")
        server.sendmail(email,mail, text)
        print("code send")
 

        return redirect(url_for('confirmeacc'))
    
    return render_template("confirmeacc.html")

@app.route('/confirmeacc', methods=['GET','POST'])
def confirmeacc():
    if request.method == 'POST':
        code = request.form['code']
        if code == session.get('random_code'):
            name = session.get('name')
            mail = session.get('mail')
            password = session.get('password')
            connection = sqlite3.connect('users.db')
            cursor = connection.cursor()
            query = "INSERT INTO user (name,email, password) VALUES (?, ?, ?)"
            cursor.execute(query, (name, mail , password))
            user_id = cursor.lastrowid  # Get the ID of the newly inserted user
            session['user_id'] = user_id  # Store the user ID in the session

            # No need to create a new table for each user
            # Instead, add a new column for the user ID in the history table
            create_table_query = """
            CREATE TABLE IF NOT EXISTS history (
            UserID INTEGER,
            YTBiD TEXT,
            POSITIVE INTEGER,
            NEGATIVE INTEGER,
            NEUTRAL INTEGER,
            UNKOWN INTEGER,
            FOREIGN KEY(UserID) REFERENCES user(id)
            );
            """
            cursor.execute(create_table_query)
            connection.commit()
            connection.close()

            session.pop('random_code', None)
            session.pop('names', None)
            session.pop('emails', None)
            session.pop('passwords', None)
            
            return redirect(url_for('loggedin'))
        else:
            error = "Invalid code, please try again."
            return render_template("confirmeacc.html", error=error)

    return render_template("confirmeacc.html")

@app.route('/submit_form', methods=['POST'])
def submit_form():
    
    url = request.form.get('url')
    id = request.form.get('id')

    result = comment_analysis(url, id)
    print(type(result))

    if 'user_id' in session:
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        query = "INSERT INTO history (UserID, YTBiD, POSITIVE, NEGATIVE, NEUTRAL, UNKOWN) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(query, (session['user_id'], id, result[0], result[1], result[2], result[3]))
        connection.commit()
        connection.close()
    
    return jsonify(result)

    

@app.route('/submit_amz_form', methods=['POST'])
def submit_amz_form():
    
    url = request.form.get('url')
    lang = request.form.get('lang')
    response = get_reviews(url, lang)
    positives, negatives = response
    videos = search_videos(get_name(url), 3, lang)
    return jsonify({'positives': positives, 'negatives': negatives, 'videos': videos})
    


@app.route('/history', methods=['GET'])
def history():
    if 'user_id' in session:
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        query = "SELECT * FROM history WHERE UserID = ?"
        cursor.execute(query, (session['user_id'],))
        results = cursor.fetchall()
        connection.close()

        # Convert the results to a list of dictionaries for easier JSON serialization
        history = [{'YTBiD': row[1], 'POSITIVE': row[2], 'NEGATIVE': row[3], 'NEUTRAL': row[4], 'UNKOWN': row[5]} for row in results]

        history_list = []  # Create an empty list to store the video details

        for video in history:
            video_details = get_data(video['YTBiD'])
            if video_details is not None:
                video_list = video_details
                video_list.append(video['POSITIVE'])
                video_list.append(video['NEGATIVE'])
                video_list.append(video['NEUTRAL'])
                video_list.append(video['UNKOWN'])
                history_list.append(video_list)  # Append the video details to the history list

        return render_template('history.html', history=json.dumps(history_list))
    else:
        return jsonify({'error': 'Not logged in'}), 401
    
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)