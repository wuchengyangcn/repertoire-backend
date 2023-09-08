import gspread
import pandas as pd
import json
from oauth2client.service_account import ServiceAccountCredentials
from collections import OrderedDict

class jsonData:
    file = ""
    def __init__(self):
        pass
        

    def getData(self, filename): 
        # get credentials
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name("./static/secret_key.json",scopes=scopes)
        file = gspread.authorize(creds)
        event = file.open(filename)
        event_menu = event.sheet1

        # get the first activate sheet
        df_event = pd.DataFrame(event_menu.get_all_records())
        cur_file = ""
        for index, row in df_event.iterrows():
            if row['status'] == "active":
                cur_file = row['file']
                break
        
        # get the data from the activate sheet
        workbook = file.open(cur_file)
        sheet1 = workbook.sheet1
        sheet2 = workbook.get_worksheet(1)
        sheet3 = workbook.get_worksheet(2)

        df1 = pd.DataFrame(sheet1.get_all_records())
        df2 = pd.DataFrame(sheet2.get_all_records())
        df3 = pd.DataFrame(sheet3.get_all_records())
        content = []

        grouped = df1.groupby('performer')

        for performer, group_df in grouped:
            titles = group_df['title'].tolist()
            composers = group_df['composer'].tolist()
            pieces = []
            for title, composer in zip(titles, composers):
                piece_dict = {"title": [title], "composer": [composer]}
                pieces.append(piece_dict)
            performer_dict = {"performer": performer, "pieces": pieces}
            content.append(performer_dict)
        content_json = json.dumps(content)
        
        #add sheet2 data
        front_dict = OrderedDict()
        col2 = df2['Content']
        front_dict['title'] = col2[0]
        front_dict['subtitle'] = col2[1]
        front_dict['time'] = col2[2]
        front_dict['location'] = col2[3]
        front_dict['address'] = col2[4]
        front_dict['background'] = col2[5]
        front_dict_json = json.dumps(front_dict)

        #add sheet3 data
        back_list = []
        icons = df3['icon'].to_list()
        names = df3['name'].to_list()
        for icon, name in zip(icons,names):
            icon_dict = {"icon": icon, "name":name}
            back_list.append(icon_dict)
        back_list_json = json.dumps(back_list)
        

        music_dict = {
            "license notice": [
            "Copyright (C) 2023 musicnbrain.org",
            "This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.",
            "This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.",
            "You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>."
            ],
            "front": front_dict_json,
        "content": content_json,
        "back": back_list_json,
        }
        print(music_dict)

        data = json.dumps(music_dict)
        return data

# test1 = jsonData()
# test1.getData("all events")

    




# update data