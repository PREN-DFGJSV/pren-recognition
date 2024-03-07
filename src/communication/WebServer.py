from flask import Flask
from datetime import datetime

app = Flask(__name__)

timer: datetime = None


@app.route('/start')
def start():
    global timer
    time = datetime.now()
    return 'start'


@app.route('/result/<int:result_id')
def get_result(result_id):
    return f'ID {result_id}'


@app.route('/end')
def end():
    global timer
    if timer is None:
        return 'Error', 400
    end_time = datetime.now()
    duration = end_time - timer
    timer_start = None  # Zurücksetzen der Startzeit für den nächsten Lauf
    return 'end'


def reset():
    return 'reset'
