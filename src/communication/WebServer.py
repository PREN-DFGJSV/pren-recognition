from flask import Flask, Response
from datetime import datetime

from src.model.BuildInstructionDto import BuildInstructionDto

app = Flask(__name__)

timer: datetime = None


@app.route('/start')
def start():
    global timer
    time = datetime.now()
    return 'start'


@app.route('/result/<int:result_id>')
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


@app.route('/test')
def test():
    # Erstelle eine Liste von BuildInstructionDto Objekten
    instructions = [
        BuildInstructionDto(1, 2, False),
        BuildInstructionDto(3, 4, True)
    ]

    # Konvertiere jedes Objekt zu einem JSON-String und fasse diese in einer Liste zusammen
    json_strings = [instruction.to_json() for instruction in instructions]

    # Füge die JSON-Strings zu einem Gesamt-JSON-Array zusammen
    json_array_string = '[' + ', '.join(json_strings) + ']'

    # Setze den Content-Type der Antwort auf 'application/json'
    return Response(json_array_string, mimetype='application/json')


def reset():
    return 'reset'


# Definiere die main Methode
if __name__ == '__main__':
    # Starte den Flask Webserver
    app.run(debug=True, host='0.0.0.0', port=5000)

