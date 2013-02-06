import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask.ext.script import Manager, Server
from tumblelog import app

manager = Manager(app)

# Turn on debugger by default and reloader
'''
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0')
)
'''
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = 'ec2-50-18-9-255.us-west-1.compute.amazonaws.com', port=27017)
)
#'''
if __name__ == "__main__":
    manager.run()
