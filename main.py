import parser_utils as parser


def main():
    vacancies_prompts_links = []

    with open('input_links.txt', 'r', encoding='utf-8') as file:
        for line in file:
            vacancies_prompts_links.append(line)

    for vacancy_prompt_link in vacancies_prompts_links:
        driver = parser.create_driver()
        driver.get('https://duckduckgo.com/')
        print(f'[MAIN] Поиск вакансий по заданной ссылке: ({vacancy_prompt_link.strip()})')
        vacancies_links = parser.find_vacancies_links(driver, vacancy_prompt_link)
        # получение информации о вакансиях
        # запись вакансий в xlsx


if __name__ == "__main__":
    main()
