from flask import *
from flask import current_app as app
from main import cache
import controllers.file_controller as file_controller
import os

@app.route("/webhook")
def webhook():
    if request.args.get("token") != os.environ["webhook_token"]:
        abort(403)
        
    file_controller.download_and_unzip_source()
    cache.clear()
    
    return "OK"