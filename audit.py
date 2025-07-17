from database import mysql_conn

from typing import Optional

def log_action(username: str, action: str, note_id: Optional[str] = None):
    if not mysql_conn:
        return  # Fail silently if MySQL isn't available
    
    try:
        cursor = mysql_conn.cursor()
        cursor.execute(
            "INSERT INTO audit_logs (username, action, note_id) VALUES (%s, %s, %s)",
            (username, action, note_id)
        )
        mysql_conn.commit()
    except:
        pass  # Don't interrupt main app flow