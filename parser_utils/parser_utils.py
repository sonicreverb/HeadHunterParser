# import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


# Возвращает настроенный driver с отключенной загрузкой изображений
def create_driver():
    chrome_options = Options()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # print('[DRIVER INFO] Driver created successfully with images disabled.\n')
    return driver


# закрывает все окна и завершает сеанс driver
def kill_driver(driver):
    driver.close()
    driver.quit()
    # print('[DRIVER INFO] Driver was closed successfully.\n')


# возвращает soup указанной страницы
def get_htmlsoup(driver):
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        return soup

    except Exception as exc:
        print(f'[GET SOUP] Error while trying to get soup was accuired {exc}')
        return None


# меняет текущий url driver
def change_driver_url(driver, new_url: str):
    driver.execute_script('window.location.href = arguments[0];', new_url)


# принимает на вход driver с открытым окном и url страницы со списком вакансий, возвращает список ссылок на вакансии
def find_vacancies_links(driver, url: str):
    vacancies_links = []

    change_driver_url(driver, url)
    soup = get_htmlsoup(driver)
    links_li = soup.find_all('a', {'class': 'serp-item__title'})

    for link_elem in links_li:
        vacancies_links.append(link_elem.get('href'))
    print(f'[GET VACANCIES LINKS] Кол-во найденных вакансий на текущей странице: {len(links_li)}')

    current_url = url
    while soup.find('a', {'data-qa': 'pager-next'}):
        new_url = soup.find('a', {'data-qa': 'pager-next'}).get('href')
        host = current_url[:current_url.find('/search')]
        new_url = host + new_url
        print(f'[GET VACANCIES LINKS] Переход на след. страницу ({new_url}).')
        change_driver_url(driver, new_url)
        current_url = new_url
        soup = get_htmlsoup(driver)
        links_li = soup.find_all('a', {'class': 'serp-item__title'})

        for link_elem in links_li:
            vacancies_links.append(link_elem.get('href'))
        print(f'[GET VACANCIES LINKS] Кол-во найденных вакансий на текущей странице: {len(links_li)}')

    return vacancies_links


# принимает на вход драйвер и url вакансии, возвращает словарь с информацией о вакансии
def get_data(driver, url):
    change_driver_url(driver, url)
    vacancy_data = {'Post', 'Salary', 'ReqWorkExp', 'TypeOfEmployment', 'CompanyName', 'CompanyInfo', 'Duties',
                    'Working conditions', 'ReqSkills', 'ContactName', 'ContactPhone', 'ContactMail', 'ContactURL',
                    'CompanySiteURL', 'CompanyActitvityAreas', 'CompanyAddress', 'CompanyDescription',
                    'CompanyHHPageURL'}

    '''
    ПАРСИНГ ИНФОРМАЦИИ
    '''

    return vacancy_data
