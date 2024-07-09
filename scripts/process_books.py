import sqlite3

def process_book_data(list_of_books, db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Create table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            author_key TEXT,
            ebook_access TEXT,
            publish_year INTEGER
        )
    ''')
    conn.commit()

    # Insert data
    for book in list_of_books:
        cur.execute('''
            INSERT INTO books (title, author, author_key, ebook_access, publish_year)
            VALUES (?, ?, ?, ?, ?)
        ''', (book['title'], book['author_name'], book['author_key'], book['ebook_access'], book['first_publish_year']))
    conn.commit()
    conn.close()
