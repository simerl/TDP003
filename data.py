#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

import locale                                                           #Imports locale, will be used to sort lists containing unicode strings
locale.setlocale(locale.LC_ALL, "sv_SE.UTF-8")                          #Sets locale to utf-8 swedish

tech_list = []
project_list = []							#Creates a global list which will be used to store the lines of the csv file
errorcode = 1								#Sets the error code to "error accessing data file" because no data is loaded

def init():
    global project_list
    global errorcode
    project_list = []

    csvReader = csv.DictReader(open('data.csv', 'rb'), delimiter=',')	#Reads from csv file using "," as a splitter
    
    for row in csvReader:
        row2 = {}							 #Creates an empty dict to store each project in
        for key, value in row.iteritems():
            row2[unicode(key, 'utf-8')] = unicode(value,'utf-8')	   	#Puts the current row in the dict and converts it to unicode
        if row2['project_name'] and row2['project_no']:
            project_list.append(row2)						#Adds the dict to the list "project_list", if project_name or project_no is empty, no project will be added

    for i in range(len(project_list)):						                   
        project_list[i]["project_no"] = int((project_list[i]["project_no"]))    #Converts project_no back from unicode string to integer
        project_list[i]["group_size"] = int((project_list[i]["group_size"]))    #Does the same with group_size
    
    for i in range(len(project_list)):						#Converts techniques_used to list then sort it using swedish locale
        if len(project_list[i]["techniques_used"]) > 0:                                                              
            temp = project_list[i]["techniques_used"]                        
            project_list[i]["techniques_used"] = temp.split(',')
            project_list[i]["techniques_used"] = sorted(project_list[i]["techniques_used"], cmp=locale.strcoll)
        else:
            project_list[i]["techniques_used"] = []
        
    errorcode = 0				#Changes the error code to "Ok"

    return project_list				#Returns project_list


def project_count():

    return (errorcode, len(project_list))	#Returns the error code and the length of project_list as a tuple

def lookup_project(a):                                                  

    for proj in project_list:                   #Iterates through the list of projects.
    	if a == proj['project_no']:                                             
			return (errorcode, proj)#If input matches project_no the project dict is returned 

    return (2, None)                            #If no project is found errorcode 2 is returned. 

def retrieve_projects(sort_by='start_date', sort_order='asc', techniques=None, search=None, search_fields=None):

    sorted_list = []                            #Declares local variables
    tech_list = []
    search_list = []

    if techniques:                              #Puts all the used techniques matching input in tech_list
        for proj in project_list:
            for x in techniques:
                if x in proj['techniques_used']:
                    
                    if proj not in tech_list:   #Checks for duplicates
                        tech_list.append(proj)

    else:                                       #If no input, all techniques are added to tech_list
        tech_list = project_list

    if search and search_fields:                #Check search and search_fields input
        if search != unicode(search, 'utf-8'):
            search = unicode(search, 'utf-8')       #Converts search to unicode 
        search = search.lower()                  #Converts to lower case, will make it easier to search
        
        for proj in tech_list:			#Adds projects to search_list for each element in search_fields
            for y in search_fields: 
                search_list.append(proj[y])
                     
            for i in range(len(search_list)):			#Encodes all the elements in search_list to unicode
                search_list[i] = unicode(search_list[i])	
            
            search_list = [element.lower() for element in search_list]	#Converts all elements to lowercase.

            for a in search_list:		#Checks if the search word is in search_list, the list with all found projects
                if search in a:                               
                    sorted_list.append(proj)	#Adds it to the list of search is in search_list 
            search_list = []

    elif search_fields == []:			#If search_fields is empty, set sortec_list to empty
        sorted_list = []    
            
    else:
        sorted_list = tech_list			#If none of the other criterias are fulfilled, set sorted_list to tech_list

    sorted_list = sorted(sorted_list, key=lambda k: k[sort_by]) 	#Sort sorted_list after the key "sort_by" chosen by the user

    if sort_order == 'desc':                    #Set sort order, asc or desc
        sorted_list.reverse()			#If sort_order is "desc", reverse the list before returning it

    return (errorcode, sorted_list)

def retrieve_techniques():
    create_tech_list()			#Uses the create_tech_list function to create a list of techniques
    return (errorcode, tech_list)

def create_tech_list():
    global tech_list
    tech_list = []

    for proj in project_list:			#Checks for all techniques in techniques_used
        for tech in proj['techniques_used']:
            if tech not in tech_list:		#Adds them to tech_list if it doesnt exist in the list yet
                tech_list.append(tech)

    tech_list = sorted(tech_list)		#Sorts the list
    return tech_list

def retrieve_technique_stats():
    create_tech_list()			#Fetches the list of all techniques thought create_tech_list()
    tech_list_all = []			#Keeps track of ALL occurrances of the techniques
    tech_count = []			#Counts how many times each technique is found
    dict_keys = [u'count', u'name', u'projects', u'id', u'name']	#Creates a list with the keys needed for the tech stats
    tech_stats = []			#The list containing each dict for each technique
    projects = []			#The list containing all the projects using the techniques
    temp_projects = []			#List to save the projects containing a techniques
    
    for proj in project_list:			#Adds all occurances of the techniques to tech_list_all
        for tech in proj['techniques_used']:
            tech_list_all.append(tech)

    for tech in tech_list:			#Counts the number of occurances of the techniques
        tech_count.append(tech_list_all.count(tech))
        
    for i in range(len(tech_list)):			#Checks all the projects to see which techniques is being used
        for proj in project_list:
            if tech_list[i] in proj['techniques_used']:
                temp_projects.append({u'id':proj['project_no'], u'name':proj['project_name']})	#Adds it to a temporary list
        temp_projects = sorted(temp_projects, key=lambda k: k['name'])		#Sorts it by name  
        if temp_projects:		#if temp_projects exist, add it to projects
            projects.append(temp_projects)
            temp_projects = []		#Clear the temporary list for the next technique
   
    for i in range(len(tech_list)):		#Puts all the list together into a dict, and then adds it to the final list
        stats = dict(zip(dict_keys[0:3], [tech_count[i], tech_list[i], projects[i]]))
        tech_stats.append(stats)        

    return (errorcode, tech_stats)
