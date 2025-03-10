import mysql.connector
from config import DB_CONFIG

def connect_db():
    """Conecta ao banco de dados MySQL."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("Conectado ao MySQL!")
        return conn
    except mysql.connector.Error as err:
        print(f"Erro de conexão: {err}")
        return None

def add_contact(number, name):
    """Adiciona um contato ao banco de dados."""
    conn = connect_db()
    cursor = conn.cursor()
    sql = "INSERT IGNORE INTO contacts (number, name) VALUES (%s, %s)"
    cursor.execute(sql, (number, name))
    conn.commit()
    conn.close()

def save_receipt(contact_id, image_path, amount, payment_date):
    """Salva um comprovante no banco de dados."""
    conn = connect_db()
    cursor = conn.cursor()
    sql = "INSERT INTO receipts (contact_id, image_path, amount, payment_date) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (contact_id, image_path, amount, payment_date))
    conn.commit()
    conn.close()

def get_contact(number):
    """Obtém o ID de um contato do banco de dados."""
    conn = connect_db()
    cursor = conn.cursor()
    sql = "SELECT id FROM contacts WHERE number = %s"
    cursor.execute(sql, (number,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None