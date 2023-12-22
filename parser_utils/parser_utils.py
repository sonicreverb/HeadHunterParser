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
