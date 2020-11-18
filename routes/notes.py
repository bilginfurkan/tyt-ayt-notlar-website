from flask import *
from flask import current_app as app
from main import cache
import controllers.file_controller as file_controller
import controllers.md_controller as md_controller
import os


@app.route("/", defaults={"req_path": ""})
@app.route("/<path:req_path>", strict_slashes=False)
@cache.memoize(60 * 60 * 24 * 7) #1 week cache, wow
def homepage(req_path):
    if req_path == "":
        return render_template("index.html")
    exists, path_obj = file_controller.path_exists(req_path)

    if not exists:
        abort(404)
    
    if not path_obj.is_file():
        return render_template("directory.html", files=file_controller.get_ls(path_obj))
    elif path_obj.is_image():
        return send_file(path_obj.original)
    else:
        return render_template("note.html", content=file_controller.get_content(path_obj), file=path_obj, process_md=md_controller.process_md)



@app.route("/medya/<path:req_path>")
def return_media(req_path):
    print(req_path)
    media = file_controller.get_media(req_path)
    if media is None:
        abort(404)

    return send_file(media.original)