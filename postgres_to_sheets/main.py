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

import psycopg2
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from io import BytesIO
import pandas as pd
import datetime
import os

class DatabaseConnection:
    def __init__(self, info):
        self.host = info['host']
        self.database = info['database']
        self.user = info['user']
        self.password = info['password']
        self.connection = None
        self.cursor = None

    def open(self):
        self.connection = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def get(self, table):
        self.open()
        self.cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}';")
        results = self.cursor.fetchall()
        columns = [temp[0] for temp in results[1:]]
        self.cursor.execute(f"SELECT * FROM {table};")
        results = self.cursor.fetchall()
        rows = [list(temp[1:]) for temp in results]
        self.close()
        return columns, rows

    def put(self, table, columns, rows):
        self.open()
        self.cursor.execute(f"DROP TABLE IF EXISTS {table};")
        self.cursor.execute(f"CREATE TABLE {table} (id SERIAL PRIMARY KEY, {' TEXT, '.join(columns)} TEXT);")
        queries = ""
        for row in rows:
            queries += f"INSERT INTO {table} ({', '.join(columns)}) VALUES ("
            for ele in row:
                queries += f"'{ele}', "
            queries = queries[:-2] + "); "
        self.cursor.execute(queries)
        self.connection.commit()
        self.close()

class DriveConnection:
    def __init__(self, token):
        self.token = token
        self.service = None
        self.folder = None
    
    def open(self):
        self.credentials = service_account.Credentials.from_service_account_file(
            self.token,
            scopes=['https://www.googleapis.com/auth/drive']
        )
        self.service = build('drive', 'v3', credentials=self.credentials).files()
        self.folder = self.service.list(q="mimeType='application/vnd.google-apps.folder'").execute()['files'][0]['id']
    
    def get(self, table):
        self.open()
        results = self.service.list(q=f"'{self.folder}' in parents").execute()['files']
        for result in results:
            if result['name'] == f'{table}.xlsx':
                file_id = result['id']
        content = BytesIO()
        downloader = MediaIoBaseDownload(content, self.service.get_media(fileId=file_id))
        done = False
        while not done:
            _, done = downloader.next_chunk()
        df = pd.read_excel(content)
        columns = df.columns.tolist()
        rows = df.values.tolist()
        return columns, rows

    def put(self, table, columns, rows):
        self.open()
        results = self.service.list(q=f"'{self.folder}' in parents").execute()['files']
        for result in results:
            if result['name'] == f'{table}.xlsx':
                self.service.delete(fileId=result['id']).execute()
        data = {}
        for i in range(len(columns)):
            data[columns[i]] = [row[i] for row in rows]
        df = pd.DataFrame(data)
        with pd.ExcelWriter(f'{table}.xlsx', engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)
            worksheet = writer.sheets['Sheet1']
            for i, col in enumerate(df.columns):
                max_len = df[col].astype(str).apply(len).max()
                worksheet.set_column(i, i, max_len * 2)
        metadata = {
            'name': f'{table}.xlsx',
            'parents': [self.folder],
            'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
        media = MediaFileUpload(f'{table}.xlsx')
        self.service.create(body=metadata, media_body=media).execute()
        os.remove(f'{table}.xlsx')

print(datetime.datetime.now())
# columns = ['name', 'composer', 'title']
# rows = [['Allison', 'Minuet in G', 'Christian Petzold'],
#            ['Christy', 'Johann Bach', 'Minute in D minor'],
#            ['Aiden', 'The Animal Band', 'The Animal Band']]
table = 'session1'

database_credentials = {
    'host': 'localhost',
    'database': 'database',
    'user': 'postgres',
    'password': 'secret'
}
database_connection = DatabaseConnection(database_credentials)
# database_connection.put(table, columns, rows)
database_columns, database_rows = database_connection.get(table)
print(database_columns)
print(database_rows)

drive_token = 'token.json'
drive_connection = DriveConnection(drive_token)
drive_connection.put(table, database_columns, database_rows)
drive_columns, drive_rows = drive_connection.get(table)
print(drive_columns)
print(drive_rows)
