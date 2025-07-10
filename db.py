# db.py
import sqlite3

DB_PATH = "D:/rental/rental_manager.db"

def connect():
    return sqlite3.connect(DB_PATH)

# תעריפים
def fetch_tariffs():
    conn = connect()
    c = conn.cursor()
    c.execute("""
        SELECT group_id, start_date, vat, price_per_kwh,
               fixed_electricity_daily, price_per_cubic_meter
        FROM tariffs
        ORDER BY group_id, start_date DESC
    """)
    results = c.fetchall()
    conn.close()
    return results

def insert_tariff(data):
    conn = connect()
    c = conn.cursor()
    c.execute("""
        INSERT INTO tariffs (
            group_id, start_date, vat, price_per_kwh,
            fixed_electricity_daily, price_per_cubic_meter
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

def update_tariff(data):
    conn = connect()
    c = conn.cursor()
    c.execute("""
        UPDATE tariffs
        SET vat = ?, price_per_kwh = ?, fixed_electricity_daily = ?, price_per_cubic_meter = ?
        WHERE group_id = ? AND start_date = ?
    """, data)
    conn.commit()
    conn.close()

def delete_tariff(group_id, start_date):
    conn = connect()
    c = conn.cursor()
    c.execute("""
        DELETE FROM tariffs
        WHERE group_id = ? AND start_date = ?
    """, (group_id, start_date))
    conn.commit()
    conn.close()

# דירות
def fetch_apartments():
    conn = connect()
    c = conn.cursor()
    c.execute("""
        SELECT apartment_id, tariff_group_id, group_apartment
        FROM apartments
        ORDER BY apartment_id
    """)
    results = c.fetchall()
    conn.close()
    return results

