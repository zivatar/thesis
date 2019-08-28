#!/bin/bash

NAME="zivatar"                              #Name of the application (*)
DJANGODIR=/app             # Django project directory (*)
SOCKFILE=/app/run/gunicorn.sock        # we will communicate using this unix socket (*)
USER=django                                        # the user to run as (*)
GROUP=django                                     # the group to run as (*)
NUM_WORKERS=1                                     # how many worker processes should Gunicorn spawn (*)
DJANGO_SETTINGS_MODULE=zivatar.settings             # which settings file should Django use (*)
DJANGO_WSGI_MODULE=zivatar.wsgi                     # WSGI module name (*)

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
#source /home/django/szd/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
#gunicorn --timeout=30 --workers=2 --bind 0.0.0.0:8000 ${DJANGO_WSGI_MODULE}:application
