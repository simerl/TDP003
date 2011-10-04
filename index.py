#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
import data
app = Flask(__name__)
data.init()
@app.route("/")
def hello():
    
    hej = data.retrieve_techniques()
    
    return hej

if __name__ == "__main__":
    app.run()
