#!/bin/sh

./manage.py schemamigration statistics --auto
./manage.py migrate statistics 
