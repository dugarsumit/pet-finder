import os
import subprocess

print(os.environ['PORT'])
host = "0.0.0.0" + ":" + os.environ['PORT']
subprocess.call(["python", "petfinder/manage.py", "migrate"])
subprocess.call(["python", "petfinder/manage.py", "runserver", host])
