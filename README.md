<!--
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
-->

# Repertoire Backend

> Serving HTML pages with Flask and Jinja2 templates

### Dependencies

- Python
- Flask
- Flask CORS
- Jinja2
- gspread
- oauth2client
- PyOpenSSL

### Project Structure

```
├── app.py
├── static
│   └── data.json
└── templates
    ├── repertoire_content_desktop.html
    ├── repertoire_content_mobile.html
    ├── repertoire_front_desktop.html
    └── repertoire_front_mobile.html
```

### Run

```
$ python -m flask run
```

### Build docker image

```
docker build -t musicnbrain/repertoire-backend .
```

### Run docker image

```
docker run -d -p 5001:5001 --name repertoire-backend musicnbrain/repertoire-backend
```
