from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# DB Connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root123',  # Replace with your actual MySQL password
        database='moodscape'
    )

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return redirect(url_for('survey'))  # Redirect to the survey page after successful login
    else:
        return "Invalid username or password. Please try again."

# Survey Page
@app.route('/survey')
def survey():
    return render_template('survey.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/submit-survey', methods=['POST'])
def submit_survey():
    answers = {
        'weather': request.form['weather'],
        'door': request.form['door'],
        'snack': request.form['snack'],
        'soundtrack': request.form['soundtrack'],
        'animal': request.form['animal'],
    }

    mood_map = {
        'sunny': 'joyful',
        'rainy': 'low',
        'windy': 'stressed',
        'calm': 'calm',
        'chilly': 'reflective',
        'carnival': 'joyful',
        'spa': 'calm',
        'mountain': 'stressed',
        'library': 'reflective',
        'arcade': 'joyful',
        'chocolate': 'calm',
        'spicy': 'stressed',
        'popcorn': 'reflective',
        'watermelon': 'calm',
        'cupcake': 'joyful',
        'pop': 'joyful',
        'acoustic': 'reflective',
        'orchestral': 'stressed',
        'lofi': 'calm',
        'rock': 'stressed',
        'puppy': 'joyful',
        'turtle': 'calm',
        'tiger': 'stressed',
        'bird': 'reflective',
        'octopus': 'stressed',
    }

    mood_icons = {
        'joyful': '😄',
        'calm': '😌',
        'low': '😔',
        'stressed': '😤',
        'reflective': '🤔',
    }

    # Count mood occurrences
    mood_count = {'joyful': 0, 'calm': 0, 'low': 0, 'stressed': 0, 'reflective': 0}
    for answer in answers.values():
        mood = mood_map.get(answer, 'reflective')
        mood_count[mood] += 1

    top_mood = max(mood_count, key=mood_count.get)

    # Fetch Movies from DB
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT movie_name, movie_link FROM movies WHERE mood = %s", (top_mood,))
    movies = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(
        'result.html',
        mood_scores=mood_count,
        top_mood=top_mood,
        top_mood_icon=mood_icons[top_mood],
        movies=movies  # Pass movies to the template
    )

@app.route('/watch-movie/<mood>')
def watch_movie(mood):
    mood_icons = {
        'joyful': '😄',
        'calm': '😌',
        'low': '😔',
        'stressed': '😤',
        'reflective': '🤔',
    }

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT movie_name, movie_link FROM movies WHERE mood = %s", (mood,))
    movies = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('movies.html', top_mood=mood, top_mood_icon=mood_icons[mood], movies=movies)

@app.route('/listen-music/<mood>')
def listen_music(mood):
    mood_icons = {
        'joyful': '😄',
        'calm': '😌',
        'low': '😔',
        'stressed': '😤',
        'reflective': '🤔',
    }

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT track_name, track_link FROM music WHERE mood = %s", (mood,))
    tracks = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('music.html', top_mood=mood, top_mood_icon=mood_icons[mood], tracks=tracks)

@app.route('/books/<mood>')
def books(mood):
    mood_icons = {
        'joyful': '😄',
        'calm': '😌',
        'low': '😔',
        'stressed': '😤',
        'reflective': '🤔',
        'happy': '😄',
        'sad': '😔',
        'motivated': '💪',
        'lonely': '😶',
        'relaxed': '😌',
    }

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT title, link FROM books WHERE mood = %s", (mood,))
    books = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('book.html', top_mood=mood, top_mood_icon=mood_icons[mood], books=books)

@app.route('/games/<mood>')
def games(mood):
    mood_icons = {
        'joyful': '😄',
        'calm': '😌',
        'low': '😔',
        'stressed': '😤',
        'reflective': '🤔',
        'motivated': '💪',
    }

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT game_name, game_link FROM games WHERE mood = %s", (mood,))
    games = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(
        'game.html',
        top_mood=mood,
        top_mood_icon=mood_icons.get(mood, '🎮'),  # fallback to 🎮
        games=games
    )

if __name__ == '__main__':
    app.run(debug=True)