import json
import string


class Cube:
    def __int__(self, pos1: string = '', pos2: string = '', pos3: string = '', pos4: string = '', pos5: string = '',
                pos6: string = '', pos7: string = '', pos8: string = ''):
        self.pos1: string = pos1
        self.pos2: string = pos2
        self.pos3: string = pos3
        self.pos4: string = pos4
        self.pos5: string = pos5
        self.pos6: string = pos6
        self.pos7: string = pos7
        self.pos8: string = pos8

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
