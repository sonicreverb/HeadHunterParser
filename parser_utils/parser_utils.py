import requests

from bs4 import BeautifulSoup


# принимает url страницы и возвращает её HTML код
def get_html(url: str):
    response = requests.get(url)
    if response.ok:
        return response.text
    else:
        return None


# принимает url страницы и возвращает объект soup
def get_soup(url: str):
    html_text = get_html(url)
    if html_text:
        soup = BeautifulSoup(html_text,  'html.parser')
        return soup
    else:
        return None


# принимает на вход массив с вакансиями и добавляет в него ссылки на вакансии
def get_vacancy_links_from_page(url: str, vacancy_list: list):
    soup = get_html(url)
    if soup:
        ...
    else:
        print(f"[GET VACANCIES LINKS] Не удалось получить ссылки на вакансии на странице {url}")
