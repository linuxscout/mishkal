#!/usr/bin/python3
# -*- coding=UTF-8 -*-
import sys, os, os.path, re
import os;
import locale; 
os.environ["PYTHONIOENCODING"] = "utf-8"; 
from glob import glob
sys.path.append('interfaces/web');
from bottle import run
import mishkal_bottle

if __name__ == '__main__':
    run(mishkal_bottle.app, host='localhost', port=8080, debug=True, server="cgi")    
