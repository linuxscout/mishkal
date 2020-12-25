#! /usr/bin/python
# -*- coding: UTF-8 -*-


import sys
import re
import string
import datetime
import getopt
import os
# print os.path.abspath(sys.argv[0]);
# dirname = ;
sys.path.append('/opt/mishkal/lib');
sys.path.append('../lib');
# join the actual dirctory to lib path
# print os.path.join(os.path.dirname(sys.argv[0]), 'lib');
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), 'lib'));
# sys.exit();
import pyarabic.araby as araby
import harakatpattern
scriptname = os.path.splitext(os.path.basename(sys.argv[0]))[0]

scriptversion = '0.1'
AuthorName="Taha Zerrouki"
def usage():
# "Display usage options"
	print "(C) CopyLeft 2012, %s"%AuthorName
	print "Usage: %s -f filename [OPTIONS]" % scriptname
	print (u"       %s '' [OPTIONS]\n" % scriptname).encode('utf8');
#"Display usage options"
	print "\t[-f | --file= filename]input file to %s"%scriptname
	print "\t[-h | --help]     outputs this usage message"
	print "\t[-v | --version]  program version"
	print "\n\t* Tashkeel Actions\n\t-------------------"
	print "\t[-s | --strip]    Strip tashkeel (remove harakat)."
	print "\t[-l | --limit]    vocalize only a limited number of line"
	print "\r\nThis program is licensed under the GPL License\n"

def grabargs():
#  "Grab command-line arguments"
	fname = ''
	suggestion=False;
	ignore= False;
	limit=False; 
	compare = False;
	disableSyntax = False;
	disableSemantic = False;
	disableStatistic=  False;
	stripTashkeel = False
	reducedTashkeel = False	
	if not sys.argv[1:]:
		usage()
		sys.exit(0)
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hVtcixsmrv:f:l:",
                               ["help", "version","stat","compare","reduced","strip", "syntax","semantic", "ignore","limit=", "file="],)
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
			stripTashkeel = True
		if o in ("-l", "--limit"):
			try: limit = int(val);
			except: limit=0;

		if o in ("-f", "--file"):
			fname = val
	utfargs=[]
	for a in args:
		utfargs.append( a.decode('utf8'));
	text= u' '.join(utfargs);

	#if text: print text.encode('utf8');
	return (fname, text,  stripTashkeel, limit )

if __name__ == '__main__':
	filename, text,  stripTashkeel, limit =grabargs()
	#filename="samples/randomtext.txt"	
	if not text and not filename:
		usage()
		sys.exit(0)		
	if not text:
		try:
			myfile=open(filename)
		except:
			print " Can't Open the given File ", filename;
			sys.exit();
	else:
		lines = text.split('\n');
	counter=1;
	if not limit : 
		limit=	100000000
	statTable={}
	for i in range(20):
		statTable[i]={};
	nolimit = False;
	if not text:
		line=(myfile.readline()).decode('utf8');
	else:
		if len(lines)>0:
			line= lines[0];
	while line and (nolimit or counter<=limit):
		if not line.startswith('#'):
			# lineIncorrect = 0;
			words=araby.tokenize(line);
			for word in words:
				#print word.encode('utf8');
				pattern= harakatpattern.extractHarakat(word)
				
				patternKey= harakatpattern.extractPattern(word)
				# patternkey is the first level of hashing
				# patternKey=araby.stripTashkeel(pattern);
				length= len(patternKey)
				if statTable[length].has_key(patternKey):
					if statTable[length][patternKey].has_key(pattern):
						statTable[length][patternKey][pattern]+=1;
					else:
						statTable[length][patternKey][pattern]=1
				else:
					statTable[length][patternKey]={pattern:1,};
					# else:
						# statTable[length][patternKey][pattern]+=1;
				# print pattern.encode('utf8');
			counter+=1;
			#display stat for every line
		#get the next line
		if not text:
			line=(myfile.readline()).decode('utf8');
		else:
			if counter<len(lines):
				line= lines[counter];
			else:
				line =None;
	print statTable;
	patternCount=0;
	wordCount=0;	
	for ln in statTable.keys():
		print ln, len(statTable[ln].keys());
		for patternkey in statTable[ln].keys():
			print patternkey.encode('utf8'),u'\t',u'\t'.join(statTable[ln][patternkey].keys()).encode('utf8') 
	for ln in statTable.keys():
		partialPatternCount=0
		for patternkey in statTable[ln].keys():
			partialPatternCount+=len(statTable[ln][patternkey].keys());
		if statTable[ln].keys(): average = partialPatternCount/ len(statTable[ln].keys())
		else: average=0;
		print "\t".join([ str(ln), str(len(statTable[ln].keys())), str(average), 'pw']);
# test vocalize a word
text=u"يأكل الولد التفاح بالعشاء "
words=araby.tokenize(text);
for word in words:
	patternKey= harakatpattern.extractPattern(word)
	ln=len(patternKey)
	if statTable.has_key(ln) and statTable[ln].has_key(patternKey):
		print u"\t".join(statTable[ln][patternKey].keys()).encode('utf8')
		for vocalizedPattern in statTable[ln][patternKey].keys():
			# vocalizedPattern2=araby.stripShadda(vocalizedPattern)
			# letters,harakat = araby.separate(vocalizedPattern2)
			# vocalizedForm =araby.joint(word,harakat)

			letters,harakat, ShaddaPlaces = araby.separate(vocalizedPattern,True)
			newWord_nm =araby.joint(word,ShaddaPlaces)
			vocWord =araby.joint(newWord_nm ,harakat)
			print u"\t".join([word, patternKey, vocalizedPattern,harakat, vocWord]).encode('utf8') 
	else:
		print patternKey.encode('utf8'),"pattern non found";
	
	# print wordCount/patternCount;