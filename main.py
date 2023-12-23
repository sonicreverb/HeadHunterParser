import parser_utils as parser_utils
import data_utils as data_utils


def main():
    vacancies_prompts_links = []

    with open('input_links.txt', 'r', encoding='utf-8') as file:
        for line in file:
            vacancies_prompts_links.append(line)

    for vacancy_prompt_link in vacancies_prompts_links:
        driver = parser_utils.create_driver()
        driver.get('https://duckduckgo.com/')
        parser_utils.auth_and_save_cookies(driver)
        print(f'[MAIN] Поиск вакансий по заданной ссылке: ({vacancy_prompt_link.strip()})')
        vacancies_links = parser_utils.find_vacancies_links(driver, vacancy_prompt_link)
        data = []

        for vacancy_link in vacancies_links:
            try:
                data.append(parser_utils.get_data(driver, vacancy_link))
            except Exception as _ex:
                print(f"[MAIN] Во время получения информации об вакансии была вызвана ошибка ({_ex}). "
                      f"URL: ({vacancy_link})")

        if data:
            data_utils.write_to_excel('output.xlsx', data)


if __name__ == "__main__":
    main()
