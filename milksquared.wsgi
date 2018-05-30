#!/usr/bin/python

import sys

sys.path.insert(0,"/var/www/milksquared/")

from milksquared import my_app as application
application.secret_key = 'i dont have a secret key'
