import sqlite3

class DatabaseManager:
    """Gestiona la persistencia de respuestas y progreso del usuario."""
    
    def __init__(self, db_name="isla_digital.db"):
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(base_dir, db_name)
        
        self._init_db()

    def _init_db(self):
        conn = self._get_conn()
        with conn:
            cursor = conn.cursor()
            
            # Tabla de respuestas a desafíos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS challenge_responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    protocol TEXT,
                    unit_id TEXT,
                    response TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de progreso (unidades completadas)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_progress (
                    protocol TEXT,
                    unit_id TEXT,
                    status TEXT,
                    PRIMARY KEY (protocol, unit_id)
                )
            ''')
            
            # Commit is handled by the context manager
            conn.commit()

    def _get_conn(self):
        """Retorna una conexión a la DB."""
        return sqlite3.connect(self.db_path)

    def save_response(self, protocol, unit_id, response):
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO challenge_responses (protocol, unit_id, response)
                    VALUES (?, ?, ?)
                ''', (protocol, unit_id, response))
                conn.commit()
        except Exception as e:
            print(f"Error de DB: {e}")

    def get_responses(self, unit_id=None):
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                if unit_id:
                    cursor.execute('SELECT protocol, response, timestamp FROM challenge_responses WHERE unit_id = ?', (unit_id,))
                else:
                    cursor.execute('SELECT unit_id, response, timestamp FROM challenge_responses')
                return cursor.fetchall()
        except Exception:
            return []

    def update_progress(self, protocol, unit_id, status="COMPLETED"):
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO user_progress (protocol, unit_id, status)
                    VALUES (?, ?, ?)
                ''', (protocol, unit_id, status))
                conn.commit()
        except Exception:
            pass

    def get_progress(self, protocol):
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT unit_id FROM user_progress WHERE protocol = ? AND status = "COMPLETED"', (protocol,))
                return [row[0] for row in cursor.fetchall()]
        except Exception:
            return []

# Singleton instance
db = DatabaseManager()
