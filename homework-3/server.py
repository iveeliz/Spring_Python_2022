import json
import time
from datetime import datetime
from flask import Flask, request, abort

app = Flask(__name__)

db = []


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/status")
def status():
    dt_now = datetime.now()
    users = []

    for message in db:
        if message['name'] not in set(users) and message['name'] != 'Anonymous':
            users.append(message['name'])

    current_status = {
        'Текущее время': dt_now,
        'Пользователи, которые сейчас находятся в чате': users,
        'Количество пользователейв в чате': len(users),
        'Количество сообщений в данный момент': len(db),
    }

    return json.dumps(current_status)


@app.route("/send", methods=['POST'])
def send_message():
    data = request.json

    if not isinstance(data, dict):
        return abort(400)
    # if set(data.keys()) != {'name', 'text'}:
    #     return abort(400)

    if 'name' not in data or 'text' not in data:
        return abort(400)
    if len(data) != 2:
        return abort(400)

    name = data['name']
    text = data['text']

    if not isinstance(name, str) or \
            not isinstance(text, str) or \
            name == '' or \
            text == '':
        return abort(400)

    message = {
        'time': time.time(),
        'name': name,
        'text': text,
    }
    db.append(message)

    # Bot

    if message['text'] == '/start':
        message = {
            'time': time.time(),
            'name': 'Bot',
            'text': 'Привет! Если хочешь продолжить анонимно, перед каждым новым сообщением ставь знак *\n'
                    'Hello! If you want to continue anonymously, put a * sign before each new message\n\n'
                    'Выбери свой язык\n'
                    'Choose your language\n\n'
                    'English language: /english\n'
                    'Русский язык: /русский\n'

        }
        db.append(message)

    elif message['text'] == '/english':
        message = {
            'time': time.time(),
            'name': 'Bot',
            'text': 'I will help you get acquainted with the weather in Moscow!\n'
                    'Enter one of the following commands to check the weather: \n\n'
                    'Weather today: /now\n'
                    'Weather for the week: /week\n'
        }
        db.append(message)

    elif message['text'] == '/русский':
        message = {
            'time': time.time(),
            'name': 'Бот',
            'text': 'Я помогу тебе ознакомиться с погодой в Москве!\n'
                    'Введи одну из следующих команд, чтобы узнать погоду: \n\n'
                    'Погода сейчас: /сейчас\n'
                    'Погода на неделю: /неделя\n'
        }
        db.append(message)

    elif message['text'] == '/now':
        message = {
            'time': time.time(),
            'name': 'Bot',
            'text': 'I will help you to know the weather!\n'
                    'Available at the link: https://www.gismeteo.ru/weather-moscow-4368/now/\n'
        }
        db.append(message)

    elif message['text'] == '/сейчас':
        message = {
            'time': time.time(),
            'name': 'Бот',
            'text': 'Можно ознакомиться по ссылке: https://www.gismeteo.ru/weather-moscow-4368/now/\n'
        }
        db.append(message)

    elif message['text'] == '/week':
        message = {
            'time': time.time(),
            'name': 'Bot',
            'text': 'I will help you to know the weather!\n'
                    'Available at the link: https://www.gismeteo.ru/weather-moscow-4368/weekly/\n'
        }
        db.append(message)

    elif message['text'] == '/неделя':
        message = {
            'time': time.time(),
            'name': 'Бот',
            'text': 'Можно ознакомиться по ссылке: https://www.gismeteo.ru/weather-moscow-4368/weekly/\n'
        }
        db.append(message)

    else:
        db.append(message)

    return {'ok': True}


@app.route("/messages")
def get_messages():
    try:
        after = float(request.args['after'])

    except:
        return abort(400)

    db_after = []

    for message in db:

        if message['time'] > after:
            db_after.append(message)
            if len(db_after) >= 100:
                break

            # Анонимный пользователь:

            if message['text'][0] == '*':
                message['name'] = 'Anonymous'
                message['text'] = message['text'][1:]

    return {'messages': db_after}


app.run()
