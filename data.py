#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
unic = []								#Creates a global list which will be used to store the lines of the csv file
errorcode = 1								#Sets the error code to "error accessing data file" because no data is loaded
def init():
    global unic
    global errorcode
    csvReader = csv.DictReader(open('data.csv', 'rb'), delimiter=',')	#Reads from csv file
    
    for row in csvReader:
        row2 = {}							#Creates an empty dict
        for key, value in row.iteritems():
            row2[unicode(key, 'utf-8')] = unicode(value,'utf-8')	#Puts the current row in the dict and converts it to unicode
        unic.append(row2)						#Adds the dict to the list "unic"

    for i in range(len(unic)):						#Converts project_no back from unicode string to integer
        unic[i]["project_no"] = int((unic[i]["project_no"]))
    for i in range(len(unic)):						#Does the same with group_size
        unic[i]["group_size"] = int((unic[i]["group_size"]))
    for i in range(len(unic)):						#Converts techniques_used to list
        unic[i]["techniques_used"] = (unic[i]["techniques_used"].split(','))
    errorcode = 0							#Changes the error code to "Ok"
    return unic								#Returns unic
    
									#Possibe problem: the dict isn't correctly sorted, bad variable names

def project_count():
    global unic
    global errorcode
    return (errorcode, len(unic))					#Returns the error code and the length of unic as a tuple


#The error codes are: 0 = Ok, 1 = error accessing data file and 2 = requested project does not exist.



def lookup_project(a):
    global unic
    global errorcode
    b=0
    if a > len(unic) and len(unic) != 0:				#If statement to change the errorcode if the project doesn't exist in the database
	    errorcode = 2							        #obs problem! om projekt 3 inte finns men det finns totalt 5 projekt ges fel errorcode
	    return errorcode
    else:
	for i in range(len(unic)):
        if a == unic[b]["project_no"]:
	    	#errorcode = 0
	    	return (errorcode, unic[b])
		    break
        else:
            b += 1




#for id in unic[i]["project_no"]:
	#print "hej"
    return errorcode


#def retrieve_project():


#def retrieve_techniques():



#def retieve_techniques_stats():


