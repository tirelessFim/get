import sqlite3
from dadata import Dadata


def create_table(argument_1, argument_2, argument_3):
    conn = sqlite3.connect('order.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stocks (token text, api text, language text)''')
    arguments = (argument_1, argument_2, argument_3)
    cursor.execute("INSERT INTO stocks VALUES(?, ?, ?)", arguments)
    conn.commit()


# Вытягиваем данные из таблицы
def take_values():
    conn = sqlite3.connect('order.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stocks")
    ordered_list = cursor.fetchall()
    conn.commit()
    return ordered_list


# Дропаем таблицу
def delete_table():
    conn = sqlite3.connect('order.db')
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE if EXISTS stocks''')
    conn.commit()


def get_coordinates():
    print("\n***** Вы запустили программу. *****")
    print("Для начала сделаем небольшую настройку:\n")

    # Вводим Токен
    while True:
        token = input("Введите token: ")

        if token == 'quit':
            print("Программа остановлена. До свидания!")

            quit()
        elif len(token) < 40:
            print("Некорректно введен token. Длина менее 40 сивлолов")
        elif len(token) > 40:
            print("Некорректно введен token. Длина более 40 сивлолов")
        else:
            break

    # Вводим API-ключ
    while True:
        secret = input("Введите API-ключ: ")

        if secret == 'quit':
            print("Программа остановлена. До свидания!")

            quit()
        elif len(secret) < 40:
            print("Некорректно введен API-ключ. Длина менее 40 сивлолов")
        elif len(secret) > 40:
            print("Некорректно введен API-ключ. Длина более 40 сивлолов")
        else:
            break
    # Вводим язык
    language = input("Введите тип языка ru / en: ")

    # Проверка языка. Если не en, то автоматически выставляется ru
    if language != "ru" and language != "en":
        language = "ru"
    else:
        pass

    print("\nДанные записаны. Продолжаем работать...")

    # Вызываем метод создание таблицы
    create_table(token, secret, language)

    while True:
        addresses_list = []
        base_token = take_values()[0][0]
        base_secret = take_values()[0][1]
        base_language = take_values()[0][2]
        value = input("\nВведите адрес: ")

        if value == "quit":
            print("Программа остановлена. До свидания!")

            delete_table()
            quit()
        else:
            # Запрос в dadata
            dadata = Dadata(base_secret, base_token)
            result = dadata.suggest(name="address", query=value, count=5, language=base_language)
            variant_number = 0

            print('\nСписок вариантов адресов:')

            # Выдаем список вариантов похожих на запрос
            for i in result:
                variant_number += 1
                addresses_list.append(i['value'])
                print(f"№{variant_number} {i['value']}")

            # Далее пользователь выбирает вариант из выпавшего списка
            while True:
                user_variant_number = input("\nВведите номер подходящего варианта: ")

                if user_variant_number == "quit":
                    print("Программа остановлена. До свидания!")

                    delete_table()
                    quit()
                else:
                    if 1 <= int(user_variant_number) <= len(addresses_list):
                        result = dadata.clean("address", addresses_list[int(user_variant_number) - 1])

                        print()
                        print('Результат поиска:')
                        print(result["result"])
                        print(f"Широта: {result['geo_lat']}, Долгота: {result['geo_lon']}")

                        break
                    else:
                        print("Номер указан неверно.")
