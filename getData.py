import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from collections import OrderedDict


class JsonData:
    def __init__(self):
        # get credentials
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name("./static/secret_key.json", scopes=scopes)
        self.file = None
        self.data = []

    def update_visits(self, visits):
        self.file = gspread.authorize(self.creds)
        event = self.file.open("all_events")
        event_menu = event.sheet1
        for idx in range(len(visits)):
            event_menu.update_cell(idx + 2, 5, visits[idx])

    def fetch_events(self):
        self.file = gspread.authorize(self.creds)
        self.data = []
        event = self.file.open("all_events")
        event_menu = event.sheet1

        # fetch all sheets
        df_event = pd.DataFrame(event_menu.get_all_records())
        for index, row in df_event.iterrows():
            event_data = self.fetch_event(row["file"])
            event_data["status"] = row["status"]
            event_data["visit"] = row["visit"]
            self.data.append(event_data)
        return self.data

    def fetch_event(self, name):
        # fetch sheet
        workbook = self.file.open(name)
        sheet1 = workbook.sheet1
        sheet2 = workbook.get_worksheet(1)
        sheet3 = workbook.get_worksheet(2)

        df1 = pd.DataFrame(sheet1.get_all_records())
        df2 = pd.DataFrame(sheet2.get_all_records())
        df3 = pd.DataFrame(sheet3.get_all_records())
        content = []

        grouped = df1.groupby("performer")

        for performer, group_df in grouped:
            titles = group_df["title"].tolist()
            composers = group_df["composer"].tolist()
            pieces = []
            for title, composer in zip(titles, composers):
                piece_dict = {"title": [title], "composer": [composer]}
                pieces.append(piece_dict)
            performer_dict = {"performer": performer, "pieces": pieces}
            content.append(performer_dict)

        # add sheet2 data
        front = OrderedDict()
        col2 = df2["content"]
        front["title"] = col2[0]
        front["subtitle"] = col2[1]
        front["time"] = col2[2]
        front["location"] = col2[3]
        front["address"] = col2[4]
        front["background"] = col2[5]

        # add sheet3 data
        back = []
        icons = df3["icon"].to_list()
        names = df3["name"].to_list()
        for icon, name in zip(icons, names):
            icon_dict = {"icon": icon, "name": name}
            back.append(icon_dict)

        data = {
            "front": front,
            "content": content,
            "back": back,
        }
        return data
