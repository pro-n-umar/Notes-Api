from typing import Dict
from models import User, Note
import redis

# Redis client setup
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# In-memory databases for users and notes
users_db: Dict[str, User] = {}
notes_db: Dict[str, Note] = {}

# MySQL connection setup for audit logging
try:
    import mysql.connector
    mysql_conn = mysql.connector.connect(
        host='localhost',
        user='notes_app',
        password='yourpassword',
        database='notes_audit'
    )
    cursor = mysql_conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255),
            action VARCHAR(20),
            note_id VARCHAR(255),
            action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    mysql_conn.commit()
except:
    mysql_conn = None
    print("Audit logging disabled (MySQL not available)")