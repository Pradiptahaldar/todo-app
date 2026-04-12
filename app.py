import os

from Flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from datetime import datetime


app = Flask(__name__)
app.secret_key = "your_secret_key"

# connect to mysql
conn = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE"),
    port=int(os.getenv("MYSQL_PORT"))
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
            print("Inserted successfully")

            return redirect(url_for("index"))   # ✅ FIX

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
            session["user_id"]= user[0]
            return redirect(url_for("index"))
        else:
            error="Invalid email or password"
    return render_template("login.html", error=error)

    

@app.route("/home")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user_id = session.get("user_id")
    cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
    
    tasks = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) as total FROM tasks WHERE user_id = %s", (user_id,))
    total_tasks = cursor.fetchone()["total"]
    cursor.execute("SELECT COUNT(*) as completed FROM tasks WHERE user_id = %s AND completed = 1", (user_id,))
    completed_tasks = cursor.fetchone()["completed"]
    pending_tasks = total_tasks - completed_tasks
    return render_template("index.html", tasks=tasks, total_tasks=total_tasks, completed_tasks=completed_tasks, pending_tasks=pending_tasks)

@app.route("/add", methods=["POST"])
def add():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user_id = session.get("user_id")
    title = request.form.get("title")
    description = request.form.get("description")

    if not title:
        return redirect(url_for("index"))

    created_at = datetime.now()

    cursor.execute(
        "INSERT INTO tasks (user_id, title, description, created_at) VALUES (%s, %s, %s, %s)",
        (user_id, title, description, created_at)
    )
    conn.commit()

    return redirect(url_for("index"))

@app.route("/about")
def about():
    next_page = request.args.get("next")
    return render_template("about.html", next_page=next_page)

@app.route("/all")
def all_tasks():
    cursor.execute("SELECT * FROM tasks")
    return render_template("index.html", tasks=cursor.fetchall())

@app.route("/today")
def today_tasks():
    cursor.execute("SELECT * FROM tasks WHERE DATE(created_at) = CURDATE()")
    return render_template("index.html", tasks=cursor.fetchall())

@app.route("/recent")
def recent_tasks():
    cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC LIMIT 5")
    return render_template("index.html", tasks=cursor.fetchall())

@app.route("/delete/<int:id>")
def delete(id):
    cursor.execute("DELETE FROM tasks WHERE id=%s", (id,))
    conn.commit()
    return redirect(url_for("index"))

@app.route("/edit/<int:id>")
def edit(id):
    cursor.execute("SELECT * FROM tasks WHERE id=%s", (id,))
    task = cursor.fetchone()
    return render_template("edit.html", task=task)

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    title = request.form.get("title")
    description = request.form.get("description")

    cursor.execute(
        "UPDATE tasks SET title=%s, description=%s WHERE id=%s",
        (title, description, id)
    )
    conn.commit()

    return redirect(url_for("index"))

@app.route("/toggle/<int:id>")
def toggle(id):
    print("TOGGLE HIT:", id)   #debugging statement

    cursor.execute(
        "UPDATE tasks SET completed = NOT completed WHERE id=%s",
        (id,)
    )
    conn.commit()

    return redirect(url_for("index"))

#search route
@app.route("/search")
def search():
    query = request.args.get("query", "")
    cursor.execute(
        "SELECT * FROM tasks WHERE title LIKE %s OR description LIKE %s",
        (f"%{query}%", f"%{query}%")
    )
    return render_template("index.html", tasks=cursor.fetchall())
if __name__ == "__main__":
    app.run (host="0.0.0.0", port=5000)
