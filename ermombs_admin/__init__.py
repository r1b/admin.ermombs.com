import os
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import FileUploadField, ImageUploadField
from flask_sqlalchemy import SQLAlchemy


# -----------------------------------------------------------------------------


app = Flask(__name__, static_folder=os.environ['STATIC_ROOT'])


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

    def __repr__(self):
        return self.title


class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dimensions = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.Text, nullable=False)
    materials = db.Column(db.Text, nullable=False)
    slug = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    series_id = db.Column(db.Integer, db.ForeignKey(Series.id))
    series = db.relationship(Series, backref=db.backref('works'))

    def __repr__(self):
        return self.title


# -----------------------------------------------------------------------------

class MyImageUploadField(ImageUploadField):
    # Hack around OSError when uploading GIF
    keep_image_formats = ('PNG', 'GIF',)


class InfoModelView(ModelView):
    form_args = {
        'cv_filename': {
            'base_path': app.config['STATIC_ROOT'],
        },
        'featured_image_filename': {
            'base_path': app.config['STATIC_ROOT'],
        }
    }
    form_overrides = {
        'cv_filename': FileUploadField,
        'featured_image_filename': MyImageUploadField,
    }


class SeriesModelView(ModelView):
    form_args = {
        'featured_image_filename': {
            'base_path': app.config['STATIC_ROOT'],
        }
    }
    form_overrides = {
        'featured_image_filename': MyImageUploadField,
    }


class WorkModelView(ModelView):
    form_args = {
        'image_filename': {
            'base_path': app.config['STATIC_ROOT'],
        }
    }
    form_overrides = {
        'image_filename': MyImageUploadField,
    }


InfoView = InfoModelView(Info, db.session)
SeriesView = SeriesModelView(Series, db.session)
WorkView = WorkModelView(Work, db.session)


# -----------------------------------------------------------------------------


admin = Admin(name='ermombs.com admin', template_mode='bootstrap3', url='/')


admin.add_view(InfoView)
admin.add_view(SeriesView)
admin.add_view(WorkView)


admin.init_app(app)
