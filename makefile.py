import os

os.system('git pull')
os.system('python3 manage.py makemigrations user_api')
os.system('python3 manage.py migrate')
os.system('python3 manage.py runserver 195.133.147.101:228')
