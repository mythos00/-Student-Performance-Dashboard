# 🎓 Student Performance Dashboard

A simple Student Performance Dashboard built with **Python, Streamlit, and PostgreSQL**. The application allows users to manage students, search for students by name, calculate grades, and view statistics about student performance.

## 🚀 Features

* Add new students
* View all students
* Search students by name
* Automatically calculate grades
* Display total number of students
* Calculate average, highest, and lowest scores
* Visualize student performance with charts
* Store student data in PostgreSQL

## 🛠️ Technologies Used

* Python
* Streamlit
* PostgreSQL
* Psycopg2
* Pandas

## 📁 Project Structure

```text
student_dashboard/
│
├── main.py
├── database.py
├── services.py
├── config.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd student_dashboard
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## 🗄️ Database Setup

This project uses PostgreSQL.

Create a database named `UniversityDB` in PostgreSQL, then execute the following SQL command:

```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    score INTEGER NOT NULL CHECK (score BETWEEN 0 AND 100)
);
```

## 🔌 Database Connection

Configure your PostgreSQL connection in `config.py`:

```python
DB_CONFIG = {
    "host": "localhost",
    "database": "UniversityDB",
    "user": "postgres",
    "password": "YOUR_POSTGRES_PASSWORD",
    "port": 5432
}
```

Replace `YOUR_POSTGRES_PASSWORD` with your PostgreSQL password.

The `database.py` file uses **Psycopg2** to connect Python to PostgreSQL and execute database queries.

**Important:** Do not upload your real database password or other secret credentials to a public repository.

## 📊 Grade Calculation

Student grades are calculated based on their scores:

| Score  | Grade |
| ------ | ----- |
| 90–100 | A     |
| 80–89  | B     |
| 70–79  | C     |
| 60–69  | D     |
| 0–59   | F     |

## ▶️ Run the Application

Start the Streamlit application with:

```bash
python -m streamlit run main.py
```

The application will open in your browser.

## 📈 Statistics

The dashboard displays:

* Total number of students
* Average score
* Highest score
* Lowest score

## 👨‍💻 Author

Developed as a student project to practice Python, PostgreSQL, database connectivity, and data visualization.
