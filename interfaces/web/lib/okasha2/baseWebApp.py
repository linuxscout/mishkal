# -*- coding: UTF-8 -*-
"""
Okasha - a very simple WSGI webframe work
Copyright © 2009, Muayyad Alsadi <alsadi@ojuba.org>

    Released under terms of Waqf Public License.
    This program is free software; you can redistribute it and/or modify
    it under the terms of the latest version Waqf Public License as
    published by Ojuba.org.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

    The Latest version of the license can be found on
    "http://waqf.ojuba.org/license"

"""
ALLOW_DEBUG = False
import sys, os, os.path, time, re
try: import json
except ImportError: import simplejson as json

#import json # for templates
import urlparse # for parsing query string
from cgi import escape, FieldStorage # for html escaping
from operator import attrgetter # for OkashaFields
from Cookie import SimpleCookie # in python 3.0 it's from http.cookies import SimpleCookie
from utils import fromFs, toFs

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

#import urllib # to be used for quote and unquote

# TODO: use c=Cookie.SimpleCookie(string)

webAppResponses={
    200:'200 OK',
    302:'302 Temporary Redirect',
    403:'403 Forbidden',
    404:'404 Not Found Taha',
    500:'500 Internal Server Error'
  }

class webAppBaseException(Exception):
  """
  exceptions like fileNotFoundException
  """
  def __init__(self, code, *args,**kw):
    self.code=code
    self.args=args
    self.kw=kw


forbiddenException=lambda *a,**kw: webAppBaseException(403,*a,**kw)
fileNotFoundException=lambda *a,**kw: webAppBaseException(404,*a,**kw)
def redirectException(location,*a,**kw):
  e=webAppBaseException(302,*a,**kw)
  if type(location)==unicode: l=location.encode('utf-8')
  else: l=location
  e.kw['location']=l
  return e


class Response:
  def __init__(self, rq=None, code=None,contentType=None,headers=None):
    self.rq=rq
    self.code=code
    self.contentType=contentType
    self.headers=headers
    self.cookies=SimpleCookie('')

  def setCookie(self, key, value, t=None, path=None, domain=None, comment=None):
    """
    sets or replace a cookies with key and value, and sets its expire time in seconds since now (if given)
    """
    if isinstance(value,unicode): value=value.encode('utf8')
    self.cookies[key]=value
    if t!=None:
      # TODO: is this the right way of setting both expires and max-age
      self.cookies[key]['expires']=time.strftime("%a, %d %b %Y %H:%M:%S UTC", time.gmtime(time.time()+t))
      if t>0: self.cookies[key]['max-age']=t
    if path==None: path=self.rq.script+'/'
    if isinstance(path,unicode): path=path.encode('utf8')
    self.cookies[key]['path']=path
    if domain!=None:  self.cookies[key]['domain']=domain
    if comment!=None:  self.cookies[key]['comment']=comment

ok_tailing_digits=re.compile("^(.*?)(\d*)$",re.U)

class OkashaFields(FieldStorage):
  def __init__(self, *args, **kw):
    self._ok_max_files_count=-1
    FieldStorage.__init__(self, *args, **kw)
    # TODO: do we need to process tmp files by overriding make_file and delete ?

  def _suggest_fn(self, fn, suffix_len):
    if suffix_len==None:
      i=fn.rfind(".")
      if i<0: i=len(fn);
    b=fn[:i]
    e=fn[i:]
    l=ok_tailing_digits.findall(b)
    b=l[0][0]
    n=l[0][1]
    if not n: n=2
    else: n=int(n)+1
    fn=b+str(n)
    while(os.path.exists(fn)):
      n+=1; fn=b+str(n)
    return fn

  def save_as(self, key, fn, overwrite=False):
    if key not in self: return False
    l=self[key]
    if type(l) is type([]):
      if len(l)==1: i=l[0]
      else: return False
    else: i=l
    if os.path.exists(fn):
      if overwrite: os.unlink(fn)
      else: return False
    i.file.seek(0)
    try: open(fn,"wb").write(i.file.read())
    finally: i.file.seek(0)
    return True


  def _save_in(self, i, d, overwrite, name_pattern, suffix_len, max_size):
    # FIXME: max_size is ignored
    r=0
    if name_pattern==None: name_pattern=i.filename
    fn=os.path.join(d,name_pattern)
    if os.path.exists(fn):
      if overwrite==False: return 0
      elif overwrite==None: fn=self._suggest_fn(name_pattern, suffix_len)
      else: os.unlink(fn)
    i.file.seek(0)
    # FIXME: done at once using memory, maybe we want to do it in chunks
    # FIXME: implement size-based limits
    try: open(fn,"wb").write(i.file.read()); r=1 # on success
    finally: i.file.seek(0)
    return r

  def save_in(self, key, d, overwrite=False, name_pattern=None,suffix_len=None, max_count=0, max_size=-1):
    """this method handles multiple files having same form name
    if overwrite==False then already existing files will be ignored
    if true they will be overwritten
    if None then number will be aded or incremented after name_pattern[:-suffix_len] if suffix_len==None then rfind('.') will be used
    return number of successfully saved files on success
      0     key not found
      -1    max_count exceeded
      -2    max_size exceeded
      -3    dir does not exist
      -4    IOError
    """
    if not os.path.isdir(d): return -3
    r=0
    if key not in self: return r
    l=self[key]

    if type(l) is type([]):
      c=len(l)
      if max_count<=0: max_count=self._ok_max_files_count
      if max_count>0 and len(l)>max_count: return -1
      for i in l:
        try: r+=self._save_in(i, d. overwrite, name_pattern, suffix_len, max_size)
        except IOError: return -4
    else:
      try: r=self._save_in(l, d, overwrite, name_pattern, suffix_len, max_size)
      except IOError: return -4
    return r


