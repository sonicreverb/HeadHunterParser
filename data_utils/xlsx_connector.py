import os
import openpyxl


def write_to_excel(filename, data):
    # проверяем, существует ли файл
    if os.path.exists(filename):
        # если файл существует, открываем его и выбираем активный лист
        wb = openpyxl.load_workbook(filename)
        ws = wb.active
        # считывание уже присутствующих ссылок в таблице
    else:
        # если файл не существует, создаем новую книгу Excel и выбираем активный лист
        wb = openpyxl.Workbook()
        ws = wb.active

    # добавляем заголовки таблицы
    headers = list(data[0].keys())
    for col_num, header in enumerate(headers, 1):
        ws.cell(row=1, column=col_num, value=header)

    # записываем данные в конец таблицы
    for row_num, row_data in enumerate(data, ws.max_row + 1):
        for col_num, key in enumerate(headers, 1):
            cell = ws.cell(row=row_num, column=col_num, value=row_data[key])

    # сохраняем книгу Excel
    wb.save(filename)

    print(f'[ЗАПИСЬ В ЭКСЕЛЬ] Данные успешно записаны в файл {filename}')