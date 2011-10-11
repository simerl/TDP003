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

@app.route("/listold")
def list():
    print "List"
    return render_template('list.html', projects = data.retrieve_projects()[1])

@app.route("/techniques")
def techniques():
    print "Techniques"
    return render_template('techniques.html', techniques = data.retrieve_techniques()[1], tech_stats = data.retrieve_technique_stats()[1], descr = data.retrieve_projects()[1])

@app.route("/project/<int:post_id>")
def show_project(post_id):
    if data.lookup_project(post_id)[0] == 0:
        return render_template('project_id.html', project = data.lookup_project(post_id)[1])
    else:
        return render_template('project_id.html', error = "Project not found")

@app.route("/list", methods=['GET'])
def search():


    form_techniques_used = []
    form_search_fields = [] 
    adv_search_string = request.args.get('adv_search')
    search_string = request.args.get('search')
    form_sort_by = request.args.get('sort_by')
    form_sort_order = request.args.get('sort_order')
    if not request.args.get('sort_by'): 
        form_sort_by = 'start_date'
    if not request.args.get('sort_order'):
        form_sort_order = 'asc'
    for tech in data.create_tech_list():
        if request.args.get(tech):
            form_techniques_used.append(request.args.get(tech))
    if not form_techniques_used:
        form_techniques_used = None
    result = []

    if request.args.get('project_name'):
        form_search_fields.append(request.args.get('project_name'))

    if request.args.get('course_name'):
        form_search_fields.append(request.args.get('course_name'))

    if not request.args.get('project_name') and not request.args.get('course_name'):
        form_search_fields = ['project_name', 'course_name']

   

    



    if adv_search_string:
        adv_search_string = adv_search_string.encode('ascii')
    
        result = data.retrieve_projects(sort_by=form_sort_by, sort_order=form_sort_order, techniques=form_techniques_used, search=adv_search_string, search_fields=form_search_fields)[1]
    else:
        result = data.retrieve_projects(techniques=form_techniques_used, sort_order=form_sort_order, sort_by=form_sort_by)[1]

    if not result:
        result = 'No matching projects'
    return render_template('search.html', search = result, tech_list = data.create_tech_list())
    
     
  
if __name__ == "__main__":
    app.debug = True
    app.run()
