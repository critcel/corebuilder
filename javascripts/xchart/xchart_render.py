#!/usr/bin/python

import jinja2
import string

import jinja2
#env = jinja2.Environment()
#env.globals.update(zip=zip)
# use env to load template(s)

templateLoader = jinja2.FileSystemLoader( searchpath="./" )
templateEnv = jinja2.Environment( loader=templateLoader )

TEMPLATE_FILE = "xchart/template_xchart.json"
template = templateEnv.get_template( TEMPLATE_FILE )

# Here we add a new input variable containing a list.
# Its contents will be expanded in the HTML as a unordered list.
X = [ "1x1", "2x2", "3x3" ]
Y = [ 4, 8, 8 ]

templateVars = { "bar_data":
                 ["\"x\": \""+str(i)+"\", \"y\": "+str(j) for i,j in zip(X,Y)],
               }

outputText = template.render( templateVars )

print outputText
