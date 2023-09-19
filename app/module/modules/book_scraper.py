"""
This will be class in the future.
"""
import sys

import requests
from bs4 import BeautifulSoup


def scrape_books_info(number_of_books):
    """
    Taking care for scraping N number of books.
    Will be in class in the future.

    :param number_of_books: Number of books
    :return: List of book dictionaries
    """

    working_url = 'https://books.toscrape.com/'
    response = requests.get(working_url)
    document_parser = BeautifulSoup(response.text, 'html.parser')
    books_info = []

    if response.status_code != 200:
        print(f'Server status code {response.status_code}')
        return sys.exit(1)

    books_to_extract = number_of_books
    extracted_books_per_page = 0

    while True:
        books_article_tags = document_parser.find_all('article', class_='product_pod')
        number_of_books_on_page = len(books_article_tags)

        for book in books_article_tags:
            book_title = book.h3.a['title']
            book_price = book.select('div p.price_color')[0].get_text()
            book_rating = book.select_one('p.star-rating')['class'][1]

            books_info.append({
                'Title': book_title,
                'Price': book_price,
                'Rating': book_rating
            })
            extracted_books_per_page += 1
            books_to_extract -= 1

            if books_to_extract == 0:
                [print(index + 1, el) for index, el in enumerate(books_info)]
                return books_info

            if extracted_books_per_page == number_of_books_on_page:
                pager_tag = document_parser.find('ul', class_='pager')
                try:
                    next_page_url_href = pager_tag.find('li', class_='next').findNext().get(
                        'href')
                except AttributeError:
                    return books_info

                next_page_url = 'http://books.toscrape.com/' if 'catalogue/' in next_page_url_href else 'http://books.toscrape.com/catalogue/'
                next_page_link = next_page_url + next_page_url_href
                current_response = requests.get(next_page_link)
                document_parser = BeautifulSoup(current_response.text, 'xml')
                extracted_books_per_page = 0
                break
