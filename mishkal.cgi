#!/usr/bin/python
# -*- coding=UTF-8 -*-
import sys, os, os.path, re
from glob import glob
import cgitb
cgitb.enable(logdir=os.path.join(os.path.dirname(__file__), 'tmp/logs'),
            display=True, format='html',)
sys.path.append('interfaces/web/lib/');
sys.path.append('interfaces/web');
sys.path.append('support');
sys.path.append('mishkal');
#~ from okasha2.baseWebApp import *
#~ from okasha2.utils import fromFs, toFs
#~ from adawaty import *
import okasha2.baseWebApp
from okasha2.utils import fromFs
#~ import okasha2.utils.toFs
import adawaty
# this requires python-paste package
import logging
import cgirunner  

if __name__ == '__main__':

    # prepare logging 
    d = fromFs(os.path.dirname(sys.argv[0]))
    LOG_FILENAME = os.path.join(d,u'tmp','logging_mishkal.out')
    logging.basicConfig(filename = LOG_FILENAME,level=logging.INFO,)
    myLogger = logging.getLogger('Mishkal')
    h = logging.StreamHandler() # in production use WatchedFileHandler or RotatingFileHandler
    h.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    myLogger.addHandler(h)
    myLogger.setLevel(logging.INFO) # in production use logging.INFO
    #~ myLogger.setLevel(logging.DEBUG) # in production use logging.INFO

    app = adawaty.webApp(
      os.path.join(d,u'interfaces/web/resources/templates'),
      staticBaseDir={u'/_files/':os.path.join(d,u'interfaces/web/resources/files'),
      u'~/':os.path.join(d,u'tmp/home/'),
      },
      logger=myLogger
    );
    # for options see http://pythonpaste.org/modules/httpserver.html
    cgirunner.run_with_cgi(app)
