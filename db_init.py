import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect('database/app.db')       
        print(f'successful connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(e)
    return conn

def close_connection(conn):
    conn.close()
    print('connection closed')

def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE Journal(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Date DATE NOT NULL,
        Domain TEXT NOT NULL,
        Sentiment TEXT NOT NULL,
        Description TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE SelfDevelopment(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Date DATE NOT NULL,
        Domain TEXT NOT NULL,
        Topic TEXT NOT NULL,
        TimeSpent INTEGER NOT NULL,
        Description TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE Configuration(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Sentiment TEXT NOT NULL,
        Icon TEXT NOT NULL,
        Color TEXT NOT NULL
    )
    """)

    conn.commit()

def main():
    conn = create_connection()
    create_tables(conn)
    close_connection(conn)

if __name__ == "__main__":
    main()