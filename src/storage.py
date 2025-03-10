import mysql.connector
from config import DB_CONFIG


def connect_db():
    """Connect to MySQL database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("✅ Connected to MySQL!")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Connection error: {err}")
        return None


def add_contact(number, name):
    """Add a contact to the database."""
    conn = connect_db()
    cursor = conn.cursor()
    sql = "INSERT IGNORE INTO contacts (number, name) VALUES (%s, %s)"
    cursor.execute(sql, (number, name))
    conn.commit()
    conn.close()


def save_receipt(contact_id, image_path, amount, payment_date):
    """Save a receipt to the database."""
    conn = connect_db()
    cursor = conn.cursor()
    sql = "INSERT INTO receipts (contact_id, image_path, amount, payment_date) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (contact_id, image_path, amount, payment_date))
    conn.commit()
    conn.close()


def get_contact(number):
    """Get contact ID from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    sql = "SELECT id FROM contacts WHERE number = %s"
    cursor.execute(sql, (number,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None