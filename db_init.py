import sqlite3

def create_database():
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()

    # Create the tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS journal(
            entry_id INTEGER PRIMARY KEY, 
            date TEXT, 
            domain TEXT, 
            sentiment TEXT, 
            description TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS self_dev(
            entry_id INTEGER PRIMARY KEY, 
            date TEXT, 
            domain TEXT, 
            topic TEXT, 
            duration TEXT, 
            description TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS sentiments(
            sentiment_id INTEGER PRIMARY KEY, 
            sentiment TEXT, 
            icon TEXT, 
            color TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS domains(
            domain_id INTEGER PRIMARY KEY, 
            domain TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS topics(
            topic_id INTEGER PRIMARY KEY, 
            domain_id INTEGER, 
            topic TEXT,
            FOREIGN KEY(domain_id) REFERENCES domains(domain_id)
        )
    ''')

    # Insert initial entries for sentiments, domains, and topics
    sentiments = [('Positive', 'smile', 'green'), ('Negative', 'frown', 'red'),
                  ('Worried', 'frown', 'yellow'), ('Delighted', 'smile', 'blue')]
    c.executemany('INSERT INTO sentiments(sentiment, icon, color) VALUES (?, ?, ?)', sentiments)

    domains = [('Work',), ('Personal',), ('Global',)]
    c.executemany('INSERT INTO domains(domain) VALUES (?)', domains)

    topics = [('Coding', 'Open Source'), ('Training', 'Coursera'), ('Blogs', 'Medium')]
    c.executemany('INSERT INTO topics (domain_id, topic) VALUES (?, ?)', topics)

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()