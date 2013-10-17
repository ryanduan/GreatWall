from fabric.api import local


def makemessages():
    local('django-admin.py makemessages -l en -e html,py,inc,txt -s')
    local('django-admin.py makemessages -l en -d djangojs')
    local('django-admin.py makemessages -l zh -e html,py,inc,txt -s')
    local('django-admin.py makemessages -l zh -d djangojs')
    local('django-admin.py compilemessages')
