import jinja2
import time  

import jinja2
#env = jinja2.Environment()
#env.globals.update(zip=zip)
# use env to load template(s)

templateLoader = jinja2.FileSystemLoader( searchpath="./" )
templateEnv = jinja2.Environment( loader=templateLoader )

TEMPLATE_FILE = "template_timestamp.json"
template = templateEnv.get_template( TEMPLATE_FILE )

# Here we add a new input variable containing a list.
# Its contents will be expanded in the HTML as a unordered list.
myfile = "plot.js"
mytime = time.strftime("%c")

templateVars = { "file" : myfile, "time" : mytime }

outputText = template.render( templateVars )

print outputText
