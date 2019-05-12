import os
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy


# -----------------------------------------------------------------------------


app = Flask(__name__)


app.config['DATABASE_FILE'] = os.environ['DATABASE_FILE']
app.config['FLASK_ADMIN_SWATCH'] = 'paper'
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['STATIC_ROOT'] = os.environ['STATIC_ROOT']


# -----------------------------------------------------------------------------


db = SQLAlchemy(app)


class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cv_filename = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    featured_image_filename = db.Column(db.Text, nullable=False)
    featured_text = db.Column(db.Text, default='')


class Series(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    featured_image_filename = db.Column(db.Text, nullable=False)
    featured_text = db.Column(db.Text, default='')
    slug = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)


class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dimensions = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.Text, nullable=False)
    materials = db.Column(db.Text, nullable=False)
    series = db.Column(db.Integer, db.ForeignKey(Series.id))
    slug = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)


# -----------------------------------------------------------------------------

InfoView = ModelView(Info, db.session)
SeriesView = ModelView(Series, db.session)
WorkView = ModelView(Work, db.session)


# -----------------------------------------------------------------------------


admin = Admin(name='ermombs.com admin', template_mode='bootstrap3')


admin.add_view(FileAdmin(app.config['STATIC_ROOT'], '/static/', name='Static Files'))
admin.add_view(InfoView)
admin.add_view(SeriesView)
admin.add_view(WorkView)


admin.init_app(app)
