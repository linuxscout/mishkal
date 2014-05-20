#!/usr/bin/python
# -*- coding=utf-8 -*-
#************************************************************************
# $Id: conjugate.py,v 0.7 2009/06/02 01:10:00 Taha Zerrouki $
#
# ------------
# Description:
# ------------
#  Copyright (c) 2009, Arabtechies, Arabeyes Taha Zerrouki
#
#  This file is the main file to execute the application in the command line
#
# -----------------
# Revision Details:    (Updated by Revision Control System)
# -----------------
#  $Date: 2009/06/02 01:10:00 $
#  $Author: Taha Zerrouki $
#  $Revision: 0.7 $
#  $Source: arabtechies.sourceforge.net
#
#***********************************************************************/

from verb_const import *
# from ar_ctype import *
from classverb import *
from mosaref_main import *
import sys,re,string
import sys, getopt, os
scriptname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
scriptversion = '0.1'
AuthorName="Taha Zerrouki"
def usage():
# "Display usage options"
	print "(C) CopyLeft 2009, %s"%AuthorName
	print "Usage: %s -f filename [OPTIONS]" % scriptname
#"Display usage options"
	print "\t[-h | --help]\t\toutputs this usage message"
	print "\t[-V | --version]\tprogram version"
	print "\t[-f | --file= filename]\tinput file to %s"%scriptname
	print "\t[-d | --display=  format]\t display format as html,csv, tex, xml"
	print "\t[-a | --all ]\t\tConjugate in all tenses"
	print "\t[-i | --imperative]\tConjugate in imperative"
	print "\t[-F | --future]\t\tconjugate in the present and the future"
	print "\t[-p | --past]\t\tconjugate in the past"
	print "\t[-c | --confirmed]\t\tconjugate in confirmed ( future or imperative) "
	print "\t[-m | --moode]\t\tconjugate in future Subjunctive( mansoub) or Jussive (majzoom) "
	print "\t[-v | --passive]\tpassive form";
	print "\r\nN.B. FILE FORMAT is descripted in README"
	print "\r\nThis program is licensed under the GPL License\n"


def grabargs():
#  "Grab command-line arguments"
	all = False;
	future=False;
	past=False;
	passive=False;
	imperative=False;
	confirmed=False;
	future_moode=False;
	fname = ''
	display_format = 'csv'

	if not sys.argv[1:]:
		usage()
		sys.exit(0)
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hVvcmaiFpi:d:f:",
                               ["help", "version","imperative", "passive",'confirmed','moode', "past","all",
                                "future",  "file=","display="],)
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
		if o in ("-v", "--passive"):
			passive = True
		if o in ("-f", "--file"):
			fname = val
		if o in ("-d", "--display"):
			display_format = val.upper();
		if o in ("-F", "--future"):
			future = True
		if o in ("-a", "--all"):
			all=True;
		if o in ("-p", "--past"):
			past =True;
		if o in ("-i","--imperative"):
			imperative=True;
		if o in ("-c","--confirmed"):
			confirmed=True;
		if o in ("-m","--moode"):
			future_moode=True;

	return (fname,all,future,past,passive,imperative,confirmed,future_moode,display_format)

def main():
	filename,all,future,past,passive,imperative,confirmed,future_moode,display_format= grabargs()
	try:
		fl=open(filename);
	except:
		print " Error :No such file or directory: %s" % filename
		sys.exit(0)

	print filename,all,future,past,passive,imperative,confirmed,future_moode

	line=fl.readline().decode("utf");
	text=u""
	verb_table=[];
	nb_field=2;
	while line :
		if not line.startswith("#"):

			text=text+" "+chomp(line)
			liste=line.split("\t");
			if len(liste)>=nb_field:
				verb_table.append(liste);

		line=fl.readline().decode("utf8");
	fl.close();

	for tuple_verb in verb_table:
		word=tuple_verb[0];

		if not is_valid_infinitive_verb(word):
		    print u"is invalid verb ",
		    print word.encode("utf8")
		else:
			future_type=u""+tuple_verb[1];
			future_type=get_future_type_entree(future_type);
			transitive=u""+tuple_verb[2];
			if transitive in (u"متعدي",u"م",u"مشترك",u"ك","t","transitive"):
			    transitive=True;
			else :
			    transitive=False;
			text=do_sarf(word,future_type,all,past,future,passive,imperative,future_moode,confirmed,transitive,display_format);
			print text.encode("utf8")

if __name__ == "__main__":
  main()