class Request:
  def __init__(self, webapp, environ, start_response):
    self.webapp=webapp
    self.environ=environ
    self.script=environ.get('SCRIPT_NAME','') # the uri of the webapp
    self.rhost=environ.get('REMOTE_ADDR','')
    self.start_response=start_response
    self.response=Response(self)
    # FIXME: find a way to simplify decoding query strings into unicode
    qs=environ.get('QUERY_STRING','')
    if environ.has_key('wsgi.input'):
      self.q=OkashaFields(fp=environ['wsgi.input'],environ=environ)
    else: self.q=OkashaFields(fp=StringIO(''),environ=environ)

    try: self.cookies=SimpleCookie(environ.get('HTTP_COOKIE','')) # cookies['key'].value
    except: self.cookies=SimpleCookie('')

    if environ.has_key('PATH_INFO'):
      self.uri=environ['PATH_INFO'] # can be / or /view
    else: self.uri="/";
    if type(self.uri)!=unicode:
      try: self.uri=self.uri.decode('utf8')
      except UnicodeDecodeError: self.uri=None

    if self.uri.endswith('/'): self.tailingSlash=True
    else: self.tailingSlash=False
    if self.uri.startswith('/'): self.uriList=self.uri[1:].split(u'/')
    else: self.uriList=self.uri.split('/') # NOTE: this should never happen
    if self.uriList and self.uriList[-1]=='': self.uriList.pop()


class expose:
  def __init__(self, template=None, templateArgs=[],templateKw={},
    responseCode=200, contentType='text/html; charset=utf-8', headers={},
    requiresTailingSlash=False
    ):
    """
    a decorator that applies the result of the function to the provided template
    """
    self._template=template
    self._templateArgs=templateArgs
    self._templateKw=templateKw
    self._response=responseCode
    self._contentType=contentType
    self._headers=headers
    self._requiresTailingSlash=requiresTailingSlash

  def __call__(self, func):
    def wrapper(*args):
      if not args: raise webAppBaseException(500)
      elif isinstance(args[0],baseWebApp) and len(args)>=2:
        rq=args[1]
      else:
        rq=args[0]
      if self._requiresTailingSlash and not rq.tailingSlash:
        raise redirectException(rq.script+rq.uri+'/')
      # FIXME: do we need here a try: except:
      if self._template:
        r=self._template(rq, func(*args), *self._templateArgs, **self._templateKw)
      else: r=func(*args)

      # fix response
      if rq.response.code==None: rq.response.code=self._response
      if rq.response.contentType==None: rq.response.contentType=self._contentType
      # FIXME: it should be merged not replaced
      if rq.response.headers==None: rq.response.headers=self._headers
      rs=webAppResponses.get(rq.response.code,"%d Unknown code" % rq.response.code)
      cookies=rq.response.cookies.output(header="")
      if cookies: h=map(lambda c: ('Set-Cookie',c),cookies.split('\n'))
      else: h=[]
      rq.start_response(rs, [('content-type', rq.response.contentType)]+h+map(lambda k: (k,rq.response.headers[k]),rq.response.headers))
      if type(r)==unicode: return (r.encode('utf8'),)
      elif isinstance(r, basestring): return (r,)
      return r
    return wrapper

