# import time
import os.path
import pickle
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
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


# sub функция
def get_text_or_empty(element):
    return element.text.strip() if element else ''


# аутенфикация и получение кук
def auth_and_save_cookies(driver):
    try:
        mail = 'telojo6668@watrf.com'
        password = 'LJPWg8IHKoXh!U#5Q!7-'

        change_driver_url(driver, 'https://hh.ru/account/login?backurl=%2F&hhtmFrom=main')

        buttonLoginWithPass = driver.find_element(By.XPATH,
                                                  '//*[@id="HH-React-Root"]/div/div[4]/div[1]/div/div/div/div/div/div[1'
                                                  ']/div[1]/div/div[2]/form/div[4]/button[2]')
        buttonLoginWithPass.click()

        inputLogin = driver.find_element(By.XPATH, '//*[@id="HH-React-Root"]/div/div[4]/div['
                                                   '1]/div/div/div/div/div/div[1] '
                                                   '/div[1]/div/form/div[1]/fieldset/input')
        inputLogin.clear()
        inputLogin.send_keys(mail)

        inputPass = driver.find_element(By.XPATH, '//*[@id="HH-React-Root"]/div/div[4]/div['
                                                  '1]/div/div/div/div/div/div[1]/ '
                                                  'div[1]/div/form/div[2]/fieldset/input')
        inputPass.clear()
        inputPass.send_keys(password)

        buttonLogin = driver.find_element(By.XPATH, '//*[@id="HH-React-Root"]/div/div[4]/div['
                                                    '1]/div/div/div/div/div/div[1] '
                                                    '/div[1]/div/form/div[6]/button[1]')
        buttonLogin.click()
        time.sleep(5)
        # сохранение cookies
        pickle.dump(driver.get_cookies(), open('cookies.pkl', 'wb'))
        print(f'[AUTHENTICATION] Авторизация успешна. Кукис получены.')
    except Exception as _ex:
        print(f'[AUTHENTICATION] Не удалось войти в аккаунт и сохранить куки. Ошибка: ({_ex}).')


# загрузка кук
def load_cookies(driver):
    try:
        if os.path.exists('cookies.pkl'):
            for cookie in pickle.load(open('cookies.pkl', 'rb')):
                driver.add_cookie(cookie)
            driver.refresh()
            print('[COOKIES LOAD] Куки успешно загружены в драйвер.')
            return True
        else:
            print('[COOKIES LOAD] Не удалось загрузить куки в драйвер.')
            return False
    except Exception as _ex:
        for cookie in pickle.load(open('cookies.pkl', 'rb')):
            print(cookie)
        print(f'[COOKIES LOAD] Ошибка во время попытки загрузить куки ({_ex})')
        return False


