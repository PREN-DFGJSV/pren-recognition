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

    def to_key_value_pair(self):
        return {
            1: int(self.pos1) if self.pos1.isdigit() else 0,
            2: int(self.pos2) if self.pos2.isdigit() else 0,
            3: int(self.pos3) if self.pos3.isdigit() else 0,
            4: int(self.pos4) if self.pos4.isdigit() else 0,
            5: int(self.pos5) if self.pos5.isdigit() else 0,
            6: int(self.pos6) if self.pos6.isdigit() else 0,
            7: int(self.pos7) if self.pos7.isdigit() else 0,
            8: int(self.pos8) if self.pos8.isdigit() else 0
        }
