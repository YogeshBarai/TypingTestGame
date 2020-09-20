import os
import sqlite3
import glob

class TypingTestDB:  
    def __init__(self):
        self.DB_NAME = r"\TypingTestGame\TypingTest_DB.db"

    def directory_path(self):
        curr_file_path = os.path.dirname(os.path.abspath(__file__))
        curr_file_path = curr_file_path[:curr_file_path.rfind('\\')]
        db_file_path = curr_file_path + self.DB_NAME
        print(db_file_path)
        return db_file_path

    def search(self,entry_id):
        path_str = self.directory_path()
        conn = sqlite3.connect(path_str)
        cur = conn.cursor()
        cur.execute("SELECT display_sentence FROM tbl_sentences where id=?", (entry_id,))
        rows = cur.fetchall()
        conn.close()
        text = rows[0][0]
        return text