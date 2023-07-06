#!/bin/bash

PWD=$1

cd /home/kusaches/fitness/fitness-backend
echo $PWD | sudo -S find . -path "*/migrations" -type d -exec sh -c 'mv "$0" "${0/migrations/fake-migrations}"' {} \;
echo "
**/migrations/
**/migrations/*.py
**/migrations/*.pyc
!**migrations/__init__.py

**/fake-migrations/
**/fake-migrations/*.py
**/fake-migrations/*.pyc

pgbouncer-1.15.0/
" >> .gitignore
rm -rf pgbouncer-1.15.0.tar.gz
rm -rf pgbouncer-1.18.0.tar.gz
echo $PWD | sudo -S git add .gitignore
echo $PWD | sudo -S git commit -m "gitignore file changes"
echo $PWD | sudo -S git reset --hard
echo $PWD | sudo -S git pull
echo $PWD | sudo -S git checkout prod-new-extra-without-migrations
echo $PWD | sudo -S find . -path "*/fake-migrations" -type d -exec sh -c 'mv "$0" "${0/fake-migrations/migrations}"' {} \;
echo $PWD | sudo -S pip3 install django-filter
echo $PWD | sudo -S pip3 install aiochclient
echo $PWD | sudo -S python3 manage.py makemigrations
echo $PWD | sudo -S python3 manage.py migrate
