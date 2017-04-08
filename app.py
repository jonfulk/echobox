#!/usr/bin/env python

#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from uuid import uuid4

from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
# @app.teardown_request
# def shutdown_session(exception=None):
#     db_session.remove()


class Echo(db.Model):
    __tablename__ = 'echoes'

    pk = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Unicode, nullable=False)
    url = db.Column(db.Unicode, unique=True, index=True)

    def __init__(self, message):
        self.message = message
        self.url = self.generate_url()

    def generate_url(self):
        maybe_url = unicode(uuid4().hex[:12])
        if Echo.query.filter_by(url=maybe_url).first():
            return self.generate_url()
        else:
            return maybe_url

    @property
    def permalink(self):
        return url_for('echo', url=self.url, _external=True)


#----------------------------------------------------------------------------#
# Views.
#----------------------------------------------------------------------------#
@app.route('/', methods=['GET', 'POST'])
def home():
    """Post route for creating an echo."""
    if request.method == 'POST':
        item = Echo(request.form['message'])
        db.session.add(item)
        db.session.commit()
        return redirect(item.permalink)
    else:
        echoes = Echo.query.all()
        return render_template('pages/home.html', echoes=echoes)


@app.route('/echoes')
def view_all():
    """Display all echoes"""
    echoes = Echo.query.all()
    return render_template('pages/echoes.html', echoes=echoes)


@app.route('/echoes/<url>')
def echo(url):
    """Return individual echo by ID"""
    echo = Echo.query.filter_by(url=url).first_or_404()
    echoes = Echo.query.all()
    return render_template('/pages/echo.html', echo=echo, echoes=echoes)


@app.route('/echoes/delete/<url>')
def delete(url):
    """Delete a specific echo and update total"""
    echo = Echo.query.filter_by(url=url).first()
    if echo:
        db.session.delete(echo)
        db.session.commit()
        echoes = Echo.query.count()
        return jsonify({'success': True, 'echoes': echoes})
    else:
        return jsonify({'success': False})


# Error handlers
@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    db.create_all()
    app.run()
