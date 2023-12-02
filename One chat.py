import pandas as pd
from telethon.sync import TelegramClient

api_id = 'можно узнать на https://my.telegram.org/'
api_hash = 'можно узнать на https://my.telegram.org/'
phone = 'номер на который зарегестрирован акк'

def main():
    client = TelegramClient(phone, api_id, api_hash)
    client.connect()
    
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Введите код: '))

    print(client.get_me())

    chat = 'ссылка на чат, в котором производится поиск'

    # Получение списка участников группы
    participants = client.get_participants(chat)

    # Создание DataFrame с информацией об участниках
    df_users = pd.DataFrame([{'id': participant.id, 'first_name': participant.first_name, 'last_name': participant.last_name} for participant in participants])

    # Ввод никнейма участника для поиска
    username_to_search = input("Введите никнейм участника: ")

    # Поиск участника по никнейму
    user_row = df_users[df_users['first_name'] == username_to_search]
    
    if user_row.empty:
        print("Участник не найден.")
        return

    user_id = user_row.iloc[0]['id']

    # Ввод ключевого слова для поиска сообщений
    keyword_to_search = input("Введите ключевое слово для поиска сообщений: ")

    # Получение последних сообщений в чате
    messages = client.get_messages(chat, limit=100)

    # Фильтрация сообщений по участнику и ключевому слову
    filtered_messages = [message.text for message in messages if message.sender_id == user_id and keyword_to_search.lower() in message.text.lower()]

    if not filtered_messages:
        print("Сообщений не найдено.")
        return

    # Вывод найденных сообщений
    for message_text in filtered_messages:
        print(message_text)

if __name__ == "__main__":
    main()
