import jinja2

env = jinja2.Environment()
env.globals.update(zip=zip)
# use env to load template(s)

templateLoader = jinja2.FileSystemLoader( searchpath="./" )
templateEnv = env( loader=templateLoader )

TEMPLATE_FILE = "template.jinja"
template = templateEnv.get_template( TEMPLATE_FILE )

# Here we add a new input variable containing a list.
# Its contents will be expanded in the HTML as a unordered list.
FAVORITES = [ "chocolates", "lunar eclipses", "rabbits" ]

templateVars = { "title" : "Test Example",
                 "description" : "A simple inquiry of function.",
                 "favorites" : FAVORITES
               }

outputText = template.render( templateVars )

