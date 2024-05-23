from flask import Flask, Response
from datetime import datetime
from threading import Thread

from src.communication import DbContext
from src.model.BuildInstructionDto import BuildInstructionDto
from src.services.RecognitionService import RecognitionService
from src.common.ConfigProperties import ConfigProperties
from src.services.ValidationService import ValidationService

config = ConfigProperties()
app = Flask(__name__)
timer: datetime = None


@app.route('/<int:result_id>/result')
def get_result(result_id):
    global timer
    db = DbContext.SQLiteDB(ConfigProperties.DATABASE_NAME)
    if timer is None:
        timer = datetime.now()

    if result_id > 3:
        return 'Keine weitere Bausinstruktion, Bauvorgang abgeschlossen.', 208  # HTTP-Statuscode "Already Reported"

    max_result_id = db.get_max_id()
    print(f"Currently {max_result_id} results are persisted")

    if result_id > max_result_id:
        return 'Warten bis nächste Scanetappe abgeschlossen ist...', 204  # HTTP-Statuscode "No Content"
    
    instructions = RecognitionService.get_build_instructions_from_db(result_id, db)
    print(f"Currently a total of {len(instructions)} instruction steps exist")

    # TODO-go: Is this check neeeded? Will this condition ever be reached?
    if len(instructions) < result_id:
        return 'Warte bis nächste Bauinstruktion vorhanden ist', 204  # HTTP-Statuscode "No Content"

    # Konvertiere jedes Objekt zu einem JSON-String und fasse diese in einer Liste zusammen
    json_strings = [instruction.to_json() for instruction in instructions[result_id - 1]]

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
    thread = Thread(target=ValidationService.send_to_validation_server(duration))
    thread.start()
    timer = None  # Zurücksetzen der Startzeit für den nächsten Lauf
    return str(duration)


@app.route('/start')
def start():

    # TODO-go: Fix multithreading when starting
    thread = Thread(target=RecognitionService.analyze_turntable_video_stream())
    thread.start()
    return 'Done', 200


@app.route('/test')
def test():
    
    RecognitionService.test_fill_with_static_data_variation_a()
    
    # Erstelle eine Liste von BuildInstructionDto Objekten

    instructions = [
        BuildInstructionDto(1, 2),
        BuildInstructionDto(3, 1),
        BuildInstructionDto(5, 3)
    ]

    # Konvertiere jedes Objekt zu einem JSON-String und fasse diese in einer Liste zusammen
    json_strings = [instruction.to_json() for instruction in instructions]

    # Füge die JSON-Strings zu einem Gesamt-JSON-Array zusammen
    json_array_string = '[' + ', '.join(json_strings) + ']'

    # Setze den Content-Type der Antwort auf 'application/json'
    return Response(json_array_string, mimetype='application/json')


@app.route('/reset')
def reset():
    db = DbContext.SQLiteDB(ConfigProperties.DATABASE_NAME)
    db.reset_table()
    db.close()

    global timer
    timer = None

    return 'Done', 200


if __name__ == '__main__':
    # Starte den Flask Webserver
    app.run(debug=True, host='0.0.0.0', port=config.DEPLOY_PORT)
