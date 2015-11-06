# -*- coding: UTF-8 -*-
"""

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
import sys, time, hashlib, random
import bisect
from itertools import groupby,imap
import re

dD_re=re.compile(ur'(\d+|\D+)')

def stringOrFloat(s):
  try: return float(s)
  except ValueError: return s

def strverscmp(a,b):
  "something like GNU strverscmp"
  return cmp([stringOrFloat(i) for i in dD_re.findall(a)],
    [stringOrFloat(i) for i in dD_re.findall(b)])


def fromFs(filenameblob):
  """
  recives a blob encoded in filesystem encoding and convert it into a unicode object
  """
  if type(filenameblob)!=unicode:
  	return filenameblob.decode(sys.getfilesystemencoding())
  return filenameblob

def toFs(filename):
  """
  recives a unicode object and encode it into filesystem encoding
  """
  if type(filename)==unicode:
  	return filename.encode(sys.getfilesystemencoding())
  return filename


def randomblob(m,M):
  return ''.join(map(lambda i: chr(random.randrange(0,255)), range(random.randrange(m,M))))


def safeHash(stringSeed, o):
  """
  a URL safe hash, it results a 22 byte long string hash based on md5sum
  """
  if isinstance(o,unicode): o=o.encode('utf8')
  return hashlib.md5(stringSeed+o).digest().encode('base64').replace('+','-').replace('/','_')[:22]

# TODO: is this needed by anything ?
def unixUniq(l):
  """
  Unix-like uniq, the iteratable argument should be sorted first to get unique elements.
  """
  return imap(lambda j:j[0],groupby(l,lambda i: i))

def unixUniqAndCount(l):
  """
  Unix-like uniq -c, it returns an iteratable of tuples (count, uniq_entry)
  """
  return imap(lambda j:(len(list(j[1])),j[0]),groupby(l,lambda i: i))

class ObjectsCacheObject:
  def __init__(self, objId, obj):
    self.objId=objId
    self.obj=obj
    self.atime=self.ctime=time.time()
    self.freq=1 # how many time it was accessed
    self.i=0 # shifted index

  def __cmp__(self, b):
    # passing cmp as an argument is twise as faster as overloading cmp
    if isinstance(b,ObjectsCacheObject): return cmp(self.atime,b.atime)
    if b<=0: return cmp(self.i,-b)
    return cmp(self.atime,b)

def cmp_bisect_right(ccmp, a, x, lo=0, hi=None):
    """
    same as bisect.bisect but uses custom cmp function
    """
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)>>1
        if ccmp(a[mid],x)>0: hi = mid # ie. if x < a[mid]
        else: lo = mid+1
    return lo
def cmp_bisect_left(ccmp, a, x, lo=0, hi=None):
    """
    same as bisect.bisect_left but uses custom cmp function
    """
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)>>1
        if ccmp(x, a[mid])>0: lo = mid+1 # ie. if a[mid] < x
        else: hi = mid
    return lo

class fakeLock:
  def acquire(self, blocking=True): pass
  def release(self): pass

class ObjectsCache:
  _feasible_bisect_limit=4
  def __init__(self, lock=None, minCount=10, maxCount=100, maxTime=3600):
    """
    minCount is the minimum number of cached objects below which no cached object will be freed, use 0 to set no lower limit
    maxCount is the maximum number of cached objects above which no cached object will be kept, use 0 to set no upper limit
    maxTime is positive time to live in seconds, all objects older than this will be removed when free is called, use 0 to discard time checking
    
    example:
      setting minCount and maxTime to 0 will keep all cached objects no matter how many or for how long
      setting maxCount to 0 will disable caching (all objects will be freed when free is called)
    """
    if not lock: self._lock=fakeLock()
    else: self._lock=lock
    self.maxTime=maxTime
    self.maxCount=maxCount
    self.minCount=minCount
    self._hash={} # a mapping between ids and shifted array index
    self._shift=0 # the current shift in array index
    self._shifts=0 # number of tailing shifts done
    self.objs=[] # objects list from older to most recent
    # when freeing old objects we don't need to update the mapping between ids and array index, we only adjust the shift

  def _get(self, objId):
    i=self._hash.get(objId,None)
    if i==None: return None
    si=min(i+self._shift,len(self.objs)-1)
    # NOTE: withou tailing shifts it would be o=self.objs[si]
    # because of Tailing Shifts we need to search between objs[si-shifts:si]
    # in case of shifts==0 then the object is at si
    # if shifts>0 then the worst case is that our very object was the target of all past tailing shifts, ie. it's on objs[si-shifts]
    # NOTE: worst case happens when one keep accessing the least expected object and this can only happen if the user access all objects in a uniform way
    cb=si-self._shifts # candidates lower bound
    if cb<0: cb=0
    if si-cb<self._feasible_bisect_limit:
      sh=si
      while(True): # should be sh>=cb but it's guaranteed to work without it
        o=self.objs[sh]
        if o.i==i: break
        sh-=1
    else:
      sh=cb+cmp_bisect_left(lambda a,b: cmp(a,b.i), self.objs[cb:si+1],i)
      o=self.objs[sh]
    o.atime=time.time()
    o.freq+=1
    # Tailing shifts should be done if o is not the last one
    # change position from: oldest,older,*accessed*,old, recent
    # to be something like: oldest,older,old, recent, *accessed*
    # this will case the shifted index returned from hash of old and recent to be greater than its real value
    if sh<len(self.objs)-1:
      self._shifts+=1
      del self.objs[sh]
      if self.objs: i=self.objs[-1].i+1
      else: i=0
      self._hash[objId]=i
      o.i=i
      self.objs.append(o)
    self._free()
    return o.obj

  def get(self, objId):
    self._lock.acquire()
    try: o=self._get(objId)
    finally: self._lock.release()
    return o

  def append(self, objId, obj):
    self._lock.acquire()
    try:
      if self._hash.has_key(objId):
        # replace it
        self._get(objId) # this will make it last object
        # remove it
        del self.objs[-1]
        del self._hash[objId]
      else: self._free()
      # add it
      o=ObjectsCacheObject(objId, obj)
      if self.objs: i=self.objs[-1].i+1
      else: i=0
      self._hash[objId]=i
      o.i=i
      self.objs.append(o)
    finally: self._lock.release()

  def free(self):
    """
    free old objects, return number of freed objects
    """
    self._lock.acquire()
    try:
      r=self._free()
    finally: self._lock.release()
    return r

  def _free(self):
    """
    the real internal free is done here without locks, locks are done in free()
    """
    # if there are too many tailing shifts then reconstruction would be feasible
    # or if there are 
    if len(self.objs)>self._feasible_bisect_limit and (self._shifts>>1)>len(self.objs): self._reconstruct()
    # TODO: also if the oldest element is older than some limit an expensive reconstruction based on frequency maybe feasible
    l=len(self.objs)
    if self.minCount>0 and l<=self.minCount: return 0
    k=l-self.minCount # max number of objs to remove
    j=max(l-self.maxCount,0) # number of objs to remove
    if self.maxTime>0:
      c=time.time()-self.maxTime # time older than which should be removed
      i=cmp_bisect_right(lambda a,b: cmp(a.atime,b),self.objs,c) # number of objs to remove by time
      i=max(i,j)
    else: i=j
    if self.minCount>0: i=min(j,k)
    # can be done by deleting hash elements which has values < -newshift
    for o in self.objs[:i]: del self._hash[o.objId]
    del self.objs[:i]
    self._shift-=i
    return i

  def _reconstruct(self):
    """
    reconstruct objects so that no shifting is used,
    this expensive operation O(n) might speed things up for next retrievals
    """
    for i,o in enumerate(self.objs):
      o.i=i; self._hash[o.objId]=i
    self._shift=0; self._shifts=0

