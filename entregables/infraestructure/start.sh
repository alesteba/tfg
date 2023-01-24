
#!/bin/bash

curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc|sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg

sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

sudo apt update
sudo apt upgrade

sudo apt install postgresql-14
sudo apt install postgresql-14-postgis-scripts

sudo service postgresql start

sudo -u postgres createuser -P agrai_user
sudo -u postgres createdb -O agrai_user agrai_db
sudo -u postgres psql -c "CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;" agrai_db

# gdal native:
sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
sudo apt-get update
  
# cargarte la versión de la máquina, dejar solo 1:
sudo apt autoremove python3

# python repositories

sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa

# python concrete installation

sudo apt install python3.10 # version concreta
sudo apt-get install python3.10-dev python3.10-venv
sudo apt install python3.10-dev python3.10-venv
sudo apt install virtualenv

# python env var

export PYTHONPATH="/usr/local/bin/python3.10:/usr/local/lib/python3.10/lib-dynload:/usr/local/lib/python3.10/site-packages"

alias py=python3.10
alias python=python3.10
alias python3=python3.10

# creacion entorno_venv
sudo python3.10 -m venv ../agrai_venv

# GDAL
sudo apt-get install libgdal-dev

# env gdal lib variables

export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal

# install dep in python agrai_venv

source ../agrai_venv/bin/activate
# pip install --upgrade pip # quitar
sudo python3 -m pip install -r requirements.txt