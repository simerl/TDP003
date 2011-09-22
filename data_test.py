#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import md5

print "Testfile for data.py - version 1.6"
print "Created by Niklas Hayer"
print md5.new(sys.argv[0]).hexdigest()
print

import data

def WORKED(errcode):
    assert errcode == 0
	
data_temp_name = "data_should-not-be-used-anymore.csv"
	
if os.path.exists(data_temp_name):
  os.rename(data_temp_name, "data.csv")

errcode, result = data.project_count()
assert errcode != 0

data.init()

os.rename("data.csv", data_temp_name)

errcode, result = data.project_count()
WORKED(errcode)
assert result == 4

errcode, result = data.lookup_project(1)
WORKED(errcode)
assert result[u'course_id'] == u'TDP003'
assert result[u'course_name'] == u'OKÄNT'
assert result[u'techniques_used'] == [u'python']

errcode, result = data.lookup_project(4)
WORKED(errcode)
assert result[u'course_id'] == u' "'
assert result[u'techniques_used'] == []
assert result[u'lulz_had'] == u'over 9000'

errcode, result = data.lookup_project(2)
WORKED(errcode)
assert result[u'project_name'] == u'2007'

errcode, result = data.lookup_project(3)
WORKED(errcode)
assert result[u'lulz_had'] == u'few'
assert result[u'techniques_used'] == [u'c++', u'csv', u'python']

errcode, result = data.lookup_project(9000)
assert errcode == 2
assert result == None

errcode, result = data.retrieve_techniques()
WORKED(errcode)
assert len(result) == 4
assert result == [u'ada', u'c++', u'csv', u'python']

errcode, result = data.retrieve_projects()
WORKED(errcode)
assert len(result) == 4

errcode, result = data.retrieve_projects(techniques=["csv"])
WORKED(errcode)
assert len(result) == 1

errcode, result = data.retrieve_projects(sort_order='desc',techniques=["python"])
WORKED(errcode)
assert len(result) == 3
assert result[0][u'project_no'] == 2
assert result[1][u'project_no'] == 3
assert result[2][u'project_no'] == 1

errcode, result = data.retrieve_projects(sort_by="end_date", search="okänt", search_fields=["project_no","project_name","course_name"])
WORKED(errcode)
assert len(result) == 3
assert result[0][u'project_no'] == 1
assert result[1][u'project_no'] == 3
assert result[2][u'project_no'] == 2


errcode, result = data.retrieve_projects(search="okänt", search_fields=["project_no","project_name","course_name"])
WORKED(errcode)
assert len(result) == 3

errcode, result = data.retrieve_projects(techniques=[], search="okänt", search_fields=["project_no","project_name","course_name"])
WORKED(errcode)
assert len(result) == 3

errcode, result = data.retrieve_projects(search="okänt", search_fields=[])
WORKED(errcode)
assert len(result) == 0

errcode, result = data.retrieve_projects(sort_by='group_size')
WORKED(errcode)
assert len(result) == 4
assert result[0][u'project_no'] == 1
assert result[1][u'project_no'] == 3
assert result[2][u'project_no'] == 2
assert result[3][u'project_no'] == 4

errcode, result = data.retrieve_technique_stats()
WORKED(errcode)
t_stats_expect_result = [
{u'count': 1, u'name': u'ada', u'projects': [{u'id': 2, u'name': u'2007'}]},
{u'count': 1, u'name': u'c++', u'projects': [{u'id': 3, u'name': u'NEJ'}]},
{u'count': 1, u'name': u'csv', u'projects': [{u'id': 3, u'name': u'NEJ'}]},
{u'count': 3, u'name': u'python', u'projects': [{u'id': 2, u'name': u'2007'}, {u'id': 3, u'name': u'NEJ'}, {u'id': 1, u'name': u'python data-module test script'}]}
]
assert result == t_stats_expect_result

os.rename(data_temp_name, "data.csv")

print "Tests Complete!"
