from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup


# возвращает driver
def create_driver():
    print('[DRIVER INFO] Driver created successfully.\n')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))


# закрывает все окна и завершает сеанс driver
def kill_driver(driver):
    driver.close()
    driver.quit()
    print('[DRIVER INFO] Driver was closed successfully.\n')


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


# добавляет в список vacancies_links ссылки с текущей страницы на все вакансии
def get_vacancies_links(driver, url: str, vacancies_links: list):
    ...


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
