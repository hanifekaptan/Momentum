from datetime import datetime, timedelta
import sqlite3
import os
import random
import faker

DATABASE_NAME = "momentum_database.db"
DB_PATH = os.path.join("src", "data", DATABASE_NAME)

class TaskManager:
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
                        CREATE TABLE IF NOT EXISTS tasks (
                        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        is_completed INTEGER DEFAULT 0,
                        start_date TEXT,
                        end_date TEXT,
                        priority INTEGER,
                        tag TEXT
                    );
                """)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Veritabanı tablosu oluşturulurken hata oluştu: {e}")

    def create_fake_data(self):
        fake = faker.Faker()
        for _ in range(50):
            title = fake.sentence(nb_words=6).replace(".", "")
            is_completed = random.choice([0, 1])
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            start_date_obj = fake.date_between(start_date=start_date, end_date=end_date)
            end_date_obj = None
            if random.random() > 0.3:
                end_date_obj = start_date_obj + timedelta(days=random.randint(1, 365))
            start_date_str = start_date_obj.strftime("%Y-%m-%d") if start_date_obj else None
            end_date_str = end_date_obj.strftime("%Y-%m-%d") if end_date_obj else None
            priority = random.randint(1, 10) if random.random() > 0.2 else None
            tag = random.choice([fake.word(), fake.word(), fake.word(), None, None])
            self.insert_task(title, is_completed, start_date_str, end_date_str, priority, tag)

    def insert_task(self, title, is_completed=0, start_date=None, end_date=None, priority=None, tag=None):
        if not title:
            print("Hata: Başlık (title) boş olamaz.")
            return None
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO tasks (title, is_completed, start_date, end_date, priority, tag)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (title, is_completed, start_date, end_date, priority, tag))
                conn.commit()
                task_id = cursor.lastrowid
                return task_id
        except sqlite3.Error as e:
            print(f"Görev eklenirken hata oluştu: {e}")
            return None

    def get_task(self, task_id):
        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,))
                task = cursor.fetchone()
                if task:
                    return dict(task)
                return None
        except sqlite3.Error as e:
            print(f"Görev getirilirken hata oluştu: {e}")
            return None
    
    def get_task_in_one_day(self, date):
        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM tasks WHERE start_date = ?", (date, ))
                tasks = cursor.fetchall()
                return [dict(task) for task in tasks]
        except sqlite3.Error as e:
            print(f"Görev getirilirken hata oluştu: {e}")
            return []
    
    def get_all_task_completion(self, is_completed: bool = False):
        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM tasks WHERE is_completed = ?", (is_completed,))
                tasks = cursor.fetchall()
                return [dict(row) for row in tasks]
        except sqlite3.Error as e:
            print(f"Tüm görevler getirilirken hata oluştu: {e}")
            return []

    def get_all_tasks(self):
        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM tasks ORDER BY task_id DESC")
                tasks = cursor.fetchall()
                return [dict(row) for row in tasks]
        except sqlite3.Error as e:
            print(f"Tüm görevler getirilirken hata oluştu: {e}")
            return []
        
    def get_task_summary_data(self):
        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT is_completed, COUNT(*) AS count FROM tasks GROUP BY is_completed")
                tasks = cursor.fetchall()
                return [dict(row) for row in tasks]
        except sqlite3.Error as e:
            print(f"Tüm görevler getirilirken hata oluştu: {e}")
            return []
        
    def get_all_tasks_sorted_custom(self, sorting_criteria=None):
        allowed_columns = ["task_id", "title", "is_completed", "start_date", "end_date", "priority", "tag"]
        order_parts = []
        if not sorting_criteria:
             order_parts.append("task_id DESC")
        else:
            for criterion in sorting_criteria:
                if not isinstance(criterion, tuple) or len(criterion) != 2:
                    print(f"Hata: Geçersiz sıralama kriteri formatı: {criterion}. (sütun_adı, yön) şeklinde tuple bekleniyor.")
                    return []
                column, direction = criterion
                if column not in allowed_columns:
                    print(f"Hata: Geçersiz sıralama sütunu: {column}. İzin verilen sütunlar: {", ".join(allowed_columns)}")
                    return []
                direction = direction.upper() if isinstance(direction, str) else "ASC"
                if direction not in ["ASC", "DESC"]:
                    print(f"Hata: Geçersiz sıralama yönü: {direction} for column {column}. 'ASC' veya 'DESC' bekleniyor.")
                    return []
                order_parts.append(f"{column} {direction}")

        order_by_clause = ", ".join(order_parts)

        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM tasks ORDER BY {order_by_clause}")
                tasks = cursor.fetchall()
                return [dict(row) for row in tasks]
        except sqlite3.Error as e:
            print(f"Görevler sıralanırken hata oluştu: {e}")
            return []

    def update_task(self, task_id, title=None, is_completed=None, start_date=None, end_date=None, priority=None, tag=None):
        fields = []
        values = []
        if title is not None:
            fields.append("title = ?")
            values.append(title)
        if is_completed is not None:
            fields.append("is_completed = ?")
            values.append(is_completed)
        if start_date is not None:
            fields.append("start_date = ?")
            values.append(start_date)
        if end_date is not None:
            fields.append("end_date = ?")
            values.append(end_date)
        if priority is not None:
            fields.append("priority = ?")
            values.append(priority)
        if tag is not None:
            fields.append("tag = ?")
            values.append(tag)
        if not fields:
            print("Güncellenecek alan belirtilmedi.")
            return False
        sql = f"UPDATE tasks SET {", ".join(fields)} WHERE task_id = ?"
        values.append(task_id)

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, tuple(values))
                conn.commit()
                if cursor.rowcount > 0:
                    print(f"Görev ID {task_id} başarıyla güncellendi.")
                    return True
                else:
                    print(f"Görev ID {task_id} bulunamadı.")
                    return False
        except sqlite3.Error as e:
            print(f"Görev güncellenirken hata oluştu: {e}")
            return False

    def delete_task(self, task_id):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
                conn.commit()
                if cursor.rowcount > 0:
                    print(f"Görev ID {task_id} başarıyla silindi.")
                    return True
                else:
                    print(f"Görev ID {task_id} bulunamadı.")
                    return False
        except sqlite3.Error as e:
            print(f"Görev silinirken hata oluştu: {e}")
            return False
