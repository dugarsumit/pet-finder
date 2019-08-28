import os
import subprocess

print(os.environ.get('PORT', None))
port = os.environ.get('PORT', "8000")
host = "0.0.0.0" + ":" + port
subprocess.call(["python", "petfinder/manage.py", "migrate"])
subprocess.call(["python", "petfinder/manage.py", "runserver", host])
