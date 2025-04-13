import sqlite3


class DataBase:
    def __init__(self, db_name: str = "tk.db"):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self.connection:
            self.connection.close()

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.connection.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            return f"Error connecting to database: {e}"


    def get_article(self, article_number: str):
        if not self.connection:
            self.connect()

        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT article_text FROM articles WHERE number = ?", (article_number,))
                result = cursor.fetchone()
                return result[0] if result else None
        except sqlite3.Error as e:
            return f"Unable to find the article: {e}"