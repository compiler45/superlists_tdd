Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3.6
* virtualenv + pip
* Git

e.g. on Ubuntu

sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get install nginx git python36 python3.6-venv

## Nginx Virtual host config ##

* see nginx.template.conf
* replace SITENAME with subdomain name

## Systemd service ##

* see gunicorn-systemd.template.service 
* replace SITENAME with subdomain name

## Folder structure: ##
Assume we have a user account at /home/username
/home/username
---> sites
     ---> SITENAME
          ---> database
          ---> source
          ---> static
          ---> virtualenv
