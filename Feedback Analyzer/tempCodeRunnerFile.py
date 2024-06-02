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

        return render_template('history.html', history=jsonify(history))
    else:
        return jsonify({'error': 'Not logged in'}), 401