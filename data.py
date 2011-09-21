#!/usr/bin/python
# -*- coding: utf-8 -*-

#en kommentar

import csv

def init():
    csvReader = csv.DictReader(open('data.csv', 'rb'), delimiter=',')
    unic = []
    for row in csvReader:
        row2 = {}
        for key, value in row.iteritems():
            row2[unicode(key, 'utf-8')] = unicode(value,'utf-8')
        unic.append(row2)

    return unic

#def project_count():


#def lookup_project():


#def retrieve_project():


#def retrieve_techniques():


#def retieve_techniques_stats():


