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
from json import loads
from getData import jsonData


class Booklet:
    def __init__(self):
        # read data
        # data = load(open(path, "r"))
        # self.front = data["front"]
        # self.content = data["content"]
        # self.back = data["back"]
        self.menu_data = jsonData()

    def repertoire(self, device):
        # read data
        data = loads(self.menu_data.getData("Music-menu"))
        self.front = data["front"]
        self.content = data["content"]
        self.back = data["back"]

        # line limit for each page
        html_code = []
        if device is None:
            device = "mobile"
        if device == "mobile":
            lines_per_page = 14
        else:
            lines_per_page = 13

        # front page
        front_template = f"repertoire_front_{device}.html"
        html_code.append(render_template(front_template, data=self.front))

        content_template = f"repertoire_content_{device}.html"
        current_page = []
        current_count = 0
        for performer in self.content:
            lines = 0
            # count number of lines
            for piece in performer["pieces"]:
                lines += max(len(piece["title"]), len(piece["composer"]))
            lines += 2
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
        for sponsor in self.back:
            html_code.append(render_template(back_template, data=sponsor))

        return jsonify(html_code)


app = Flask(__name__, static_url_path="")
CORS(app)
booklet = Booklet()


@app.route("/repertoire/")
def repertoire():
    # device type
    device = request.args.get("device")
    return booklet.repertoire(device)


if __name__ == "__main__":
    app.run()
