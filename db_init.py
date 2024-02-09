import sqlite3

def create_database():
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()

    # Create the tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS journal(
            entry_id INTEGER PRIMARY KEY, 
            date TEXT, 
            domain_id INTEGER, 
            sentiment_id INTEGER, 
            description TEXT,
            FOREIGN KEY(domain_id) REFERENCES domains(domain_id)
            FOREIGN KEY(sentiment_id) REFERENCES sentiments(sentiment_id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS self_dev(
            entry_id INTEGER PRIMARY KEY, 
            date TEXT, 
            domain_self_dev_id INTEGER, 
            topic_id INTEGER, 
            duration Integer, 
            description TEXT,
            FOREIGN KEY(domain_self_dev_id) REFERENCES domains_self_dev(domain_self_dev_id)
            FOREIGN KEY(topic_id) REFERENCES topics(topic_id)
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
        CREATE TABLE IF NOT EXISTS domains_self_dev(
            domain_self_dev_id INTEGER PRIMARY KEY, 
            domain TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS topics(
            topic_id INTEGER PRIMARY KEY, 
            topic TEXT
        )
    ''')

    # Insert initial entries for sentiments, domains, and topics
    sentiments = [('Positive', 'smile', 'green'), ('Negative', 'frown', 'red'),
                  ('Worried', 'frown', 'yellow'), ('Delighted', 'smile', 'green'),]
    c.executemany('INSERT INTO sentiments(sentiment, icon, color) VALUES (?, ?, ?)', sentiments)

    domains = [('Work',), ('Personal',), ('Global',)]
    c.executemany('INSERT INTO domains(domain) VALUES (?)', domains)
    
    domains_self_dev = [('Coding',), ('Learning',), ('Trend view',)]
    c.executemany('INSERT INTO domains_self_dev(domain) VALUES (?)', domains_self_dev)

    topics = [('Open Source',), ('Reading',), ('Exercise',), ('Presonal Project',), ('Learning',)]
    c.executemany('INSERT INTO topics (topic) VALUES (?)', topics)

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()