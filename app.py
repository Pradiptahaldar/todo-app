from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
# connect to mysql
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 3306)),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    ssl_disabled=False
)
cursor = conn.cursor(dictionary=True)

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        age = int(request.form["age"])
        phone = request.form["phone"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            cursor.execute(
                "INSERT INTO users (name, age, phone, email, password) VALUES (%s, %s, %s, %s, %s)",
                (name, age, phone, email, password)
            )

            conn.commit()

            user_id = cursor.lastrowid
            session["user_id"] = user_id

            print("Inserted successfully")

            return redirect(url_for("index"))

        except Exception as e:
            print("Error:", e)

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute(
            "SELECT * FROM users WHERE email = %s AND password = %s",
            (email, password)
        )
        user = cursor.fetchone()

        if user:
            session["user_id"]= user["id"]
            return redirect(url_for("index"))
        else:
            error="Invalid email or password"
    return render_template("login.html", error=error)

    

@app.route("/home")
def index():
    print("SESSION:", session)
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    cursor.execute(
        "SELECT * FROM tasks WHERE user_id = %s",
        (user_id,)
    )

    tasks = cursor.fetchall()
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task["completed"])
    pending_tasks = total_tasks - completed_tasks
    return render_template("index.html", tasks=tasks, total_tasks=total_tasks, completed_tasks=completed_tasks, pending_tasks=pending_tasks)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    description = request.form.get("description")

    if not title:
        return redirect(url_for("index"))

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    created_at = datetime.now()

    cursor.execute(
        """
        INSERT INTO tasks (title, description, created_at, user_id)
        VALUES (%s, %s, %s, %s)
        """,
        (title, description, created_at, user_id)
    )

    conn.commit()
    return redirect(url_for("index"))

@app.route("/about")
def about():
    next_page = request.args.get("next")
    return render_template("about.html", next_page=next_page)

@app.route("/all")
def all_tasks():
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    cursor.execute(
        "SELECT * FROM tasks WHERE user_id = %s",
        (user_id,)
    )

    tasks = cursor.fetchall()

    return render_template("index.html", tasks=tasks)

@app.route("/today")
def today_tasks():
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    cursor.execute(
        """
        SELECT * FROM tasks
        WHERE user_id = %s
        AND DATE(created_at) = CURDATE()
        """,
        (user_id,)
    )

    tasks = cursor.fetchall()

    return render_template("index.html", tasks=tasks)

@app.route("/recent")
def recent_tasks():
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    cursor.execute(
        """
        SELECT * FROM tasks
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 5
        """,
        (user_id,)
    )

    tasks = cursor.fetchall()

    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    cursor.execute(
        "DELETE FROM tasks WHERE id=%s AND user_id=%s",
        (id, user_id)
    )

    conn.commit()

    return redirect(url_for("index"))

@app.route("/edit/<int:id>")
def edit(id):
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    cursor.execute(
        "SELECT * FROM tasks WHERE id=%s AND user_id=%s",
        (id, user_id)
    )

    task = cursor.fetchone()

    if not task:
        return redirect(url_for("index"))

    return render_template("edit.html", task=task)

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    title = request.form.get("title")
    description = request.form.get("description")

    cursor.execute(
        """
        UPDATE tasks
        SET title=%s, description=%s
        WHERE id=%s AND user_id=%s
        """,
        (title, description, id, user_id)
    )

    conn.commit()

    return redirect(url_for("index"))

@app.route("/toggle/<int:id>")
def toggle(id):
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    cursor.execute(
        """
        UPDATE tasks
        SET completed = NOT completed
        WHERE id=%s AND user_id=%s
        """,
        (id, user_id)
    )

    conn.commit()

    return redirect(url_for("index"))

#search route
@app.route("/search")
def search():
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    query = request.args.get("query", "")

    cursor.execute(
        """
        SELECT * FROM tasks
        WHERE user_id = %s
        AND (title LIKE %s OR description LIKE %s)
        """,
        (user_id, f"%{query}%", f"%{query}%")
    )

    tasks = cursor.fetchall()

    return render_template("index.html", tasks=tasks)
if __name__ == "__main__":
    app.run (debug=True, port=9000)