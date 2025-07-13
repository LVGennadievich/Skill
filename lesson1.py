import requests
from bs4 import BeautifulSoup
import json
import time
import os

class LetterboxdParser:
    def __init__(self, username):
        self.base_url = "https://letterboxd.com"
        self.username = username
        self.movies = []

    def fetch_user_films_page(self, page=1):
        url = f"{self.base_url}/{self.username}/films/page/{page}/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/115.0.0.0 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Ошибка при получении страницы {url}: {e}")
            return None

    def parse_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        film_blocks = soup.find_all('li', class_='listitem')
        for block in film_blocks:
            # Название
            img_tag = block.find('img', alt=True)
            title = img_tag['alt'] if img_tag else None

            # Рейтинг
            rating_div = block.find('div', class_='rating')  # актуальный класс может отличаться
            rating = None
            if rating_div:
                try:
                    rating = float(rating_div.get_text(strip=True))
                except:
                    rating = None

            if title:
                self.movies.append({'title': title, 'rating': rating})

    def parse_all_pages(self, max_pages=3):
        for page in range(1, max_pages + 1):
            print(f"Парсинг страницы {page}")
            html = self.fetch_user_films_page(page)
            if html:
                self.parse_page(html)
                time.sleep(1)
            else:
                break

    def save_to_json(self, filename='data/user_ratings.json'):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    username = "rfeldman9"  # замените на реальный username
    parser = LetterboxdParser(username)
    parser.parse_all_pages(max_pages=3)
    parser.save_to_json()
    print("Парсинг завершен, данные сохранены в data/user_ratings.json")