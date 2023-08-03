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
from json import load


class Booklet:
    def __init__(self, path):
        data = load(open(path, "r"))
        self.front = data["front"]
        self.content = data["content"]

    def repertoire(self, device):
        html_code = []
        if device is None:
            device = "mobile"
        if device == "mobile":
            lines_per_page = 15
        else:
            lines_per_page = 13

        front_template = f"repertoire_front_{device}.html"
        html_code.append(render_template(front_template, data=self.front))

        content_template = f"repertoire_content_{device}.html"
        current_page = []
        current_count = 0
        for performer in range(len(self.content)):
            lines = 0
            for piece in self.content[performer]["pieces"]:
                lines += max(len(piece["title"]), len(piece["composer"]))
            lines += 2
            if current_count + lines > lines_per_page:
                html_code.append(render_template(content_template, data=current_page))
                current_page = []
                current_count = 0
            current_page.append(self.content[performer])
            current_count += lines
        if len(current_page) > 0:
            html_code.append(render_template(content_template, data=current_page))

        return jsonify(html_code)


app = Flask(__name__, static_url_path="")
CORS(app)
booklet = Booklet("./static/data.json")


@app.route('/repertoire/')
def repertoire():  # put application's code here
    device = request.args.get("device")
    return booklet.repertoire(device)


if __name__ == '__main__':
    app.run()
