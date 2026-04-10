# 📝 Flask Todo App

A simple and functional **Todo Web Application** built using **Flask + MySQL**.
This project demonstrates full **CRUD operations** along with task completion tracking.

---

## 🚀 Features

* ➕ Add new tasks
* 📋 View all tasks
* ✏️ Edit/update tasks
* 🗑️ Delete tasks
* ✅ Mark tasks as completed
* 🔄 Toggle task status (complete / incomplete)
* 🕒 Automatic date & time tracking

---

## 🛠️ Tech Stack

* **Backend:** Python (Flask)
* **Database:** MySQL
* **Frontend:** HTML, Bootstrap
* **Connector:** mysql-connector-python

---

## 📂 Project Structure

```
project/
│── app.py
│── templates/
│   ├── index.html
│   ├── edit.html
│   └── about.html
│── static/ (optional)
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone <your-repo-link>
cd <project-folder>
```

### 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```
pip install flask mysql-connector-python
```

### 4. Setup MySQL Database

Open MySQL and run:

```sql
CREATE DATABASE pradipta;
USE pradipta;

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    created_at DATETIME,
    completed BOOLEAN DEFAULT FALSE
);
```

---

### 5. Run the app

```
python app.py
```

Open in browser:

```
http://127.0.0.1:5000/
```

---

## 🧠 How It Works

* Flask handles routing and backend logic
* MySQL stores tasks permanently
* Jinja2 templates render dynamic content
* Checkbox updates task status in real-time
* CRUD operations handled via routes

---

## 🔥 Key Learning Outcomes

* Understanding Flask routing
* Connecting Python with MySQL
* Implementing CRUD operations
* Handling forms and user input
* Dynamic rendering using Jinja2

---

## 📌 Future Improvements

* 🔍 Search functionality
* 📊 Progress bar
* 🌙 Dark mode
* 🔐 User authentication (login system)
* 📱 Responsive UI improvements

---

## 👨‍💻 Author

**Pradipta Haldar**

---

## 💡 Note

This project is built for learning and practice purposes, and can be extended into a full production-ready app.

---

⭐ If you like this project, consider giving it a star!
