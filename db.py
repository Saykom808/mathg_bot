import sqlite3
import threading


class Database:
    def __init__(self, db_file):
        self.lock = threading.Lock()
        self.conn = sqlite3.connect(db_file, check_same_thread=False)

    def add_user(self, user_id):
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO `users` (`user_id`) VALUES (?)', (user_id,))
            self.conn.commit()

    def user_exists(self, user_id):
        with self.lock:
            cursor = self.conn.cursor()
            result = cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def set_nickname(self, user_id, nickname):
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE `users` SET `nickname` = ? WHERE `user_id` = ?", (nickname, user_id,))
            self.conn.commit()

    def get_signup(self, user_id):
        with self.lock:
            cursor = self.conn.cursor()
            result = cursor.execute("SELECT `signup` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            signup = str(result[0][0]) if result else ""
            return signup

    def set_signup(self, user_id, signup):
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE `users` SET `signup` = ? WHERE `user_id` = ?", (signup, user_id,))
            self.conn.commit()


    def get_nickname(self, user_id):
        with self.lock:
            cursor = self.conn.cursor()
            result = cursor.execute("SELECT `nickname` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            nickname = str(result[0][0]) if result else ""
            return nickname