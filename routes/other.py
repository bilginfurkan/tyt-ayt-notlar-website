from flask import *
from flask import current_app as app


@app.errorhandler(404)
def error_404(exc):
    return render_template("error.html", content="Bu sayfa bulunamadı."), 404


@app.errorhandler(403)
def error_404(exc):
    return render_template("error.html", content="Bu sayfaya girmeniz mümkün değil :'("), 403


@app.errorhandler(500)
def error_500(exc):
    return render_template("error.html", content="Sunucu hatası! Bir süre sonra tekrar deneyin."), 500