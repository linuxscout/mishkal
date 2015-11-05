#!/usr/bin/python
# -*- coding=utf-8 -*-
#************************************************************************
# $Id: conjugate.py, v 0.7 2009/06/02 01:10:00 Taha Zerrouki $
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
"""
Conjugate console
"""

import sys
import getopt
import os
sys.path.append('../')
import libqutrub.mosaref_main as mosaref_main
import libqutrub.ar_verb as ar_verb
import libqutrub.verb_valid as verb_valid

SCRIPT_NAME =  os.path.splitext(os.path.basename(sys.argv[0]))[0]
SCRIPT_VERSION  =  '0.1'
AUTHOR_NAME = "Taha Zerrouki"
def usage():
    """Display usage options"""
    print "(C) CopyLeft 2009, %s" % AUTHOR_NAME
    print "Usage: %s -f filename [OPTIONS]" % SCRIPT_NAME
#"Display usage options"
    print "\t[-h | --help]\toutputs this usage message"
    print "\t[-V | --version]\tprogram version"
    print "\t[-f | --file=filename]\tinput file to %s" % SCRIPT_NAME
    print "\t[-d | --display=format]\tdisplay format as html, csv, tex, xml"
    print "\t[-a | --all ] \tConjugate in all tenses"
    print "\t[-i | --imperative]\tConjugate in imperative"
    print "\t[-F | --future]\tconjugate in the present and the future"
    print "\t[-p | --past]\t conjugate in the past"
    print "\t[-c | --confirmed]  conjugate in confirmed (future or imperative)"
    print """\t[-m | --moode]\tconjugate in future Subjunctive(mansoub) 
    or Jussive (majzoom)"""
    print " \t[-v | --passive] passive form"
    print "\r\nN.B. FILE FORMAT is descripted in README"
    print "\r\nThis program is licensed under the GPL License\n"


def grabargs():
    """Grab command-line arguments"""
    alltense  =  False
    future = False
    past = False
    passive = False
    imperative = False
    confirmed = False
    future_moode = False
    fname  =  ''
    display_format  =  'csv'

    if not sys.argv[1:]:
        usage()
        sys.exit(0)
    try:
        opts, args  =  getopt.getopt(sys.argv[1:], "hVvcmaiFpi:d:f:", 
                               ["help", "version", "imperative", "passive",
                               'confirmed', 'moode', "past", "all", 
                                "future", "file = ", "display = "], )
    except getopt.GetoptError:
        usage()
        sys.exit(0)
    for opt, val in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        if opt in ("-V", "--version"):
            print SCRIPT_VERSION
            sys.exit(0)
        if opt in ("-v", "--passive"):
            passive  =  True
        if opt in ("-f", "--file"):
            fname  =  val
        if opt in ("-d", "--display"):
            display_format  =  val.upper()
        if opt in ("-F", "--future"):
            future  =  True
        if opt in ("-a", "--all"):
            alltense = True
        if opt in ("-p", "--past"):
            past  = True
        if opt in ("-i", "--imperative"):
            imperative = True
        if opt in ("-c", "--confirmed"):
            confirmed = True
        if opt in ("-m", "--moode"):
            future_moode = True

    return (fname, alltense, future, past, passive, imperative, confirmed, 
    future_moode, display_format)

def main():
    """Main function"""
    filename, alltense, future, past, passive, imperative, confirmed, \
     future_moode, display_format =  grabargs()
    try:
        fle = open(filename)
    except IOError:
        print " Error :No such file or directory: %s" % filename
        sys.exit(0)

    print filename, alltense, future, past, passive, imperative, \
     confirmed, future_moode

    line = fle.readline().decode("utf")
    text = u""
    verb_table = []
    nb_field = 2
    while line :
        if not line.startswith("#"):

            text = text+" "+ line.strip()
            liste = line.split("\t")
            if len(liste) >= nb_field:
                verb_table.append(liste)

        line = fle.readline().decode("utf8")
    fle.close()

    for tuple_verb in verb_table:
        word = tuple_verb[0]

        if not verb_valid.is_valid_infinitive_verb(word):
            print u"is invalid verb ", 
            print word.encode("utf8")
        else:
            future_type = u""+tuple_verb[1]
            future_type = ar_verb.get_future_type_entree(future_type)
            transitive = u""+tuple_verb[2]
            if transitive in (u"متعدي", u"م", u"مشترك", u"ك", "t", 
            "transitive"):
                transitive = True
            else :
                transitive = False
            text = mosaref_main.do_sarf(word, future_type, alltense, past, 
            future, passive, imperative, future_moode, confirmed, 
            transitive, display_format)
            print text.encode("utf8")

if __name__  ==  "__main__":
    main()







