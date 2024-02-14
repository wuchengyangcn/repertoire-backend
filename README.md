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
- pandas
- Flask-APScheduler
- google-api-python-client
- google-auth-httplib2
- google-auth-oauthlib
- openpyxl
- xlsxwriter

### Project Structure

```
├── app.py
├── static
│   ├── data.json
│   └── model_config.json
└── templates
    ├── ip14_front.html
    ├── ip14_content.html
    ├── ip14_back.html
    ├── ip14pro_front.html
    ├── ip14pro_content.html
    ├── ip14pro_back.html
    ├── ip14promax_front.html
    ├── ip14promax_content.html
    ├── ip14promax_back.html
    ├── mobile_front.html
    ├── mobile_content.html
    └── mobile_back.html
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

### Deploy

```
./build.sh
```

### CI/CD

```
{ crontab -l; echo "0 * * * * ~/repertoire-backend/sync.sh"; } | crontab -
```
