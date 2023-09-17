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

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from getData import JsonData
from flask_apscheduler import APScheduler


class Booklet:
    def __init__(self):
        self.menu = JsonData()
        self.data = []
        self.fetch_data()

    def fetch_data(self):
        # fetch data
        self.data = self.menu.fetch_events()

    def repertoire(self, device, event_id):
        if event_id is None:
            idx = -1
        else:
            idx = int(event_id) - 1
        if idx < 0 or idx >= len(self.data):
            # find the last active event
            idx = -1
            for temp in range(len(self.data) - 1, -1, -1):
                if self.data[temp]["status"] == "active":
                    idx = temp
                    break
            if idx == -1:
                idx = len(self.data) - 1

        # line limit for each page
        if device is None:
            device = "mobile"
        if device == "mobile":
            lines_per_page = 14
        else:
            device = "desktop"
            lines_per_page = 13

        html_code = []
        front = self.data[idx]["front"]
        content = self.data[idx]["content"]
        back = self.data[idx]["back"]

        # front page
        front_template = f"repertoire_front_{device}.html"
        html_code.append(render_template(front_template, data=front))

        # content page
        content_template = f"repertoire_content_{device}.html"
        current_page = []
        current_count = 0
        for performer in content:
            lines = 0
            # count number of lines
            for piece in performer["pieces"]:
                lines += max(len(piece["title"]), len(piece["composer"]))
            if device == "mobile":
                lines += 3
            else:
                lines += 3
            if current_count + lines > lines_per_page:
                # generate a new content page
                html_code.append(render_template(content_template, data=current_page))
                current_page = []
                current_count = 0
            current_page.append(performer)
            current_count += lines
        # last page
        if len(current_page) > 0:
            html_code.append(render_template(content_template, data=current_page))

        # icons at the end
        back_template = f"repertoire_back_{device}.html"
        for sponsor in back:
            html_code.append(render_template(back_template, data=sponsor))

        return jsonify(html_code)


class Config(object):
    SCHEDULER_API_ENABLED = True


booklet = Booklet()
scheduler = APScheduler()
app = Flask(__name__, static_url_path="")
CORS(app)
app.config.from_object(Config())
scheduler.init_app(app)
scheduler.start()


@scheduler.task('interval', id=None, minutes=10)
def fetch_job():
    booklet.fetch_data()


@app.route("/repertoire/")
def repertoire():
    # device type
    device_type = request.args.get("device")
    event_id = request.args.get("id")
    return booklet.repertoire(device_type, event_id)


if __name__ == "__main__":
    app.run(port=5001)
