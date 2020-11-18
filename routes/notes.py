from flask import *
from flask import current_app as app
from main import cache
import controllers.file_controller as file_controller
import os


@app.route("/", defaults={"req_path": ""})
@app.route("/<path:req_path>")
@app.route("/<path:req_path>/")
@cache.memoize(60 * 60 * 24 * 7) #1 week cache, wow
def homepage(req_path):
    if req_path == "":
        return render_template("index.html")
    
    exists, is_file, path_obj = file_controller.path_exists(req_path)

    if not exists:
        abort(404)
    
    if not is_file:
        return render_template("directory.html", files=file_controller.get_ls(path_obj))
    else:
        return render_template("note.html", content=file_controller.get_content(path_obj), file=path_obj)