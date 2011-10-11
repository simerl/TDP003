#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

import locale                                                           #Imports locale, will be used to sort lists containing unicode strings
locale.setlocale(locale.LC_ALL, "sv_SE.UTF-8")                          #Sets locale to utf-8 swedish

tech_list = []
project_list = []								                                #Creates a global list which will be used to store the lines of the csv file
errorcode = 1								                            #Sets the error code to "error accessing data file" because no data is loaded

def init():
    global project_list
    global errorcode

    csvReader = csv.DictReader(open('data.csv', 'rb'), delimiter=',')	#Reads from csv file
    
    for row in csvReader:
        row2 = {}							                            #Creates an empty dict
        for key, value in row.iteritems():
            row2[unicode(key, 'utf-8')] = unicode(value,'utf-8')	    #Puts the current row in the dict and converts it to unicode
        if row2['project_name'] and row2['project_no']:
            project_list.append(row2)						                        #Adds the dict to the list "project_list"

    for i in range(len(project_list)):						                   
        project_list[i]["project_no"] = int((project_list[i]["project_no"]))            #Converts project_no back from unicode string to integer
        project_list[i]["group_size"] = int((project_list[i]["group_size"]))            #Does the same with group_size
    
    for i in range(len(project_list)):						                    #Converts techniques_used to list then sort it using swedish locale
        if len(project_list[i]["techniques_used"]) > 0:                                                              
            temp = project_list[i]["techniques_used"]                        
            project_list[i]["techniques_used"] = temp.split(',')
            project_list[i]["techniques_used"] = sorted(project_list[i]["techniques_used"], cmp=locale.strcoll)
        else:
            project_list[i]["techniques_used"] = []
        
    errorcode = 0							                            #Changes the error code to "Ok"

    return project_list								                            #Returns project_list


def project_count():

    return (errorcode, len(project_list))										#Returns the error code and the length of project_list as a tuple

def lookup_project(a):                                                  

    for proj in project_list:                                                   #Iterates through the list of projects.
    	if a == proj['project_no']:                                             
			return (errorcode, proj)                                            #If input matches project_no the project dict is returned 

    return (2, None)                                                            #If no project is found errorcode 2 is returned. 

def retrieve_projects(sort_by='start_date', sort_order='asc', techniques=None, search=None, search_fields=None):

    sorted_list = []                                                            #Declares local variables
    tech_list = []
    search_list = []

    if techniques:                                                              #Puts all the used techniques matching input in tech_list
        for proj in project_list:
            for x in techniques:
                if x in proj['techniques_used']:
                    
                    if proj not in tech_list:                                   #kex for duplicates
                        tech_list.append(proj)

    else:                                                                       #If no input, all techniques are added to tech_list
        tech_list = project_list

    if search and search_fields:                                                #Check search and search_fields input
        search = unicode(search, 'utf-8')                                       #Converts search to unicode 
        search = search.lower()                                                 #Converts to lower case, will make it easier to search
        
        for proj in tech_list:
            
            for y in search_fields: 
               
                search_list.append(proj[y])
                
                        
            for i in range(len(search_list)):
                search_list[i] = unicode(search_list[i])
            
            search_list = [element.lower() for element in search_list]

            for a in search_list:
                
                if search in a:
                    
                                                    
                    sorted_list.append(proj)
            
            search_list = []

    elif search_fields == []:
        sorted_list = []    
            
    else:
        sorted_list = tech_list

 

    sorted_list = sorted(sorted_list, key=lambda k: k[sort_by])

    if sort_order == 'desc':                                                    #Set sort order, asc or desc
        sorted_list.reverse()

    return (errorcode, sorted_list)

def retrieve_techniques():
    create_tech_list()

    return (errorcode, tech_list)

def create_tech_list():
    global tech_list

    for proj in project_list:
        for tech in proj['techniques_used']:
            if tech not in tech_list:
                tech_list.append(tech)

    tech_list = sorted(tech_list)
    return tech_list

def retrieve_technique_stats():
    create_tech_list()
    tech_list_all = []
    tech_count = []
    dict_keys = [u'count', u'name', u'projects', u'id', u'name']
    tech_stats = []
    projects = []
    temp_projects = []
    for proj in project_list:
        for tech in proj['techniques_used']:
            tech_list_all.append(tech)

    for tech in tech_list:
        tech_count.append(tech_list_all.count(tech))
        
    for i in range(len(tech_list)):
        for proj in project_list:
            if tech_list[i] in proj['techniques_used']:
                temp_projects.append({u'id':proj['project_no'], u'name':proj['project_name']})
        temp_projects = sorted(temp_projects, key=lambda k: k['name'])       
        if temp_projects:
            projects.append(temp_projects)
            temp_projects = []
   
    for i in range(len(tech_list)):
        stats = dict(zip(dict_keys[0:3], [tech_count[i], tech_list[i], projects[i]]))
        tech_stats.append(stats)        

    return (errorcode, tech_stats)
