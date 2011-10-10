#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
import data
app = Flask(__name__)
data.init()

@app.route("/")
def hello():
    print "Hello"
    return render_template('main.html')

@app.route("/list")
def list():
    print "List"
    return render_template('list.html', projects = data.retrieve_projects()[1])

@app.route("/techniques")
def techniques():
    print "Techniques"
    return render_template('main.html')

@app.route("/project/<int:id>")
def show_project():
    return render_template('main.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
