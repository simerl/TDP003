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
    global unic
    global errorcode
    for dic in unic:
    	if a == dic['project_no']:
			return (errorcode, dic)
    return (2, None)

def retrieve_project():#sort_by='start_date', sort_order='asc', techniques=None, search=None, search_fields=None):
	global unic
	global errorcode


#def retrieve_techniques():



#def retieve_techniques_stats():


