#не работает потому что для проверки сразу нескольких чатов нужно быть администратором 

import pandas as pd
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import ChatAdminRequiredError, UserNotParticipantError
from telethon.tl.types import User

api_id = 'можно узнать на https://my.telegram.org'
api_hash = 'можно узнать на https://my.telegram.org/'
phone = 'номер на который акк зарегестрирован'

def get_usernames_from_file(file_path):
    try:
        usernames_df = pd.read_csv(file_path)
        return usernames_df['username'].tolist() # наименование колонки в файле
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return []

def get_participants(client, chat):
    try:
        # Получение списка участников группы
        participants = client.get_participants(chat)
        return participants
    except (ChatAdminRequiredError, UserNotParticipantError):
        print(f"Ошибка: Не достаточно прав для доступа к участникам группы {chat.title}.")
        return []
    except Exception as e:
        print(f"Ошибка при получении участников для группы {chat.title}: {e}")
        return []

def main():
    client = TelegramClient(phone, api_id, api_hash)
    client.connect()

    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Введите код: '))

    print(client.get_me())

    # Получение списка групп, на которые подписан пользователь
    my_groups = client.get_dialogs()

    # Считывание имен пользователей из файла
    file_path = 'путь к документу'
    usernames_to_search = get_usernames_from_file(file_path)

    if not usernames_to_search:
        print("Файл с именами пользователей пуст или не найден.")
        return

    # Создание DataFrame с информацией об участниках
    df_users = pd.DataFrame()

    for group in my_groups:
        chat = group.entity

        # Получение списка участников группы с обработкой ошибок
        participants = get_participants(client, chat)

        # Добавление информации об участниках в DataFrame
        df_users_group = pd.DataFrame([{'id': participant.id, 'first_name': participant.first_name, 'last_name': participant.last_name, 'group': chat.username if hasattr(chat, 'username') else 'Unknown Group'} for participant in participants])
        df_users = pd.concat([df_users, df_users_group])

    # Фильтрация участников по именам из файла
    filtered_users = df_users[df_users['first_name'].isin(usernames_to_search)]

    if filtered_users.empty:
        print("Участники не найдены.")
        return

    # Вывод таблицы с информацией о подписках
    print(filtered_users[['first_name', 'last_name', 'group']])

if __name__ == "__main__":
    main()
