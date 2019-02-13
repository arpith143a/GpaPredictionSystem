import app
from app.model import db
from passlib.apps import custom_app_context as pwd_context

import os
from flask import Flask, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    fos = db.Column(db.String(64), nullable=False)
    picture_url = db.Column(db.String(64), nullable=True)

    def __init__(self, name, username, email, fos, password=None):
        self.name = name
        self.username = username
        self.email = email
        if password:
            self.password_hash = pwd_context.encrypt(password)
        self.fos = fos

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        """verifies password.
        :password: String, plain text password, will be compared with
                   self.password_hash.
        :returns: True if password is correct, otherwise False.
        """
        return pwd_context.verify(password, self.password_hash)

    def upload_photo(self, app, request, upload_folder="app/static"):
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
            # if file and allowed_file(file.filename):
            if file:
                filename = secure_filename(file.filename)
                path = os.path.join(upload_folder, str(self.id)+".png")
                file.save(path)
                self.picture_url = str(self.id)+".png"
                # return redirect("login.html")

