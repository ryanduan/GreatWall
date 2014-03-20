####Introduction
######Functions
1. Django i18n (unfinished): more than one language in the project.

2. South: database migration.

###Install on Ubuntu 12.04(12.10/13.04/13.10):
####Deployment environment

    sudo apt-get install python python-dev
    sudo apt-get install python-virtualenv (or pip install virtualenv)
    virtualenv --no-site-packages gwenv
    source gwenv/bin/activate
    pip install django
    pip install django-rosetta
    pip install fabric

####Create a django project
    mkdir GreatWall
    cd GreatWall
    django-admin.py startproject easyauto
    cd easyauto
    python manage.py startapp suvs

####Configuration
#####Project & application
    vim easyauto/settings.py (add database/add application/add rosetta)
    vim easyauto/urls.py (add url)
    vim suvs/views.py (add views functions)

#####The rosetta:
    vim fabfile.py(create a function named makemessages)
    mkdir locale
    mkdir locale/en
    mkdir locale/zh
    fab makemessages

#####You can clone my project

    git clone https://github.com/ryanduan/GreatWall.git
