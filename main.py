import parser_utils as parser


def main():
    driver = parser.create_driver()
    driver.get('https://duckduckgo.com/')
    # вызов get_data()
    parser.kill_driver(driver)


if __name__ == "__main__":
    main()
