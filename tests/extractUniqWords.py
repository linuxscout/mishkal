#! /usr/bin/python
# -*- coding: UTF-8 -*-
import sys
sys.path.append('/opt/mishkal/lib');
sys.path.append('mishkal/');
sys.path.append('mishkal/lib/');

import re
import string
import datetime
import getopt
import os
# join the actual dirctory to lib path
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '../lib'));
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '../mishkal/lib/'));
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '../mishkal/'));
import pyarabic.araby as araby
import qalsadi.analex
import aranasyn.anasyn
import aranasyn.synnode
scriptname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
scriptversion = '0.1'
WordsTab={}
globalFreq =0
AuthorName="Taha Zerrouki"
def usage():
# "Display usage options"
	print "(C) CopyLeft 2012, %s"%AuthorName
	print "Usage: %s -f filename [OPTIONS]" % scriptname
	print (u"       %s 'السلام عليكم' [OPTIONS]\n" % scriptname).encode('utf8');
#"Display usage options"
	print "\t[-f | --file= filename]input file to %s"%scriptname
	print "\t[-h | --help]     outputs this usage message"
	print "\t[-v | --version]  program version"
	print "\n\t* Extraxtion Actions\n\t-------------------"
	print "\t[-s | --strip]    Last Mark (remove harakat)."
	print "\t[-c | --full]  extract words with full vocalization"
	print "\t[-r | --reduce]  extract and classify words"
	print "\n\t* Tashkeel Options\n\t------------------"
	print "\t[-l | --limit]    vocalize only a limited number of line"
	print "\t[-t | --stat]     enable statistics display"
	print "\r\nThis program is licensed under the GPL License\n"

def grabargs():
#  "Grab command-line arguments"
	fname = ''
	options={
	'strip':False,
	'full':False,
	'limit':False,
	'stat':False,
	'reduce':False,
}
	if not sys.argv[1:]:
		usage()
		sys.exit(0)
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hVtcixsmrv:f:l:",
                               ["help", "version","stat","full","strip","reduce", "limit=", "file="],)
	except getopt.GetoptError:
		usage()
		sys.exit(0)
	for o, val in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit(0)
		if o in ("-V", "--version"):
			print scriptversion
			sys.exit(0)
		if o in ("-s", "--strip"):
			options['strip'] = True
		if o in ("-c", "--full"):
			options['full'] = True
		if o in ("-r", "--reduce"):
			options['reduce'] = True
		if o in ("-t", "--stat"):
			options['stat'] = True;
		if o in ("-l", "--limit"):
			try: options['limit'] = int(val);
			except: options['limit']=0;

		if o in ("-f", "--file"):
			fname = val
	utfargs=[]
	for a in args:
		utfargs.append( a.decode('utf8'));
	text= u' '.join(utfargs);

	#if text: print text.encode('utf8');
	return (fname, options)

def stringToInt(word):
	try: 
		return int(word);
	except: return 0;
def extract(word):
	"""
	"""
	#print word.encode('utf8');
	if araby.isArabicword(word):
		print araby.stripLastHaraka(word).encode('utf8');
def treatLine(line, action):
	""" treat one line at once with action"""
	global globalFreq
	if action == "extract":
		words=araby.tokenize(line);
		for word in words:
			extract(word);
	elif action =="reduce":
		line= line.strip(' ');
		fields=line.split(' ');
		if len(fields)>=2:
			freq = fields[0]
			word = fields[1]
			word_nm = araby.stripTashkeel(word);
			if WordsTab.has_key(word_nm): # the word has multiple vocalization
				WordsTab[word_nm]=False;
			else:
				WordsTab[word_nm]={'f':freq,'v':word} ;	
			globalFreq += stringToInt(freq);

			

	
if __name__ == '__main__':
	filename, options =grabargs()
	
	if not filename:
		usage()
		sys.exit(0)		

	try:
		myfile=open(filename)
	except:
		print " Can't Open the given File ", filename;
		sys.exit();
	counter=1;
	if not options['limit'] : 
		limit=	100000000
	else: limit =0;

	nolimit = False;
	line=(myfile.readline()).decode('utf8');
	action='extract'
	if options['reduce'] == True:
		action ="reduce";
	while line and (nolimit or counter<=limit):
		line = line.strip('\n')
		treatLine(line, action);
			#print word.encode('utf8');
			#print araby.stripLastHaraka(word).encode('utf8');

		counter+=1;
		#get the next line
		line=(myfile.readline()).decode('utf8');
	if action == "reduce":
		print globalFreq;
		uniqWordFreq = 0;
		for key in WordsTab.keys():
			if WordsTab[key]:
				print u'\t'.join([WordsTab[key]['f'], key, WordsTab[key]['v'],  ]).encode('utf8') ;
				uniqWordFreq += stringToInt (WordsTab[key]['f']);
		print "Global words Count:", globalFreq
		print "Unique words Count:", uniqWordFreq
		print "%", round(float(uniqWordFreq*100.00/(globalFreq+1)),2);

 
			
