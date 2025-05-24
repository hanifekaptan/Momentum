import sqlite3
import os
import random

DATABASE_NAME = "momentum_database.db"
DB_PATH = os.path.join("src", "data", DATABASE_NAME)

class PomodoroManager:

    def __init__(self):
        self.db_path = DB_PATH
        self._create_table_if_not_exists()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def _create_table_if_not_exists(self):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                        CREATE TABLE IF NOT EXISTS pomodoro_log (
                        pomodoro_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        duration INTEGER NOT NULL,
                        pomodoro_type TEXT NOT NULL
                    );
                """)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Veritabanı tablosu oluşturulurken hata oluştu: {e}")

    def create_fake_data(self):
        for i in range(50):
            for j in ["study", "break"]:
                if j == "break":
                    duration = random.randint(1, 20)
                else:
                    duration = random.randint(20, 60)
                self.insert_pomodoro_log(duration, j)


    def insert_pomodoro_log(self, duration, pomodoro_type):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO pomodoro_log (duration, pomodoro_type)
                    VALUES (?, ?)
                """, (duration, pomodoro_type))
                conn.commit()
                pomodoro_id = cursor.lastrowid
                return pomodoro_id
        except sqlite3.Error as e:
            print(f"Görev eklenirken hata oluştu: {e}")
            return None
        
    def get_pomodoro_summary_data(self):
        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                sql = """
                SELECT pomodoro_type, COUNT(*) AS count, AVG(duration) AS average, SUM(duration) AS total
                FROM pomodoro_log
                GROUP BY pomodoro_type
                """
                cursor.execute(sql)
                pomodoro_data = cursor.fetchall()
                return [dict(row) for row in pomodoro_data]
        except sqlite3.Error as e:
            print(f"Session getirilirken hata oluştu: {e}")
            return None