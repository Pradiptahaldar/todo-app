from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# connect to mysql
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="pradipta"
)
cursor = conn.cursor(dictionary=True)

@app.route("/")
def index():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    description = request.form.get("description")

    if not title:
        return redirect(url_for("index"))

    created_at = datetime.now()

    cursor.execute(
        "INSERT INTO tasks (title, description, created_at) VALUES (%s, %s, %s)",
        (title, description, created_at)
    )
    conn.commit()

    return redirect(url_for("index"))

@app.route("/about")
def about():
    return render_template("about.html")

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
    print("TOGGLE HIT:", id)   # 👈 DEBUG

    cursor.execute(
        "UPDATE tasks SET completed = NOT completed WHERE id=%s",
        (id,)
    )
    conn.commit()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run (debug=True)