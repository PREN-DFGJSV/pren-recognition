from flask import Flask, Response
from datetime import datetime
from threading import Thread

from src.communication import DbContext
from src.model.BuildInstructionDto import BuildInstructionDto
from src.services.RecognitionService import RecognitionService

app = Flask(__name__)

timer: datetime = None


@app.route('/<int:result_id>/result')
def get_result(result_id):
    global timer
    db = DbContext.SQLiteDB("results.db")
    if timer is None:
        timer = datetime.now()

    if not db.recognition_exists(result_id):
        return 'Warten bis nächste Scanetappe abgeschlossen ist...', 204  # HTTP-Statuscode "No Content"

    # Konvertiere jedes Objekt zu einem JSON-String und fasse diese in einer Liste zusammen
    json_strings = [instruction.to_json() for instruction in get_buildinstructions_from_db(result_id, db)]

    # Füge die JSON-Strings zu einem Gesamt-JSON-Array zusammen
    json_array_string = '[' + ', '.join(json_strings) + ']'

    db.close()

    # Setze den Content-Type der Antwort auf 'application/json'
    return Response(json_array_string, mimetype='application/json')


@app.route('/duration')
def end():
    global timer
    if timer is None:
        return 'Error', 400
    end_time = datetime.now()
    duration = end_time - timer
    timer = None  # Zurücksetzen der Startzeit für den nächsten Lauf
    return str(duration)

@app.route('/start')
def start():
    thread = Thread(target=RecognitionService.analyze_turntable_video_stream())
    thread.start()
    return 'Done', 200
    
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


@app.route('/reset')
def reset():
    db = DbContext.SQLiteDB("results.db")
    db.reset_table()
    db.close()

    global timer
    timer = None

    return 'Done', 200


def get_buildinstructions_from_db(element_id: int, db_context: DbContext.SQLiteDB) -> list:
    current_result = db_context.get_recognition_by_id(element_id)
    instructions = []

    # Überprüfen, ob alle Positionsspalten nicht NULL sind
    all_positions_filled = all(value is not None for key, value in current_result.items() if key.startswith('pos'))

    # Behandlung des Falls, wenn die ID 1 ist
    if element_id == 1:
        for pos, color in current_result.items():
            if pos == 'id':  # Überspringen der id-Spalte
                continue
            if color is not None:
                position = int(pos.replace("pos", ""))
                instructions.append(BuildInstructionDto(position, int(color), all_positions_filled))
        return instructions

    previous_result = db_context.get_recognition_by_id(element_id - 1)

    # Nur durchführen, wenn sowohl das aktuelle als auch das vorherige Ergebnis existieren
    if current_result and previous_result:
        for pos, current_color in current_result.items():
            if pos == 'id':  # Überspringen der id-Spalte
                continue
            previous_color = previous_result.get(pos)
            # Prüfen, ob sich der Wert geändert hat
            if current_color != previous_color:
                position = int(pos.replace("pos", ""))
                instructions.append(BuildInstructionDto(position, int(current_color), all_positions_filled))

    return instructions


if __name__ == '__main__':
    # Starte den Flask Webserver
    app.run(debug=True, host='0.0.0.0', port=5000)

