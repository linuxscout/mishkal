#!/home/tahadz/usr/bin/python
import sys, os, os.path, re
from glob import glob
sys.path.append('lib/');
sys.path.append('lib/web');
from okasha.baseWebApp import *
from okasha.utils import fromFs, toFs
from adawaty import *
if __name__ == '__main__':
    # this requires python-paste package
    import logging
    import cgirunner

    d=fromFs(os.path.dirname(sys.argv[0]))
    LOG_FILENAME = os.path.join(d,u'tmp','logging_example.out')
    logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,)
    myLogger=logging.getLogger('MyTestWebApp')
    h=logging.StreamHandler() # in production use WatchedFileHandler or RotatingFileHandler
    h.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    myLogger.addHandler(h)
    myLogger.setLevel(logging.INFO) # in production use logging.INFO
    #d=fromFs(os.path.dirname(sys.argv[0]))

    app=webApp(
      os.path.join(d,u'templates'),
      staticBaseDir={u'/_files/':os.path.join(d,u'files')},
	  logger=myLogger
    );
    # for options see http://pythonpaste.org/modules/httpserver.html
    cgirunner.run_with_cgi(app)
