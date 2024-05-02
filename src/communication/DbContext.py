import sqlite3
import string

from typing import List
from src.model.CubePart import CubePart


class SQLiteDB:
    def __init__(self, db_path):
        """Initialisiert die Verbindung zur SQLite-Datenbank."""
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_schema()

    def get_cursor(self):
        return self.cursor

    def select(self, query: string, params=()):
        """
            Führt einen SELECT-Befehl aus und gibt das Ergebnis zurück.
            ergebnis = db.select('SELECT * FROM meine_tabelle')
        """
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def get_recognition_by_id(self, record_id: int) -> dict:
        """
        Gibt einen Datensatz anhand der ID von der Recognition Tabelle zurück.
        Die Rückgabe ist ein Dictionary mit dem Spaltennamen als Key und dem Wert als Value.

        :param record_id: Die ID des Datensatzes, der abgerufen werden soll.
        :return: Ein Dictionary mit den Spaltennamen als Schlüsseln und den entsprechenden Werten oder None, falls kein Datensatz gefunden wurde.
        """
        query = "SELECT * FROM Recognition WHERE id = ?"
        self.cursor.execute(query, (record_id,))
        result = self.cursor.fetchone()

        if result:
            columns = [description[0] for description in self.cursor.description]
            return dict(zip(columns, result))
        else:
            return None
        
    def get_recognitions_by_max_id(self, max_record_id: int) -> List[dict]:
        if max_record_id > 3:
            max_record_id = 3

        query = "SELECT * FROM Recognition LIMIT ?"
        self.cursor.execute(query, (max_record_id,))
        results = self.cursor.fetchall()

        if len(results) > 0:
            recognition_results = []
            for result in results:
                columns = [description[0] for description in self.cursor.description]
                recognition_results.append(dict(zip(columns, result)))
            return recognition_results
        else:
            return []

    def get_max_id(self) -> int:
        query = "SELECT MAX(id) FROM Recognition"
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def recognition_exists(self, record_id: int) -> bool:
        """
        Überprüft, ob ein Eintrag mit der angegebenen ID in der Recognition Tabelle existiert.

        :param record_id: Die ID des Datensatzes, der überprüft werden soll.
        :return: True, wenn der Eintrag existiert, sonst False.
        """
        query = "SELECT EXISTS(SELECT 1 FROM Recognition WHERE id = ?)"
        self.cursor.execute(query, (record_id,))
        result = self.cursor.fetchone()
        return result[0] == 1

    def __insert(self, table: string, data):
        """
            Fügt Daten in eine bestimmte Tabelle ein.
            'data' sollte ein Dictionary sein, das die Spaltennamen und Werte enthält.
            db.insert('meine_tabelle', {'spalte1': 'Wert1', 'spalte2': 'Wert2'})
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        query = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        self.cursor.execute(query, tuple(data.values()))
        self.connection.commit()

    def insert_cube_part(self, cubePart: CubePart):
        self.__insert("Recognition", cubePart.to_key_value_pair())

    def reset_table(self):
        """
            Löscht alle Einträge aus der Recognition Tabelle.
            db.reset_table()
        """
        self.cursor.execute(f'DELETE FROM Recognition')
        self.connection.commit()

    def create_schema(self):
        """
        Erstellt das Schema für die Datenbank.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Recognition (
                id INTEGER PRIMARY KEY,
                pos1 INTEGER NULL,
                pos2 INTEGER NULL,
                pos3 INTEGER NULL,
                pos4 INTEGER NULL,
                pos5 INTEGER NULL,
                pos6 INTEGER NULL,
                pos7 INTEGER NULL,
                pos8 INTEGER NULL
            )
        ''')
        self.connection.commit()

    def close(self):
        """Schließt die Verbindung zur Datenbank."""
        self.connection.close()
