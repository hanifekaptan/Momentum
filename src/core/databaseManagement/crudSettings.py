import sqlite3
import os

DATABASE_NAME = "momentum_database.db"
DB_PATH = os.path.join("src", "data", DATABASE_NAME)

class SettingsManager:
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
                        CREATE TABLE IF NOT EXISTS settings (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        birth_date TEXT NOT NULL,
                        gender TEXT
                    );
                """)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Veritabanı tablosu oluşturulurken hata oluştu: {e}")

    def create_fake_data(self):
        self.insert_user_data("username", "usermail@example.com", "2000.01.01", "female")

    def insert_user_data(self, user_name, email, birth_date, gender = None):
        if gender is None:
            gender = ""
        if not user_name or not email or not birth_date:
            print("Hata: User name, email ve birth date boş olamaz.")
            return None
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO settings (user_name, email, birth_date, gender) VALUES (?, ?, ?, ?)
                """, (user_name, email, birth_date, gender))
                conn.commit()
                user_id = cursor.lastrowid
                return user_id
        except sqlite3.Error as e:
            print(f"Görev eklenirken hata oluştu: {e}")
            return None

    def update_user_data(self, user_name, email, birth_date, gender = None):
        if gender is None:
            gender = ""
        if not user_name or not email or not birth_date:
            print("Hata: User name, email ve birth date boş olamaz.")
            return None
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE settings SET user_name = ?, email = ?, birth_date = ?, gender = ?
                """, (user_name, email, birth_date, gender))
                conn.commit()
                user_id = cursor.lastrowid
                return user_id
        except sqlite3.Error as e:
            print(f"Görev eklenirken hata oluştu: {e}")
            return None
        
    def get_user_data(self):
        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                sql = """
                SELECT * FROM settings
                """
                cursor.execute(sql)
                pomodoro_data = cursor.fetchone()
                if pomodoro_data:
                    return dict(pomodoro_data)
        except sqlite3.Error as e:
            print(f"Session getirilirken hata oluştu: {e}")
            return None
