#!/usr/bin/env python
# encoding: utf-8
from main import app
from main import db
from main import bcrypt
from main import lm

from flask import render_template


@app.route('/', methods=['GET', 'POST'])
def info():
    return render_template('info.html')
