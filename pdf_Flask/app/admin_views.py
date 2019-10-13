from app import app
from flask import render_template
import os

import json
from app.myFunc import AdminParser
@app.route("/admin/dashboard")
def admin_dashboard():
    candidates = []
    my_path = os.path.realpath(os.path.dirname(__file__))
    print(os.path.join(my_path, "templates\\Files", "data.txt"))
    with open(os.path.join(my_path, "templates\\Files", "data.txt")) as json_file:
        data = json.load(json_file)
        l = len(data)
        for candidate in data:
            pdfname = candidate[2]
            fullname = candidate[1]
            candidates.append([pdfname, fullname])
    return render_template("admin/dashboard.html", candidates = candidates)

@app.route("/Costumize", methods=['POST'])
def Costumize():
    Parsing = AdminParser.costum()
    forward_message = "Moving Forward..."
    return render_template("admin/dashboard.html", Parsing=Parsing);
