from flask import Flask, request, redirect, render_template_string
import sqlite3
import random
import string

app = Flask(__name__)

# ---------------- DATABASE SETUP ----------------

conn = sqlite3.connect("urls.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS url_map (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    long_url TEXT NOT NULL,
    short_code TEXT UNIQUE NOT NULL
)
""")

conn.commit()

# ---------------- SHORT CODE GENERATOR ----------------

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# ---------------- SHORTEN URL FUNCTION ----------------

def shorten_url(long_url):

    while True:
        short_code = generate_short_code()

        cursor.execute(
            "SELECT * FROM url_map WHERE short_code=?",
            (short_code,)
        )

        if not cursor.fetchone():
            break

    cursor.execute(
        "INSERT INTO url_map (long_url, short_code) VALUES (?, ?)",
        (long_url, short_code)
    )

    conn.commit()

    return short_code

# ---------------- GET ORIGINAL URL ----------------

def get_original_url(short_code):

    cursor.execute(
        "SELECT long_url FROM url_map WHERE short_code=?",
        (short_code,)
    )

    result = cursor.fetchone()

    return result[0] if result else None

# ---------------- HOME PAGE ----------------

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        long_url = request.form["url"]

        short_code = shorten_url(long_url)

        short_url = f"http://127.0.0.1:5000/{short_code}"

        return render_template_string("""
        <h2>URL Shortener</h2>

        <p><b>Short URL:</b></p>

        <p>
        <a href="{{short_url}}" target="_blank">
        {{short_url}}
        </a>
        </p>

        <br>

        <a href="/">Shorten Another URL</a>
        """, short_url=short_url)

    return render_template_string("""

    <h2>URL Shortener</h2>

    <form method="post">

        <input type="text"
        name="url"
        placeholder="Enter long URL"
        style="width:300px"
        required>

        <br><br>

        <button type="submit">
        Shorten URL
        </button>

    </form>

    """)

# ---------------- REDIRECTION ----------------

@app.route("/<short_code>")
def redirect_url(short_code):

    original_url = get_original_url(short_code)

    if original_url:
        return redirect(original_url)

    return "<h3>Invalid Short URL</h3>"

# ---------------- RUN SERVER ----------------

if __name__ == "__main__":
    app.run(debug=True)