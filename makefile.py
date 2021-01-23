import os

os.system('python3 manage.py makemigrations')
os.system('python3 manage.py migrate')
os.system('python3 manage.py runserver 195.133.147.101:228')