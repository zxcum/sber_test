import sqlite3
import pandas as pd
from datetime import date, datetime


class DataBase:
    def __init__(self, db_name: str = "shops.db"):
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

    def add_sale(self, shop_name: str, sale_list: dict, date: str):
        if not self.connection:
            self.connect()

        shop_id = shop_name
        for prod_name in sale_list.keys():
            prod_id = self.get_prod_id(name=prod_name)

            try:
                with self.connection:
                    cursor = self.connection.cursor()
                    cursor.execute("INSERT INTO sales (product_id, quantity, shop_id, day) VALUES (?, ?, ?, ?)",
                                   (prod_id, sale_list[prod_name], shop_id, date))
            except sqlite3.Error as e:
                return f"Error inserting a sale id: {e}"

        return "success"

    def get_prod_id(self, name: str):
        if not self.connection:
            self.connect()

        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT id FROM product WHERE name = ?", (name,))
                prod_id = cursor.fetchone()
                return prod_id['id']
        except sqlite3.Error as e:
            return f"Error getting prodcut id: {e}"

    def get_shop_id(self, name: str):
        if not self.connection:
            self.connect()
        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT id FROM shop WHERE name = ?", (name,))
                shop_id = cursor.fetchone()
                return shop_id['id']
        except sqlite3.Error as e:
            return f"Error getting shop id: {e}"

    def get_plan(self, shop_id: str):
        if not self.connection:
            self.connect()

        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT product_plan, month FROM plan WHERE shop_id = ?", (shop_id,))
                plans = cursor.fetchall()
                today = date.today().strftime('%Y-%m-%d')
                year_now, month_now, day_now = today.split("-")
                for row in plans:
                    year, month, day = row['month'].split("-")
                    if year == year_now and month == month_now:
                        return row['product_plan']
        except sqlite3.Error as e:
            return f"Error getting plan: {e}"

    def get_sales_by_shop(self, shop_id: str):
        if not self.connection:
            self.connect()

        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("""
                        SELECT 
                            product_id, 
                            SUM(quantity) as total_quantity
                        FROM sales 
                        WHERE shop_id = ?
                        GROUP BY product_id
                        ORDER BY total_quantity DESC
                    """, (shop_id,))
                sales = cursor.fetchall()
                result = {}
                for sale in sales:
                    result[sale['product_id']] = sale['total_quantity']
                return result
        except sqlite3.Error as e:
            return f"Error getting sales: {e}"

    def get_prod_ids(self):
        if not self.connection:
            self.connect()

        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM product")
                ids = cursor.fetchall()
                prod_ids = {}
                for row in ids:
                    prod_ids[row['id']] = row['name']
                return prod_ids
        except sqlite3.Error as e:
            return f"Error getting prodcuts id: {e}"
