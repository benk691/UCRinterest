import flask, flask.views
import os
from flask import (Flask, request, url_for, redirect, render_template, flash,
                   session, g, send_from_directory)
from flaskext.uploads import (UploadSet, configure_uploads, IMAGES,
                              UploadNotAllowed)
from flask.ext.wtf import Form, files
from werkzeug import secure_filename
UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
class Upload(flask.views.MethodView):
    def get(self):
        return flask.render_template('upload.html')

    def post(self):
        def allowed_file(filename):
            return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
        file = request.files['photo']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("Image has been uploaded.")
            return redirect(url_for('upload', filename=filename))
        return flask.redirect(flask.url_for('upload'))
