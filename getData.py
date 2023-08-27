import gspread
import pandas as pd
import json
from oauth2client.service_account import ServiceAccountCredentials

class jsonData:
    file = ""
    def __init__(self):
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name("/Users/effiezhang/mobilewebsite-1/static/secret_key.json",scopes=scopes)
        jsonData.file = gspread.authorize(creds)

    def getData(self, filename): 
        workbook = jsonData.file.open(filename)
        sheet = workbook.sheet1

        # print(sheet.row_values(2))
        df = pd.DataFrame(sheet.get_all_records())
        content = []

        # 按照performer列进行分组
        grouped = df.groupby('performer')

        # 遍历每个分组
        for performer, group_df in grouped:
        # 获取当前分组的所有标题和作曲家
            titles = group_df['title'].tolist()
            composers = group_df['composer'].tolist()
            pieces = []
            for title, composer in zip(titles, composers):
                piece_dict = {"title": [title], "composer": [composer]}
                pieces.append(piece_dict)
            performer_dict = {"performer": performer, "pieces": pieces}
            content.append(performer_dict)

        music_dict = {
            "license notice": [
            "Copyright (C) 2023 musicnbrain.org",
            "This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.",
            "This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.",
            "You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>."
            ],
            "front": {
            "title": "A PIANO RECITAL",
            "subtitle": "featuring students of Miranda Shum",
            "time": "SUNDAY, APRIL 23, 2023 | 2:00 PM",
            "location": "Tateuchi Hall, Community School of Music and Arts",
            "address": "230 San Antonio Circle, Mountain View CA 94040"
            },
        "content": content
        }

        data = json.dumps(music_dict)
        return data

    




# update data