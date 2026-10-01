from ..main import main
from flask import url_for,flash,render_template

@main.app_errorhandler(404)
def page_not_found(e):
    flash('Sorry Page Not Found','danger')
    return render_template('base.html'),404

@main.app_errorhandler(403)
def forbidden(e):
    flash('Your not Allowed to navigate this page','danger')
    return render_template('base.html'),403

@main.app_errorhandler(500)
def server_error(e):
    flash('server under maintainance','danger')
    return render_template('base.html'),500

@main.app_errorhandler(401)
def unauthorized(e):
    flash('Anauthorized personel','danger')
    return render_template('base.html'),401
