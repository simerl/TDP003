#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

def init():
    csvReader = csv.DictReader(open('data.csv', 'rb'), delimiter=',')	#reads from csv file
    unic = []								#creates a list which will be used to store the lines of the csv file
    for row in csvReader:
        row2 = {}							#creates an empty dict
        for key, value in row.iteritems():
            row2[unicode(key, 'utf-8')] = unicode(value,'utf-8')	#puts the current row in the dict and converts it to unicode
        unic.append(row2)						#adds the dict to the list "unic"

    for i in range(len(unic)):						#Converts project_no back from unicode string to integer
        unic[i]["project_no"] = int((unic[i]["project_no"]))
    for i in range(len(unic)):						#Does the same with group_size
        unic[i]["group_size"] = int((unic[i]["group_size"]))

    return unic								#Returns unic
    
									#possibe problem: the elements in the dict isn't correctly sorted

#def project_count():


#def lookup_project():


#def retrieve_project():


#def retrieve_techniques():


#def retieve_techniques_stats():


