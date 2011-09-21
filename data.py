#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

def init():
    csvReader = csv.reader(open('data.csv', 'rb'), delimiter=',')
    print csvReader.line_num(1)

#def project_count():


#def lookup_project():


#def retrieve_project():


#def retrieve_techniques():


#def retieve_techniques_stats():


