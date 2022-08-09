# RKSOK Project
Данный проект - простая записная книга, позволяющая по имени пользователя записывать данные, просматривать и удалять их.
Для действий с записной книгой необходимо сделать соответвующий запрос на сервер. Сервер использует современный, абсолютно безопасный протокол РКСОК
Запросы автоматически проходят проверку у проверяющих органов. Все Ваши действия будут записаны и могут быть использованы против Вас.

## Installation

Перейдите в папку с проектом:
```sh
cd rksok
```

Создайте виртуальное окружение и активируйте его:
```sh
python3 -m venv env
source env/bin/activate
```

Установите зависимости:
```sh
pip install -r requirements.txt
```

Сервер готов к запуску! 

## Запуск сервера:

```sh
cd rksok
python3.9 server.py
```

## Конфигурация сервера

## Протокол РКСОК

Подробности работы протокола рассмотрены на странице: https://stepik.org/lesson/520994/step/3?auth=login&unit=513512

Примеры комманд:
```sh
ОТДОВАЙ Иван Хмурый РКСОК/1.0
```
(Ищет пользователя в записной книге и возвращает его телефон)

```sh
ЗОПИШИ Иван Хмурый РКСОК/1.0
89012345678
```
(Записывает пользователя и указанный телефон в телефонную книгу)

```sh
УДОЛИ Иван Хмурый РКСОК/1.0
```
(Удаляет указанного пользователя из записной книги)


Ответ, начинающийся с "НОРМАЛДЫКС" означает успешное выполнение запрошенной команде.
Ответ, начинающийся с "НИЛЬЗЯ" означает что команда была запрещена контролирующими органами. 

## Клиент

Вы можете воспользоваться клиентом для использования записной книги от Алексея Голобурдина:
```sh
cd rksok/client
python3.9 rksok_client.py
```


