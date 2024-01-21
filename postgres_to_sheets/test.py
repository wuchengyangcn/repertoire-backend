"""
Copyright (C) 2024 musicnbrain.org

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import unittest
from main import DatabaseConnection, DriveConnection
import warnings
warnings.filterwarnings("ignore")


class TestConnection(unittest.TestCase):
    def setUp(self):
        database_credentials = {
            'host': 'localhost',
            'database': 'database',
            'user': 'postgres',
            'password': 'secret'
            }
        self.database = DatabaseConnection(database_credentials)

        drive_token = 'token.json'
        self.drive = DriveConnection(drive_token)

    def test_database(self):
        columns = ['name', 'composer', 'title']
        rows = [['Allison', 'Minuet in G', 'Christian Petzold'],
                ['Christy', 'Johann Bach', 'Minute in D minor'],
                ['Aiden', 'The Animal Band', 'The Animal Band']]
        table = 'session1'
        self.database.put(table, columns, rows)
        database_columns, database_rows = self.database.get(table)
        self.assertEqual(columns, database_columns)
        self.assertEqual(rows, database_rows)
    
    def test_drive(self):
        columns = ['name', 'composer', 'title']
        rows = [['Allison', 'Minuet in G', 'Christian Petzold'],
                ['Christy', 'Johann Bach', 'Minute in D minor'],
                ['Aiden', 'The Animal Band', 'The Animal Band']]
        table = 'session1'
        self.drive.put(table, columns, rows)
        drive_columns, drive_rows = self.drive.get(table)
        self.assertEqual(columns, drive_columns)
        self.assertEqual(rows, drive_rows)


if __name__ == '__main__':
    unittest.main()
