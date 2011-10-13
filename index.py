#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
import data
import logging

app = Flask(__name__)

logfile = 'index.log'   #creates log file
def logger(msg):            #logging function, recieve message and print in log file
    logging.basicConfig(filename = logfile, level = logging.INFO)
    logging.info(msg)

def reload_init():      #reloads data.init() when called from other function
    data.init()
    logger('###data.init() reloaded')       #sends message to logging function

data.init()                     #loads data.init() when server starts 
logger('###data.init() loaded')


@app.route("/")
def hello():                #loads main page
    reload_init()           #calls reload function
    logger('###Main page visited')
    return render_template('main_content.html')         #renders main content



@app.route("/techniques")
def techniques():                       #opens techniques page
    reload_init()
    logger('###Techniques page visited')
    return render_template('techniques.html', techniques = data.retrieve_techniques()[1], tech_stats = data.retrieve_technique_stats()[1], descr = data.retrieve_projects()[1])         #renders techniques.html and gives it the variables 'techniques' and 'tech_stats' from the data.py file

@app.route("/project/<int:post_id>")        #post_id is the project number, can only be integer
def show_project(post_id):
    reload_init()
    if data.lookup_project(post_id)[0] == 0:            #kex err code
        logger('###Project ' + str(post_id) + ' visited')       #sends log message with post id if it exists
        return render_template('project_id.html', project = data.lookup_project(post_id)[1])        #renders the requested page
    else:
        logger('###Nonexistent project visited')            #sends err message to the log if nonexistent project
        return render_template('project_id.html', error = "Project not found")      #err msg to user

@app.route("/list", methods=['GET'])        #specifies form method GET
def search():
    reload_init()
    logger("###Visited project list")
    result = []                             #clear results
    form_techniques_used = []
    form_search_fields = [] 
    adv_search_string = request.args.get('adv_search')
    search_string = request.args.get('search')
    form_sort_by = request.args.get('sort_by')
    form_sort_order = request.args.get('sort_order')

    # ^ inserts information from THEform into lists

    if not request.args.get('sort_by'):         #if input is None, default values will be set
        form_sort_by = 'start_date'

    if not request.args.get('sort_order'):       #if input is None, default values will be set
        form_sort_order = 'asc'

    for tech in data.create_tech_list():            #adds matching techniques
        if request.args.get(tech):
            form_techniques_used.append(request.args.get(tech))

    if not form_techniques_used:                     #if input is empty list, default value None will be set
        form_techniques_used = None 
    

    if request.args.get('project_name'):            #adds matching project name
        form_search_fields.append(request.args.get('project_name'))

    if request.args.get('course_name'):             #^course name
        form_search_fields.append(request.args.get('course_name'))

    if not request.args.get('project_name') and not request.args.get('course_name'):         #if input is None, default values will be set
        form_search_fields = ['project_name', 'course_name']

    if adv_search_string:       #converts search string to ascii if it exists
        adv_search_string = adv_search_string.encode('utf-8')
    
        result = data.retrieve_projects(sort_by=form_sort_by, sort_order=form_sort_order, techniques=form_techniques_used, search=adv_search_string, search_fields=form_search_fields)[1]       #sets result with included search string

    else:
        result = data.retrieve_projects(techniques=form_techniques_used, sort_order=form_sort_order, sort_by=form_sort_by)[1]       #sets result without search string
    logger('###Searched for ' + str(adv_search_string))     #sends msg to log with search string, can be None

    if not result:
        logger('###Search was unsuccessful')        #if on match, send other log message 
        result = 'No matching projects'                 #user message if no match

    return render_template('search.html', search = result, tech_list = data.create_tech_list())     #renders page with search result in variable search
   

 

if __name__ == "__main__":
    app.debug = True
    app.run()
