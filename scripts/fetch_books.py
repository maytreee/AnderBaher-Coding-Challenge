import requests
import time
import pandas as pd

def fetch_book_data(file_path):
    base_url = "https://openlibrary.org/search.json?q="
    list_of_books = []
    headers = {"accept": "application/json"}

    try:
        # Read the Excel file
        df = pd.read_excel(file_path)
        print("Columns in the Excel file:", df.columns)
        print(df.head())

        # Fetch data for each book
        for book in df['Books']:
            book_dict = {}
            name_of_book = book.replace(' ', '+')
            url = base_url + name_of_book
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()

                if response.status_code == 200:
                    data = response.json()
                    if 'docs' in data and len(data['docs']) > 0:
                        first_book = data['docs'][0]
                        book_dict['title'] = first_book.get('title', 'N/A')
                        book_dict['author_name'] = first_book.get('author_name', ['N/A'])[0]
                        book_dict['author_key'] = first_book.get('author_key', ['N/A'])[0]
                        book_dict['ebook_access'] = first_book.get('ebook_access', 'N/A')
                        book_dict['first_publish_year'] = first_book.get('first_publish_year', 'N/A')
                        book_dict['format'] = first_book.get('format', 'N/A')
                        list_of_books.append(book_dict)
                    else:
                        print("No books found in the response.")
                else:
                    print(f"Failed to retrieve data: {response.status_code}")

                # Sleep to avoid rate limiting
                time.sleep(1)

            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")

    except FileNotFoundError:
        print(f"The file at {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return list_of_books