def formatTemplate(rq, v, bfn=None):
  """
  see http://docs.python.org/library/string.html#format-string-syntax
  """
  d=rq.webapp._templatesDir
  if not os.path.isdir(d): raise fileNotFoundException()
  if not bfn: bfn='root.html'
  fn=os.path.join(d, bfn)
  try: tmp=open(fn,'rt').read().decode('utf-8')
  except IOError: raise fileNotFoundException()
  except:
    rq.webapp._logger.debug('template error fn=[%s]' % fn)
    raise
  # Note: try is used to check for valid template
  #try: s=[(tmp % v).encode('utf-8')] # NOTE: it expects a byte sequence not unicode object
  try:
    if isinstance(v,dict): s=tmp.format(**v)
    else: s=tmp.format(*v)
  except TypeError: raise KeyError
  except KeyError: raise TypeError
  # FIXME: use logger for above exceptions
  return s

def percentTemplate(rq, v, bfn=None):
  """
  see http://docs.python.org/library/stdtypes.html#string-formatting-operations
  """
  d=rq.webapp._templatesDir
  #rq.webapp._logger.info('template uses d=[%s]' % d)
  if not os.path.isdir(d): raise fileNotFoundException()
  if not bfn: bfn='root.html'
  fn=os.path.join(d, bfn)
  #rq.webapp._logger.info('template uses fn=[%s]' % fn)

  try: tmp=open(fn,'r').read().decode('utf-8')
  except IOError: raise fileNotFoundException()
  except:
    rq.webapp._logger.debug('template error fn=[%s]' % fn)
    raise
  # Note: try is used to check for valid template
  #try: s=[(tmp % v).encode('utf-8')] # NOTE: it expects a byte sequence not unicode object
  try: s=tmp % v # NOTE: it expects a byte sequence not unicode object
  except TypeError: raise KeyError
  except KeyError: raise TypeError
  # FIXME: use logger for above exceptions
  return s

def jsonDumps(rq, o):
  if not rq.response.contentType:
    rq.response.contentType='application/x-javascript; charset=utf-8'
  return json.dumps(o, ensure_ascii=False)

class fakeLogger:
  def debug(self,msg): pass
  def info(self, msg): pass
  def warning(self, msg): pass
  def error(self, msg): pass
  def critical(self, msg): pass

class baseWebApp:
  """
  The base for our web Application, it's a mini web framework
  """
  _mimeByExtension={
    'html': 'text/html', 'txt': 'text/plain', 'css': 'text/css',
    'js':'application/javascript',
    'ico': 'image/x-icon', 'png': 'image/png', 'gif': 'image/gif',
    'jpg': 'image/jpeg', 'jpeg': 'image/jpeg'
  }

  def __init__(self, templatesDir, staticBaseDir={}, redirectBaseUrls={}, logger=fakeLogger(), max_files_count=-1, debug=False):
    """
    staticBaseDirs: a dictionary of prefixes and corresponding directories for serving static content
    redirectBaseUrls: just like staticBaseDirs, but redirect to this BaseUrls instead of surving them

    if a prefix is specified in both, redirectBaseUrls will be used.

    logger is logging object from python logging module

    max_files_count is the max number of upload file fields with dupplicated names (-1 unlimited, 1 unique keys)
    """
    self._logger=logger
    # TODO: add a self._templateFilesCache
    self._templatesDir=templatesDir
    # TODO: add a self._staticFilesCache
    self._staticBaseDir={}
    self._max_files_count=max_files_count
    self._debug=debug # FIXME: no longer needed
    for k in staticBaseDir:
      v=staticBaseDir[k]
      if not os.path.isdir(v):
        self._logger.warning("WARNING: directory [%s] not found, skipping" % v)
        continue
      self._staticBaseDir[self._tailingSlash(k)]=self._tailingOsSlash(fromFs(os.path.abspath(toFs(v))))

    self._redirectBaseUrls={}
    for k in redirectBaseUrls:
      self._redirectBaseUrls[self._tailingSlash(k)]=self._tailingSlash(redirectBaseUrls[k])
    self._staticBaseDirKeys=self._staticBaseDir.keys()
    self._staticBaseDirKeys.sort()
    self._staticBaseDirKeys.reverse() # so it's from longer to shorter
    self._redirectBaseUrlsKeys=self._redirectBaseUrls.keys()
    self._redirectBaseUrlsKeys.sort()
    self._redirectBaseUrlsKeys.reverse()

  def _tailingOsSlash(self, s):
    if not s.endswith(os.sep): return s+os.sep
    return s


  def _tailingSlash(self, s):
    if not s.endswith('/'): return s+'/'
    return s

  def _handleException(self, rq, e):
    s='_'+str(e.code)
    if hasattr(self, s):
      return getattr(self, s)(rq, e)
    return self._genericException(rq, e)

  def _genericException(self, rq, e):
    rs=webAppResponses.get(e.code,"%d Unknown code" % e.code)
    if rq.uri: s="exception [%s] happened when visiting [%s]" % (rs,rq.uri)
    else: s="exception [%s] happened" % rs
    rq.start_response(rs, [('content-type', 'text/plain')])
    return [s]

  def _302(self, rq, e):
    rs=webAppResponses[302]
    cookies=rq.response.cookies.output(header="")
    if cookies: h=map(lambda c: ('Set-Cookie',c),cookies.split('\n'))
    else: h=[]
    rq.start_response(rs, [
      ('content-type', 'text/plain'),
      ('Location', e.kw['location'])]+h)
    return ("Redirect to "+ e.kw['location'],)

