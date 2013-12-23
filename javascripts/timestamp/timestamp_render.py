#!/usr/bin/python

import jinja2
import time  

templateLoader = jinja2.FileSystemLoader( searchpath="./" )
templateEnv = jinja2.Environment( loader=templateLoader )

TEMPLATE_FILE = "timestamp/template_timestamp.json"
template = templateEnv.get_template( TEMPLATE_FILE )

# Here we add a new input variable containing a list.
# Its contents will be expanded in the HTML as a unordered list.
myfile = "xchart_data.json"
mytime = time.strftime("%c")

templateVars = { "file" : myfile, "time" : mytime }

outputText = template.render( templateVars )

print outputText
