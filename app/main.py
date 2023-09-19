from module.modules.argument_parser import ArgumentParser
from module.modules.book_scraper import scrape_books_info


def print_books_info(books):
    for i, book_info in enumerate(books, start=1):
        print(f'Book {i}:')
        print(f'Title: {book_info["Title"]}')
        print(f'Price: {book_info["Price"]}')
        print(f'Rating: {book_info["Rating"]}')
        print()


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arguments = arg_parser.return_parsed_arguments()
    scraped_books = scrape_books_info(arguments.b)
    print_books_info(scraped_books)
