import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('resume_builder.db')
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL,
                created_at TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT,
                email TEXT,
                phone TEXT,
                address TEXT,
                education TEXT,
                skills TEXT,
                experience TEXT,
                template TEXT,
                saved_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.conn.commit()
    
    def register(self, username, password, email):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, email, created_at) VALUES (?, ?, ?, ?)",
                (username, password, email, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            self.conn.commit()
            return True, "Registration successful!"
        except:
            return False, "Username already exists!"
    
    def login(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, username, email FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        user = cursor.fetchone()
        if user:
            return True, {"id": user[0], "username": user[1], "email": user[2]}
        return False, "Invalid username or password!"
    
    def save_resume(self, user_id, resume_data):
        import json
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO resumes (user_id, name, email, phone, address, education, skills, experience, template, saved_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            resume_data.get('personal', {}).get('name', ''),
            resume_data.get('personal', {}).get('email', ''),
            resume_data.get('personal', {}).get('phone', ''),
            resume_data.get('personal', {}).get('address', ''),
            json.dumps(resume_data.get('education', [])),
            json.dumps(resume_data.get('skills', [])),
            json.dumps(resume_data.get('experience', [])),
            resume_data.get('template', 'modern'),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        self.conn.commit()
        return True
    
    def get_user_resumes(self, user_id):
        import json
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, name, email, phone, address, education, skills, experience, template, saved_date FROM resumes WHERE user_id = ? ORDER BY saved_date DESC",
            (user_id,)
        )
        resumes = cursor.fetchall()
        result = []
        for r in resumes:
            result.append({
                'id': r[0],
                'name': r[1],
                'email': r[2],
                'phone': r[3],
                'address': r[4],
                'education': json.loads(r[5]) if r[5] else [],
                'skills': json.loads(r[6]) if r[6] else [],
                'experience': json.loads(r[7]) if r[7] else [],
                'template': r[8],
                'saved_date': r[9]
            })
        return result
