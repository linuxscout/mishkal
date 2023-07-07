#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mishkal_config.py
#  
OFFLINE = True
# ~ OFFLINE = False   # hosted localy

# in developement True in production False
#MODE_DEBUG = True
MODE_DEBUG = False

if OFFLINE:
    # URL HOST
    # For Testing
    URL_HOST_PATH = "http://127.0.0.1/mishkal"
    DIR_HOST_PATH = "/var/www/html/mishkal"

    #Database config directory
    DB_BASE_PATH = "/var/www/html/mishkal/"
    # Logging file
    LOGGING_CFG_FILE = DIR_HOST_PATH +"/web/config/logging.cfg"
    LOGGING_FILE     = DIR_HOST_PATH +"/web/logs/demo.log" 
else:
    # For Production
    URL_HOST_PATH = "https://example.com/mishkal"
    DIR_HOST_PATH = "~/public_html/cgi-bin"    
    #Database config directory
    DB_BASE_PATH = "/var/www/html/mishkal/"
    MY    

    # Logging file
    LOGGING_CFG_FILE = DIR_HOST_PATH +"/mishkal/web/config/logging.cfg"
    LOGGING_FILE = DIR_HOST_PATH +"/mishkal/web/logs/demo.log"      

def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