# принимает на вход драйвер и url вакансии, возвращает словарь с информацией о вакансии
def get_data(driver, url):
    change_driver_url(driver, url)
    vacancy_data = {'Post': '', 'Salary': '', 'ReqWorkExp': '', 'TypeOfEmployment': '', 'CompanyName': '',
                    'CompanyInfo': '', 'Duties': '', 'Requirements': '', 'Working conditions': '', 'Downmark': '',
                    'ReqSkills': '', 'ContactName': '', 'ContactPhone': '', 'ContactMail': '', 'VacancyURL': '',
                    'CompanySiteURL': '', 'CompanyActitvityAreas': '', 'CompanyAddress': '', 'CompanyDescription': '',
                    'CompanyHHPageURL': ''}

    soup = get_htmlsoup(driver)

    # Название вакансии
    vacancy_title_element = soup.find('h1', {'data-qa': 'vacancy-title'})
    if not vacancy_title_element:
        raise Exception(f"Не удалось получить название вакансии ({url})")
    vacancy_data['Post'] = get_text_or_empty(vacancy_title_element)

    # Зарплата
    salary_element = soup.find('span', {'data-qa': 'vacancy-salary-compensation-type-net'})
    if not salary_element:
        salary_element = soup.find('span', {'data-qa': 'vacancy-salary-compensation-type-gross'})
        if not salary_element:
            # raise Exception(f"Не удалось получить заработную плату ({url})")
            vacancy_data['Salary'] = 'Не указана'
        else:
            vacancy_data['Salary'] = get_text_or_empty(salary_element)

    # Требуемый опыт работы
    experience_element = soup.find('p', {'class': 'vacancy-description-list-item'})
    vacancy_data['ReqWorkExp'] = get_text_or_empty(experience_element)

    # Тип занятости
    employment_element = soup.find('p', {'data-qa': 'vacancy-view-employment-mode'})
    vacancy_data['TypeOfEmployment'] = get_text_or_empty(employment_element)

    # Название компании
    company_name_element = soup.find('span', {'data-qa': 'bloko-header-2'})
    vacancy_data['CompanyName'] = get_text_or_empty(company_name_element)

    # Информация о компании
    vacancy_data['CompanyInfo'] = ''

    description_block = soup.find('div', class_='g-user-content')
    if not description_block:
        raise Exception(f"Не удалось найти описание ({url})")

    description_block_text = description_block.get_text()

    # Основные задачи
    duty_patterns = ['Обязанности:', 'Чем предстоит заниматься:', 'Задачи:', 'Что важно и что делать?',
                     'Основные задачи:', 'Должностные обязанности:']
    for duty_pattern in duty_patterns:
        if duty_pattern in description_block_text:
            vacancy_data['Duties'] = description_block_text[description_block_text.find(duty_pattern):]
            break

    requirements_patterns = ['Требования:', 'Что мы ждём от кандидата:', 'Что нам важно:']
    for requirements_pattern in requirements_patterns:
        if requirements_pattern in description_block_text:
            vacancy_data['Requirements'] = description_block_text[description_block_text.find(requirements_pattern):]
            break

    # Условия
    conditions_patterns = ['Условия:', 'Мы предлагаем:']
    for conditions_pattern in conditions_patterns:
        if conditions_pattern in description_block_text:
            vacancy_data['Working conditions'] = description_block_text[description_block_text.
                                                                        find(conditions_pattern):]
            break

    # Пометка снизу
    paragraphs = description_block.find_all('p')
    if paragraphs:
        vacancy_data['Downmark'] = paragraphs[len(paragraphs) - 1].get_text()

    # Ключевые навыки
    skills_element = soup.find('div', {'class': 'bloko-tag-list'})
    if skills_element:
        skill_elements = skills_element.find_all('span', {'class': 'bloko-tag__section_text', 'data-qa': 'bloko'
                                                                                                         '-tag__text'})
        skills_li = [element.get_text(strip=True) for element in skill_elements]
        for skill in skills_li:
            vacancy_data['ReqSkills'] += skill + '\n'
    else:
        vacancy_data['ReqSkills'] = 'Не указано'

    if soup.find('button', {'data-qa': 'show-employer-contacts show-employer-contacts_top-button'}):
        try:
            buttonShowContacts = driver.find_element(By.CSS_SELECTOR, '#HH-React-Root > div > '
                                                                      'div.HH-MainContent.HH-Supernova-MainContent > '
                                                                      'div.main-content.main-content_broad-spacing > '
                                                                      'div > div > div > div > '
                                                                      'div.bloko-column.bloko-column_container.bloko'
                                                                      '-column_xs-4.bloko-column_s-8.bloko-column_m-12.'
                                                                      'bloko-column_l-10 > '
                                                                      'div:nth-child(1) > div.bloko-column.bloko-column'
                                                                      '_xs-4.bloko-column_s-8.bloko-column_m-12.bloko-'
                                                                      'column_l-10 > div > '
                                                                      'div.noprint > div.noprint > div > div.vacancy-'
                                                                      'action.vacancy-action_stretched.vacancy-action_'
                                                                      'stretched-redesigned > button')
            buttonShowContacts.click()
            time.sleep(0.5)
            soup = get_htmlsoup(driver)

            # Контактное лицо
            contact_name_elem = soup.find('div', {'data-qa': 'vacancy-contacts__fio'})
            if not contact_name_elem:
                contact_name_elem = soup.find('p', {'data-qa': 'vacancy-contacts__fio'})
            vacancy_data['ContactName'] = get_text_or_empty(contact_name_elem)

            # Телефон
            contact_phone_elem = soup.find('p', {'data-qa': 'vacancy-contacts__phone'})
            if not contact_phone_elem:
                contact_phone_elem = soup.find('div', class_='vacancy-contacts-call-tracking__phone-number')
            vacancy_data['ContactPhone'] = get_text_or_empty(contact_phone_elem)

            # Почта
            contact_mail_elem = soup.find('a', {'data-qa': 'vacancy-contacts__email'})
            vacancy_data['ContactMail'] = get_text_or_empty(contact_mail_elem)

        except NoSuchElementException as _ex:
            print(_ex)

    # Ссылка на вакансию
    vacancy_data['VacancyURL'] = url

    host = url[:url.find("/vacancy")]
    company_hh_url = soup.find('a', {'data-qa': 'vacancy-company-name'})
    if not company_hh_url:
        raise Exception(f"Не удалось получить информацию об компании ({url}).")

    company_hh_url = host + company_hh_url.get('href')
    change_driver_url(driver, company_hh_url)

    soup = get_htmlsoup(driver)

    employeer_block = soup.find('div', class_='employer-sidebar')
    if not employeer_block:
        raise Exception(f"Не удалось получить информацию об нанимателе. ({url})")

    employeer_sidebar = employeer_block.find_all('div', class_='employer-sidebar-block')

    # Сайт компании
    company_site_elem = soup.find('button', {'data-qa': 'sidebar-company-site'})
    vacancy_data['CompanySiteURL'] = get_text_or_empty(company_site_elem)

    # Сферы деятельности
    try:
        company_activity = employeer_sidebar[2]
        vacancy_data['CompanyActitvityAreas'] = get_text_or_empty(company_activity).replace('Сферы деятельности', '')
    except IndexError:
        pass

    # Адресс
    try:
        company_location_elem = employeer_sidebar[0]
        vacancy_data['CompanyAddress'] = get_text_or_empty(company_location_elem)
    except IndexError:
        pass

    # Описание
    company_desc_elem = soup.find('div', {'data-qa': 'company-description-text'})
    vacancy_data['CompanyDescription'] = get_text_or_empty(company_desc_elem)

    # Ссылка на страницу компани HH
    vacancy_data['CompanyHHPageURL'] = company_hh_url

    return vacancy_data
