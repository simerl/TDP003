#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

import locale                                                           #Imports locale, will be used to sort lists containing unicode strings
locale.setlocale(locale.LC_ALL, "sv_SE.UTF-8")                          #Sets locale to utf-8 swedish

unic = []								                                #Creates a global list which will be used to store the lines of the csv file
errorcode = 1								                            #Sets the error code to "error accessing data file" because no data is loaded

def init():
    global unic
    global errorcode

    csvReader = csv.DictReader(open('data.csv', 'rb'), delimiter=',')	#Reads from csv file
    
    for row in csvReader:
        row2 = {}							                            #Creates an empty dict
        for key, value in row.iteritems():
            row2[unicode(key, 'utf-8')] = unicode(value,'utf-8')	    #Puts the current row in the dict and converts it to unicode
        unic.append(row2)						                        #Adds the dict to the list "unic"

    for i in range(len(unic)):						                   
        unic[i]["project_no"] = int((unic[i]["project_no"]))            #Converts project_no back from unicode string to integer
        unic[i]["group_size"] = int((unic[i]["group_size"]))            #Does the same with group_size
    
    for i in range(len(unic)):						                    #Converts techniques_used to list then sort it using swedish locale
        if len(unic[i]["techniques_used"]) > 0:                                                              
            temp = unic[i]["techniques_used"]                        
            unic[i]["techniques_used"] = temp.split(',')
            unic[i]["techniques_used"] = sorted(unic[i]["techniques_used"], cmp=locale.strcoll)
        else:
            unic[i]["techniques_used"] = []
        
    errorcode = 0							                            #Changes the error code to "Ok"

    return unic								                            #Returns unic


def project_count():

    return (errorcode, len(unic))										#Returns the error code and the length of unic as a tuple


#The error codes are: 0 = Ok, 1 = error accessing data file and 2 = requested project does not exist.



def lookup_project(a):                                                  #Måste ändra a till id, kanske

    for dic in unic:
    	if a == dic['project_no']:
			return (errorcode, dic)

    return (2, None)

def retrieve_projects(sort_by='start_date', sort_order='asc', techniques=None, search=None, search_fields=None):

    sorted_list = []
    tech_list = []
    search_list = []

    if techniques:
        for proj in unic:
            for x in techniques:
                if x in proj['techniques_used']:
                    tech_list.append(proj)

    else:
        tech_list = unic

    if search and search_fields:
        search = unicode(search, 'utf-8')
        search = search.lower()

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

    if sort_order == 'desc':
        sorted_list.reverse()

    return (errorcode, sorted_list)

def retrieve_techniques():

    tech_list = []

    for proj in unic:
        for tech in proj['techniques_used']:
            if tech not in tech_list:
                tech_list.append(tech)

    tech_list = sorted(tech_list)

    return (errorcode, tech_list)

#def retieve_techniques_stats():


