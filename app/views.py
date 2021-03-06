from app import app

from flask import render_template, request

from .routes.mainSite import mainSite
from .routes.CMS import CMS

app.register_blueprint(mainSite)
app.register_blueprint(CMS)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500
