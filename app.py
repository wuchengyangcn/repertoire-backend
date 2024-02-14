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
import json


class Booklet:
    def __init__(self):
        self.menu = JsonData()
        self.data = []
        self.fetch_data()
        self.model_config = json.load(open("./static/model_config.json", "r"))

    def fetch_data(self):
        # update visit
        if len(self.data) > 0:
            visits = [page["visit"] for page in self.data]
            self.menu.update_visits(visits)
        # fetch data
        self.data = self.menu.fetch_events()

    def repertoire(self, device, event_id):
        if device is None or device not in self.model_config:
            device = "ip14"
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

        lines_per_page = self.model_config[device]["lines_per_page"]

        html_code = []
        self.data[idx]["visit"] += 1
        front = self.data[idx]["front"]
        content = self.data[idx]["content"]
        back = self.data[idx]["back"]

        # front page
        front_template = self.model_config[device]["front_template"]
        html_code.append(render_template(front_template, data=front))

        # content page
        content_template = self.model_config[device]["content_template"]
        current_page = []
        current_count = 0
        for performer in content:
            lines = (
                len(performer["performer"])
                // self.model_config[device]["performer_characters_per_line"]
                + 1
            )
            for piece in performer["pieces"]:
                lines += max(
                    sum(
                        len(temp)
                        // self.model_config[device]["piece_characters_per_line"]
                        + 1
                        for temp in piece["title"]
                    ),
                    sum(
                        len(temp)
                        // self.model_config[device]["piece_characters_per_line"]
                        + 1
                        for temp in piece["composer"]
                    ),
                )
            lines += self.model_config[device]["performer_offset"]
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
        back_template = self.model_config[device]["back_template"]
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


@scheduler.task("interval", id=None, minutes=10)
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
