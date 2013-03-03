import os
import flask, flask.views
from flask import (Flask, request, url_for, redirect, render_template, flash,
                   session, g, send_from_directory)
from flask.ext.uploads import (UploadSet, configure_uploads, IMAGES,
                              UploadNotAllowed)
from flask.ext.wtf import Form, files
from werkzeug import secure_filename

class Upload(flask.views.MethodView):
    def get(self):
        return flask.render_template('upload.html')

    def post(self):
        def allowed_file(filename):
            return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
        file = request.files['photo']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            ### Put Photo in DB
            
            flash("Image has been uploaded.")
            return redirect(url_for('upload', filename=filename))
        return flask.redirect(flask.url_for('upload'))
