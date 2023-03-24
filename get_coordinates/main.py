from models import delete_table, get_coordinates

print('      Программа для поиска координат.')
print('--------------------------------------------')
print('1. Команда "start" - для начала работы ')
print('2. Команда "quit" - для выхода из программы ')

press = input('\nВведите команду: ')
delete_table()

while True:
    if press == "quit":
        print("Программа остановлена. До свидания!")

        quit()
    elif press == "start":
        get_coordinates()
    else:
        print('Команда введена некорректно.')

        press = input('Введите команду: ')

