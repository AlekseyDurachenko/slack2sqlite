# (English) slack2sqlite

This utility saves the message history from the slack.com into the database SQLite.
The first time you are downloading the whole message history.
On the next start only new messages are added into the database.

## The backup contains the following objects:
- TUser - user list
  - TUser:id - unique user ID
  - TUser:name - display name of the user
  - TUser:color - color of the user
  - TUser:json - full json object associated with the user
- TChannel - channel list
  - TChannel:id - unique channel ID
  - TChannel:name - display name of the channel
  - TChannel:archived - 1, if channel is archived
  - TChannel:json - full json object associated with the channel
- TMessage - message history
  - TMessage:TChannelId - unique channel ID
  - TMessage:type - message type
  - TMessage:subtype - message subtype (it may be empty)
  - TMessage:user - unique user ID (it may be empty)
  - TMessage:ts - unique time stamp
  - TMessage:text - message text (it may be empty)
  - TMessage:json - full json object associated with the message

## Changelog
### v0.1.1
- migrate from getopt to argparse

### v0.1.0
- initial version

## Usage:

```bash
usage: slack2sqlite.py [-h] [--version] [--verbose]
                       [--access-token ACCESS_TOKEN]
                       [--output-database OUTPUT_DATABASE]

This utility saves the message history from the slack.com into the database
SQLite. The first time you are downloading the whole message history. On the
next start only new messages are added into the database.

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --verbose             show debug information
  --access-token ACCESS_TOKEN
                        slack access token
  --output-database OUTPUT_DATABASE
                        sqlite database file
```
- access_token - can be found here: https://api.slack.com/web

## Tips
- To run the script periodically you can add it to your crontab.


# (Русский) slack2sqlite

Данная утилита сохраняет историю сообщений slack.com в базу данных SQLite.
При первом запуске производится загрузка всей истории. 
При последующих запусках в базу данных добавляются лишь новые сообщения.

## Резервная копия содержит следующие объекты:
- TUser - список пользователей
  - TUser:id - уникальный идентификатор пользователя
  - TUser:name - отображаемое имя пользователя
  - TUser:color - цвет пользователя
  - TUser:json - полный json объект ассоциированный с пользователем
- TChannel - список каналов
  - TChannel:id - уникальный идентификатор канала
  - TChannel:name - отображаемое имя канала
  - TChannel:archived - 1, если канал архивный
  - TChannel:json - полный json объект ассоциированный с каналом
- TMessage - история сообщений
  - TMessage:TChannelId - уникальный идентификатор канала
  - TMessage:type - тип сообщения
  - TMessage:subtype - подтип сообщения (может быть пустым)
  - TMessage:user - уникальный идентификатор пользователя (может быть пустым)
  - TMessage:ts - уникальная метка времени
  - TMessage:text - текст сообщения (может быть пустым)
  - TMessage:json - полный json объект ассоциированный с сообщением

## История изменений
### v0.1.1
- миграция с getopt на argparse

### v0.1.0
- первоначальная версия

## Использование:
```bash
usage: slack2sqlite.py [-h] [--version] [--verbose]
                       [--access-token ACCESS_TOKEN]
                       [--output-database OUTPUT_DATABASE]

This utility saves the message history from the slack.com into the database
SQLite. The first time you are downloading the whole message history. On the
next start only new messages are added into the database.

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --verbose             show debug information
  --access-token ACCESS_TOKEN
                        slack access token
  --output-database OUTPUT_DATABASE
                        sqlite database file
```
- access_token - получить можно здесь: https://api.slack.com/web

## Советы
- Для периодического запуска скрипта можно добавить его в crontab.
