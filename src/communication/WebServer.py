from flask import Flask, Response
from datetime import datetime
from threading import Thread

from typing import List
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

    instructions = get_build_instructions_from_db(result_id, db)

    if instructions.count < result_id:
        return 'Warten bis nächste Scanetappe abgeschlossen ist...', 204  # HTTP-Statuscode "No Content"

    # Konvertiere jedes Objekt zu einem JSON-String und fasse diese in einer Liste zusammen
    json_strings = [instruction.to_json() for instruction in get_build_instructions_from_db(result_id, db)]

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
    db = DbContext.SQLiteDB(ConfigProperties.DATABASE_NAME)
    db.reset_table()
    db.close()

    global timer
    timer = None

    return 'Done', 200


def get_build_instructions_from_db(element_id: int, db_context: DbContext.SQLiteDB) -> List[List[BuildInstructionDto]]:
    recognition_results = db_context.get_recognitions_by_max_id(element_id)
    instructions_list = []

    built_pattern = [
        None, None, None, None,
        None, None, None, None,
    ]

    built_pattern_debug = [
        None, None, None, None,
        None, None, None, None,
    ]

    recognized_pattern = [
        None, None, None, None,
        None, None, None, None,
    ]

    recognized_pattern_debug = [
        None, None, None, None,
        None, None, None, None,
    ]

    # Alle instruktionen werden nach aktuellem Stand rekonstruiert
    for recognition_result in recognition_results:
        instructions = []
        for pos, color in recognition_result.items():
            if pos == 'id':  # Überspringen der id-Spalte
                continue
            if color is not None:
                position = int(pos.replace("pos", ""))
                pos = position - 1

                # Check if this cube is recognized for the first time   
                if recognized_pattern[pos] is None:
                    print("Cube at pos", pos, "detected")
                    recognized_pattern[pos] = BuildInstructionDto(position, int(color))
                    recognized_pattern_debug[pos] = color
                        
                    # Check if lower layer
                    if position < 5:
                        built_pattern[pos] = recognized_pattern[pos]
                        built_pattern_debug[pos] = color
                        instructions.append(built_pattern[pos])

                        # If it fills overhang then also append the overhang to the instruction
                        if recognized_pattern[pos + 4] is not None:
                            built_pattern[pos + 4] = recognized_pattern[pos + 4]
                            built_pattern_debug[pos + 4] = color
                            instructions.append(built_pattern[pos + 4])

                    # Check if lower layer was built to place upper
                    elif built_pattern[pos - 4] is not None:
                        built_pattern[pos] = recognized_pattern[pos]
                        built_pattern_debug[pos] = color
                        instructions.append(built_pattern[pos])

        print("Recog pattern:", recognized_pattern_debug)
        print("Built pattern:", built_pattern_debug)

        instructions_list.append(instructions)

    # TODO-go: Usefull/needed?
    # Überprüfen, ob alle Positionsspalten nicht NULL sind
    # all_positions_filled = all(value is not None for key, value in current_result.items() if key.startswith('pos'))

    return instructions_list


if __name__ == '__main__':
    # Starte den Flask Webserver
    app.run(debug=True, host='0.0.0.0', port=config.DEPLOY_PORT)
