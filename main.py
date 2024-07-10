<<<<<<< HEAD
import os
from scripts.fetch_books import fetch_book_data
from scripts.process_books import process_book_data

def main():
    excel_file_path = os.path.join('data', 'book_names.xlsx')
    database_path = './data/my_database.db'

    # Fetch book data
    print("Fetching book data...")
    book_data = fetch_book_data(excel_file_path)

    # Process and store book data
    print("Processing book data...")
    process_book_data(book_data, database_path)

    print("Data processing complete.")

if __name__ == "__main__":
    main()
=======
import os
from scripts.fetch_books import fetch_book_data
from scripts.process_books import process_book_data

def main():
    excel_file_path = os.path.join('data', 'book_names.xlsx')
    database_path = './data/my_database.db'

    # Fetch book data
    print("Fetching book data...")
    book_data = fetch_book_data(excel_file_path)

    # Process and store book data
    print("Processing book data...")
    process_book_data(book_data, database_path)

    print("Data processing complete.")

if __name__ == "__main__":
    main()
>>>>>>> 2eecbf196ff83072512a18ddc62e138fb4adc888