# you may customize exceptions like this
#  @expose(response=404,contentType='text/plain; charset=utf-8')
#  def _404(self, rq, e):
#    if not rq.uri: return ('File was not found',)
#    return ('File [%s] was not found' % rq.uri,)

  def __serveStatic(self, rq, fn):
    """
    internal method to serve static files like png, css,js  ...etc.
    """
    if not os.path.exists(fn): raise fileNotFoundException()
    try: f=open(fn,'rb')
    except IOError: raise fileNotFoundException()

    ext=fn[fn.rfind('.'):][1:].lower()
    rq.start_response("200 OK", [('content-type', self._mimeByExtension.get(ext,"application/octet-stream"))])
    # NOTE: since the file object is iteratable then no need for returning [r.read()]
    return f

  def __call__(self, environ, start_response):
    rq=Request(self, environ, start_response)
    if rq.uri==None:
      # handle malformed uri
      return self._handleException(rq, webAppBaseException(500))
    if ALLOW_DEBUG: self._logger.info('got uri=[%s]' % rq.uri)
    if ALLOW_DEBUG: self._logger.debug('got env=[%s]' % rq.environ)
    rq.q._ok_max_files_count=self._max_files_count
    # check if we need to serve static content
    for k in self._staticBaseDirKeys:
      if rq.uri.startswith(k):
        # SECURITY CHECK: that filename is really in side base filename ie. no ".." trick
        # NOTE: no need for this check as it seems to be done by paste
        bfn=self._staticBaseDir[k]
        if os.sep!='/': fn=bfn+rq.uri[len(k):].replace('/',os.sep)
        else: fn=bfn+rq.uri[len(k):]
        if not os.path.abspath(fn).startswith(bfn):
          return self._handleException(rq, forbiddenException())
        try: return self.__serveStatic(rq, fn)
        except webAppBaseException , e:
          return self._handleException(rq, e)
    # check if we need to serve redirect
    for k in self._redirectBaseUrlsKeys:
      if rq.uri.startswith(k):
        u=self._redirectBaseUrls[k]+rq.uri[len(k):]
        # FIXME: should we escape Location in start_response
        start_response("302 Temporary Redirect", [('Location',u),('content-type', 'text/html')])
        return [('<html><body><a href="%s">moved</a></body></html>' % escape(u))]
    # pass control to the right method
    if rq.uriList and not rq.uriList[0].startswith('_') and hasattr(self, rq.uriList[0]):
      f=getattr(self, rq.uriList[0])
      a=rq.uriList[1:]
    else:
      f=self._root
      a=rq.uriList
    try: r=f(rq, *a)
    except webAppBaseException , e:
      return self._handleException(rq, e)
    return r

  @expose()
  def _root(self, rq, *args):
    """
    called when no suitable method is found and it will be called for / too
    """
    return '''<html><body>You requested [<strong>%s</strong>]</body></html>'''% '/'.join(args)

if __name__ == '__main__':
    # this requires python-paste package
    from paste import httpserver
    app=baseWebApp(
      '/path/to/templates/files/',
      staticBaseDir={'/_files/':'/path/to/static/files/'}
    );
    # for options see http://pythonpaste.org/modules/httpserver.html
    httpserver.serve(app, host='127.0.0.1', port='8080')

