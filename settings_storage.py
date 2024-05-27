import sqlite3
from datetime import datetime

class SettingsStorage:
    def __init__(self, db_name='settings.db'):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()

        # Create the tables if they don't exist
        self.c.execute('''CREATE TABLE IF NOT EXISTS brightness
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, value REAL, date_of_creation TEXT)''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS contrast
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, value REAL, date_of_creation TEXT)''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS sound_output
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, value TEXT, date_of_creation TEXT)''')

    def insert_record(self, table_name, value):
        # Get the current date and time
        date_of_creation = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Check if the table has reached the limit of 10 records
        self.c.execute(f'SELECT COUNT(*) FROM {table_name}')
        count = self.c.fetchone()[0]
        if count >= 10:
            # Delete the record with the smallest id (oldest record)
            self.c.execute(f'DELETE FROM {table_name} WHERE id = (SELECT id FROM {table_name} ORDER BY id ASC LIMIT 1)')

        # Insert the new record
        if table_name == 'sound_output':
            self.c.execute(f'INSERT INTO {table_name} (value, date_of_creation) VALUES (?, ?)', (value, date_of_creation))
        else:
            self.c.execute(f'INSERT INTO {table_name} (value, date_of_creation) VALUES (?, ?)', (float(value), date_of_creation))

        self.conn.commit()

    def __del__(self):
        self.conn.close()

# Example usage
settings_storage = SettingsStorage()
settings_storage.insert_record('brightness', 75.5)
settings_storage.insert_record('contrast', 60.2)
settings_storage.insert_record('sound_output', 'Speakers')
