"""
Copyright (C) 2023 musicnbrain.org

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

def title(text):
  return {
    'title': [{
      'text': {
        'content': text
      }
    }]
  }

def cover(url):
  return {
    'type': 'external',
    'external': {
      'url': url
    }
  }

def icon(url):
  return {
    'type': 'external',
    'external': {
      'url': url
    }
  }

def heading(text):
  return {
    'object': 'block',
    'type': 'heading_1',
    'heading_1': {
      'rich_text': [{
        'type': 'text',
        'text': {'content': text}
      }]
    }
  }

def paragraph(text):
  return {
    'object': 'block',
    'type': 'paragraph',
    'paragraph': {
      'rich_text': [{
        'type': 'text',
        'text': {'content': text}
      }]
    }
  }

def bulleted_list_item(text, annotations={}):
  return {
    'object': 'block',
    'type': 'bulleted_list_item',
    'bulleted_list_item': {
      'rich_text': [{
        'type': 'text',
        'text': {
          'content': text
        },
        'annotations': annotations
      }],
      'children': []
    }
  }

def database_properties(title, columns):
  properties = {columns[0]: {
    'title': {}
  }}
  for column in columns[1:]:
    properties[column] = {
      'rich_text': {}
    }
  return [{'type': 'text', 'text': {'content': title}}], properties

def line(keys, values):
  properties = {keys[0]: {
    'title': [{'text': {'content': values[0]}}]
  }}
  for index in range(1, len(keys)):
    properties[keys[index]] = {
      'rich_text': [{'text': {'content': values[index]}}]
    }
  return properties