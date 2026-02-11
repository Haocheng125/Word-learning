import sqlite3
import os
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, db_path: str = "words.db"):
        self.db_path = db_path
        self.conn = None
        self.connect()
        self.create_tables()

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def create_tables(self):
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS word_lists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                list_name TEXT UNIQUE NOT NULL,
                file_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_words INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                list_id INTEGER,
                english TEXT NOT NULL,
                chinese TEXT NOT NULL,
                position INTEGER DEFAULT 0,
                FOREIGN KEY (list_id) REFERENCES word_lists (id),
                UNIQUE(list_id, english)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS study_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                list_id INTEGER,
                current_word_id INTEGER,
                current_position INTEGER DEFAULT 0,
                queue TEXT,
                last_study_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_words INTEGER DEFAULT 0,
                FOREIGN KEY (list_id) REFERENCES word_lists (id),
                FOREIGN KEY (current_word_id) REFERENCES words (id),
                UNIQUE(list_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS study_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                list_id INTEGER,
                word_id INTEGER,
                study_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'studied',
                FOREIGN KEY (list_id) REFERENCES word_lists (id),
                FOREIGN KEY (word_id) REFERENCES words (id)
            )
        ''')
        
        self.conn.commit()

    def create_word_list(self, list_name: str, file_name: str = None) -> int:
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO word_lists (list_name, file_name)
            VALUES (?, ?)
        ''', (list_name, file_name))
        self.conn.commit()
        cursor.execute('SELECT id FROM word_lists WHERE list_name = ?', (list_name,))
        return cursor.fetchone()['id']

    def add_words(self, list_id: int, words: List[Dict[str, str]]):
        cursor = self.conn.cursor()
        
        for position, word in enumerate(words, 1):
            cursor.execute('''
                INSERT OR IGNORE INTO words (list_id, english, chinese, position)
                VALUES (?, ?, ?, ?)
            ''', (list_id, word['english'], word['chinese'], position))
        
        total_words = len(words)
        cursor.execute('''
            UPDATE word_lists SET total_words = ? WHERE id = ?
        ''', (total_words, list_id))
        
        self.conn.commit()

    def get_word_list_id(self, list_name: str) -> Optional[int]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT id FROM word_lists WHERE list_name = ?', (list_name,))
        result = cursor.fetchone()
        return result['id'] if result else None

    def get_all_word_lists(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, list_name, file_name, created_at, total_words 
            FROM word_lists 
            ORDER BY created_at DESC
        ''')
        return [dict(row) for row in cursor.fetchall()]

    def get_words_by_list(self, list_id: int) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, english, chinese, position 
            FROM words 
            WHERE list_id = ? 
            ORDER BY position
        ''', (list_id,))
        return [dict(row) for row in cursor.fetchall()]

    def get_word_by_id(self, word_id: int) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, english, chinese FROM words WHERE id = ?', (word_id,))
        result = cursor.fetchone()
        return dict(result) if result else None

    def get_word_by_position(self, list_id: int, position: int) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, english, chinese, position 
            FROM words 
            WHERE list_id = ? AND position = ?
        ''', (list_id, position))
        result = cursor.fetchone()
        return dict(result) if result else None

    def get_total_words_count(self, list_id: int) -> int:
        cursor = self.conn.cursor()
        cursor.execute('SELECT total_words FROM word_lists WHERE id = ?', (list_id,))
        result = cursor.fetchone()
        return result['total_words'] if result else 0

    def save_progress(self, list_id: int, current_position: int, current_word_id: int, queue: List[int], completed_words: int = 0):
        import json
        cursor = self.conn.cursor()
        queue_json = json.dumps(queue)
        
        cursor.execute('''
            INSERT OR REPLACE INTO study_progress 
            (list_id, current_word_id, current_position, queue, completed_words, last_study_date)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (list_id, current_word_id, current_position, queue_json, completed_words))
        
        self.conn.commit()

    def get_progress(self, list_id: int) -> Dict:
        import json
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT current_word_id, current_position, queue, completed_words, last_study_date 
            FROM study_progress 
            WHERE list_id = ?
        ''', (list_id,))
        result = cursor.fetchone()
        
        if result:
            return {
                'current_word_id': result['current_word_id'],
                'current_position': result['current_position'],
                'queue': json.loads(result['queue']) if result['queue'] else [],
                'completed_words': result['completed_words'],
                'last_study_date': result['last_study_date']
            }
        
        return {
            'current_word_id': None,
            'current_position': 0,
            'queue': [],
            'completed_words': 0,
            'last_study_date': None
        }

    def add_study_history(self, list_id: int, word_id: int, status: str = 'studied'):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO study_history (list_id, word_id, status)
            VALUES (?, ?, ?)
        ''', (list_id, word_id, status))
        self.conn.commit()

    def delete_word_list(self, list_id: int):
        cursor = self.conn.cursor()
        
        cursor.execute('DELETE FROM study_history WHERE list_id = ?', (list_id,))
        cursor.execute('DELETE FROM study_progress WHERE list_id = ?', (list_id,))
        cursor.execute('DELETE FROM words WHERE list_id = ?', (list_id,))
        cursor.execute('DELETE FROM word_lists WHERE id = ?', (list_id,))
        
        self.conn.commit()

    def reset_progress(self, list_id: int):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM study_progress WHERE list_id = ?', (list_id,))
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()