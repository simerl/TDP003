#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
import data
app = Flask(__name__)
data.init()

@app.route("/")
def hello():
    print "Hejllo"
    return render_template('main.html')

@app.route("/list")
def list():
    print "List"
    return render_template('list.html', projects = data.retrieve_projects()[1])

@app.route("/techniques")
def techniques():
    print "Techniques"
    return render_template('techniques.html', techniques = data.retrieve_techniques()[1], tech_stats = data.retrieve_technique_stats()[1], descr = data.retrieve_projects()[1])

@app.route("/project/<int:post_id>")
def show_project(post_id):
    return render_template('project_id.html', project = data.lookup_project(post_id)[1])

@app.route("/search", methods=['GET'])
def search():
    adv_search_string = request.args.get('adv_search')
    search_string = request.args.get('search')
    sort_by = request.args.get('sort_by')
    result = []
    if search_string:
        search_string = search_string.encode('ascii')
        result = data.retrieve_projects(sort_by='start_date', sort_order='asc', techniques=None, search=search_string, search_fields=['project_name', 'techniques_used', 'course_name'])[1]
    if adv_search_string:
        adv_search_string = adv_search_string.encode('ascii')

        result = data.retrieve_projects(sort_by='start_date', sort_order='asc', techniques=None, search=adv_search_string, search_fields=['project_name', 'techniques_used', 'course_name'])[1]
    return render_template('search.html', search = result)

if __name__ == "__main__":
    app.debug = True
    app.run()
