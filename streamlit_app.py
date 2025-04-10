import streamlit as st
import requests
import mysql.connector
from datetime import datetime

# 💡 Verbindung zur MySQL-Datenbank
def connect_db():
    return mysql.connector.connect(
        host="kalach.mysql.db.hostpoint.ch",
        user="kalach_ihcwa",
        password="pGO3OAl2Jok2X6",
        database="kalach_ihcwiggertal"
    )

# 🔐 Bexio API Token laden
def get_token():
    with open("token_bexio.txt", "r") as file:
        return file.read().strip()

# 📥 Daten von Bexio laden
def fetch_bexio_contacts():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://api.bexio.com/2.0/contact"
    response = requests.get(url, headers=headers)
    return response.json()

# 💾 Daten in MySQL einfügen
def insert_into_db(contact):
    conn = connect_db()
    cursor = conn.cursor()

    sql = """
    INSERT INTO Data_bexio (
        id, name_1, name_2, address, postcode, city, mail, phone_fixed, updated_at
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        name_1 = VALUES(name_1),
        updated_at = VALUES(updated_at)
    """

    values = (
        contact["id"],
        contact.get("name_1"),
        contact.get("name_2"),
        contact.get("address"),
        contact.get("postcode"),
        contact.get("city"),
        contact.get("mail"),
        contact.get("phone_fixed"),
        datetime.now()
    )

    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()

# 🚀 Streamlit Interface
st.title("📡 Bexio Kontakte Synchronisieren")

if st.button("Kontakte von Bexio laden und in DB speichern"):
    contacts = fetch_bexio_contacts()
    for c in contacts:
        insert_into_db(c)
    st.success("✅ Kontakte wurden erfolgreich synchronisiert!")
