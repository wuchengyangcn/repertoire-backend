from notion_client import Client
import json
from helper import *

# connect to notion
with open('./notion_token.json', 'r') as f:
    notion_token = json.load(f)['notion_token']
notion = Client(auth=notion_token)

# prerequisites
# 1. create connection in notion workspace
# 2. create main page in notion workspace
# 3. add connection to main page in notion workspace

# search for connected main page
page_name = 'excel_to_notion'
parent_page_id = notion.search(query=page_name)['results'][0]['id']

# create child page under parent page
child_page = notion.pages.create(
    parent={'page_id': parent_page_id},
    properties=title('2/26 MusicNBrain Festival Program (Session 1-3)'),
    cover=cover('https://assets-global.website-files.com/6011e54d155cc9428daebbdd/6375ae7f5b8d277ea441c033_Rental_concerthalll.jpeg'),
    icon=icon('https://assets-global.website-files.com/6011e54d61042f6e5b8cee51/601c2c98f19e7b25abe89daf_LOGO%20green%20and%20yellow%20250x250.png'),
)
child_page_id = child_page['id']

# database template
def insert_database(parent_id, name, columns, rows):
    metadata = database_properties(name, columns)
    database = notion.databases.create(
        parent={'page_id': parent_id},
        is_inline=True,
        title=metadata[0],
        properties=metadata[1],
    )
    database_id = database['id']
    for row in rows:
        notion.pages.create(
            parent={'database_id': database_id},
            properties=line(columns, row),
        )

children = []
children.append(heading('2/26 MusicNBrain Festival Program (Session 1-3)'))
children.append(paragraph('Note: P1-G1-S1 means you are the first performer in Group 1 at Session 1'))
children.append(paragraph('C1-G1-S2 means you are the first contestant in Group 1 at Session 2'))

parent_1 = bulleted_list_item('Session 1', annotations={'bold': True})
child_1 = bulleted_list_item('Group 1: 9:45am PST')
child_2 = bulleted_list_item('Group 2: 10:30am PST')
parent_1['bulleted_list_item']['children'].append(child_1)
parent_1['bulleted_list_item']['children'].append(child_2)
children.append(parent_1)

parent_2 = bulleted_list_item('Session 2: Draw for the final order', annotations={'bold': True})
child_3 = bulleted_list_item('Group 1: 12:45pm PST')
child_4 = bulleted_list_item('Group 2: 1:40pm PST')
parent_2['bulleted_list_item']['children'].append(child_3)
parent_2['bulleted_list_item']['children'].append(child_4)
children.append(parent_2)

parent_3 = bulleted_list_item('Session 3: Draw for the final order', annotations={'bold': True})
child_5 = bulleted_list_item('Group 1: 3pm PST')
child_6 = bulleted_list_item('Group 2: 4pm PST')
parent_3['bulleted_list_item']['children'].append(child_5)
parent_3['bulleted_list_item']['children'].append(child_6)
children.append(parent_3)

blocks = notion.blocks.children.append(block_id=child_page_id, children=children)
columns = ['Name', 'Title of piece', 'Composer']
rows = [
    ['Allison', 'Christian Petzold', 'Minuet in G'],
    ['Bosco', '(1) I love mountains. (2) March Militaire', 'Franz Schubert'],
    ['Aiden', 'The Animal Band', 'The Animal Band'],
    ['Christy', 'Minute in D minor', 'Johann Bach'],
    ['Jiayu', 'Spanish Caballero', 'Manuel Fernández Caballero']
]
title = 'Session 1 (10am-12pm) All Ages'

insert_database(child_page_id, title, columns, rows)
children = []
children.append(paragraph('(*) means performance only, not for competition'))
children.append(paragraph('C1-G1-S2 means you are the first contestant in Group 1 at Session 2'))
blocks = notion.blocks.children.append(block_id=child_page_id, children=children)

insert_database(child_page_id, title, columns, rows)
children = []
children.append(paragraph('(*) means performance only, not for competition'))
children.append(paragraph('C1-G1-S2 means you are the first contestant in Group 1 at Session 2'))
blocks = notion.blocks.children.append(block_id=child_page_id, children=children)

insert_database(child_page_id, title, columns, rows)
children = []
children.append(paragraph('(*) means performance only, not for competition'))
children.append(paragraph('C1-G1-S2 means you are the first contestant in Group 1 at Session 2'))
blocks = notion.blocks.children.append(block_id=child_page_id, children=children)
