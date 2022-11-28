# Attendance-record-bot    "Бот учёта посещаемости"
Телеграмм бот для учета посещаемости группы
 
http://t.me/MyFirstUnusualbot
____
Использование
===========
Возможные варианты использования:
- Учет посещаемости группы
- Учет успеваемости группы (для бальной системы)
- Др. варианты 
____
Структура проекта
========
- core.py - Ядро для взаимодейстия драйвера БД и бота
- sqlite3_db_driver.py - драйвер для БД SQLite3
- text_messages.py - Тексты сообщений, которыми бот будет отвечать пользователю
- telegram_front.py - Оболочка взаимодейстия ядра и бота Telegram
- settings.py - Файл с токеном бота (импортируется в core.py, в репозиторий не залит)
____
Технологии
===========
При работе дома используется библиотека БД sqlite3

Библиотека для взаимодействия с Telegram - aiogram

Библиотека для логгирования - logging
____
Интерфейс пользователя:
===========

>
>После нажатия кнопки /start бот предлагает несколько вариантов действий.
Команда старт отличается у зарегистрированного пользователя и незарегистрированного
- У незарегистрированного:
  ><img src='Pictures/7.png'/>
- У зарегистрированного:
  ><img src='Pictures/8.png'/>

Общие команды:
===========
- Команда "Вход авторизует пользователя и создает таблицу в БД"

  ><img src="Pictures/2.png"/>

- >Команда "Все пропуски" возвращает пользователю список пропусков или баллов группы     

  ><img src="Pictures/3.png"/>

- >Команда "Показать ID" возвращает список уникальных номеров студентов группы и их имена/

  ><img src="Pictures/4.png"/>

- >Команда "Команды бота" возращает пользователю длинное сообщение с описанием возможных команд

- >Команда "Мой ID" возращает ID пользователя. ID пользователя поможет решить тех.проблемы, если такие возникнут

- >Вывод всех таблиц в БД

  ><img src='Pictures/16.png'/>

Команды добавления и обновления:
===========
- >Добавление новых студентов производится в следующем порядке:

  ><img src="Pictures/5.png"/>

- >Показ последних обновлений в БД:

  ><img src='Pictures/6.png'/>

Сортировка изменений:
===========
- >Вывод изменений после определённой даты:

  ><img src='Pictures/9.png'/>

- >Вывод изменений до определённой даты:

  ><img src='Pictures/10.png'/>

- >Вывод изменений в определённый период между двумя датами:

  ><img src='Pictures/11.png'/>

Команды удаления и обнуления:
===========
- >Удаление записи о студенте в таблице БД:

  ><img src='Pictures/12.png'/>

- >Обнуление пропусков одного студента

  ><img src='Pictures/13.png'/>

- >Очистка базы данных кроме таблицы chat_id (iD пользователя -> имя группы) осуществляется командой /clear_all_database и введением особого пароля:

  ><img src='Pictures/14.png'/>

- >Удаление отдельной таблицы,например, с именем 'aboba'

  ><img src='Pictures/15.png'/>

- >Очистка файла логов, также с паролем:

  ><img src='Pictures/18.png'/>
