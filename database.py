import sqlite3
import json
from datetime import datetime

def init_database():
    conn = sqlite3.connect('user_sessions.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE,
            messages TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            summary TEXT,
            sentiment_analysis TEXT,
            image_prompt TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def save_session(session_id, messages, summary=None, sentiment=None, image_prompt=None):
    conn = sqlite3.connect('user_sessions.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO chat_sessions 
        (session_id, messages, summary, sentiment_analysis, image_prompt)
        VALUES (?, ?, ?, ?, ?)
    ''', (session_id, json.dumps(messages), summary, sentiment, image_prompt))
    
    conn.commit()
    conn.close()