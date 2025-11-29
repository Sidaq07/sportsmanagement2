from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os
from datetime import datetime, date, time, timedelta

app = Flask(__name__)
import os
app.secret_key = os.environ.get("SECRET_KEY", "fallback-secret")

DB_PATH = os.path.join(os.path.dirname(__file__), "sports.db")

OPEN_TIME = time(6, 0)
CLOSE_TIME = time(20, 0)
SLOT_MINUTES = 60


# ---------------- DATABASE HELPERS ----------------
def get_db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def init_db_if_needed():
    if not os.path.exists(DB_PATH):
        with get_db() as con, open("schema.sql", "r", encoding="utf-8") as f:
            con.executescript(f.read())


@app.before_request
def setup():
    init_db_if_needed()


# ---------------- AUTH GUARDS ----------------
def require_login():
    return "user_id" in session


# ---------------- ROUTES ----------------
@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("home"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"].strip()

        with get_db() as con:
            row = con.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
            if not row or not check_password_hash(row["password_hash"], password):
                return render_template("login.html", error="Invalid credentials. Please try again.")
            session["user_id"] = row["id"]

        return redirect(url_for("home"))

    return render_template("login.html")


@app.route("/register", methods=["POST"])
def register():
    name = request.form["name"].strip()
    email = request.form["email"].strip().lower()
    password = request.form["password"].strip()

    hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')  

    with get_db() as con:
        try:
            con.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, hashed_pw)
            )
        except sqlite3.IntegrityError:
            return render_template("login.html", error="Email already registered. Please log in.")

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- MAIN PAGES ----------------
@app.route("/home")
def home():
    if not require_login(): return redirect("/login")
    return render_template("home.html")


@app.route("/about")
def about():
    if not require_login(): return redirect("/login")
    return render_template("about.html")


@app.route("/help")
def help_page():
    if not require_login(): return redirect("/login")
    return render_template("help.html")


@app.route("/facilities")
def facilities_page():
    if not require_login(): return redirect("/login")
    with get_db() as con:
        facilities = con.execute("SELECT * FROM facilities").fetchall()
    return render_template("facilities.html", facilities=facilities)


@app.route("/booking")
def booking():
    if not require_login(): return redirect("/login")
    with get_db() as con:
        facilities = con.execute("SELECT * FROM facilities").fetchall()
    return render_template("booking.html", facilities=facilities)


# ---------------- BOOKING API ----------------
@app.route("/api/book", methods=["POST"])
def api_book():
    if "user_id" not in session:
        return jsonify({"error": "Login required"}), 401

    data = request.json
    fid = data["facility_id"]
    day = data["date"]
    start = data["start_time"]
    equip = data.get("need_equipment", False)

    with get_db() as con:
        con.execute("""
            INSERT INTO bookings (user_id, facility_id, date, start_time, need_equipment, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (session["user_id"], fid, day, start, int(equip), datetime.now().isoformat()))

    return jsonify({"message": "Booking confirmed!"})

@app.route("/api/my-bookings")
def my_bookings():
    if "user_id" not in session:
        return jsonify({"error": "Login required"}), 401
    with get_db() as con:
        rows = con.execute("""
            SELECT b.date, b.start_time, b.need_equipment, f.name AS facility
            FROM bookings b
            JOIN facilities f ON f.id = b.facility_id
            WHERE b.user_id = ?
            ORDER BY b.date DESC, b.start_time
        """, (session["user_id"],)).fetchall()
    bookings = [dict(r) for r in rows]
    return jsonify({"bookings": bookings})



if __name__ == "__main__":
    app.run(debug=True)
