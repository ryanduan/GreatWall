Deployment environment

Ubuntu:

    sudo apt-get install python python-dev
    sudo apt-get install python-virtualenv or pip install virtualenv
    virtualenv --no-site-packages gwenv
    source gwenv/bin/activate
    pip install django
    pip install django-rosetta
    pip install fabric

fabric:
 touch fabfile.py
 vim fabfile.py

rosetta:
 mkdir locale
 mkdir locale/en
 mkdir locale/zh
 fab makemessages
