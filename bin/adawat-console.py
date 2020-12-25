#! /usr/bin/python
# -*- coding: UTF-8 -*-
"""
Arabic NLP console tools
most tools can be accessed on console
"""
import sys
import getopt
import os

sys.path.append('/opt/mishkal/lib')
# join the actual dirctory to lib path
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '../support/'))
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '../mishkal'))
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '../')) # used for core
  
import core.adaat              
import pyarabic.arabrepr
utf8repr = pyarabic.arabrepr.ArabicRepr() 
scriptname = os.path.splitext(os.path.basename(sys.argv[0]))[0]

scriptversion = '0.1'
AuthorName = "Taha Zerrouki"
def usage():
# "Display usage options"
    print "(C) CopyLeft 2012, %s" % AuthorName
    print "Usage: %s -f filename [OPTIONS]" % scriptname
    print (u"       %s 'السلام عليكم' [OPTIONS]\n" % scriptname).encode('utf8')
#"Display usage options"
    print "\t[-f | --file = filename]input file to %s" % scriptname
    print "\t[-h | --help]     outputs this usage message"
    print "\t[-v | --version]  program version"
    print "\t[-l | --limit]    vocalize only a limited number of line"
    print "\t[-p | --progress]  display progress status"
    print "\t[-c | --command=]  run a specific commane, use help to get command list"
    print "\tActions:"
    print "\t========"
    print "\taffixate   :   generate all word forms by affixation"
    print "\tcollocation:   extract collocations from text "
    print "\tcsv2data   :   convert CSV columns to python data "
    print "\tinverse    :   inverse text"
    print "\tlanguage   :   detect arabic and latin clauses in text"
    print "\tnamed      :   extract named enteties from text"
    print "\tnormalize  :   normalize letters in arabic text"
    print "\tnum2word   :   convert numeric value to words"
    print "\tnumbered   :   extarct numbred clauses from text"
    print "\tpoetry     :   format poetry texts to columns poetry"
    print "\trandom     :   get a random text"
    print "\treduce     :   strip unnecessary tashkeel from  avocalized text "
    print "\tromanize   :   convert an arabic script text to latin representation "
    print "\tspell      :   spellcheck  text  "
    print "\tstem       :   morphology analysis of given texts "
    print "\tstrip      :   remove all harakat and shadda  "
    print "\ttashkeel   :   vocalize  text, we recomand to use mishkal-console instead."
    print "\ttokenize   :   tokenize a text to words"
    print "\tunshape    :   unshape arabic letters"
    print "\twordtag    :   classify words into (nouns, verbs, stopwords)"
    print "\r\nThis program is licensed under the GPL License\n"

def grabargs():
#  "Grab command-line arguments"
    options={
    "filename" : '',
    "limit" :10000000,
    "progress" : False,
    "action":"",
    "text":"",
    } 
    if not sys.argv[1:]:
        usage()
        sys.exit(0)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hVpv:f:l:c:", 
                               ["help", "version", 
                               "progress","command=", "limit=", "file="], )
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
        if o in ("-p", "--progress"):
            options["progress"] = True 
        if o in ("-c", "--command"):
            options["action"] = val
        if o in ("-l", "--limit"):
            try: options["limit"] = int(val)
            except: options["limit"] = 0
        if o in ("-f", "--file"):
            options["filename"] = val
    utfargs = []
    for a in args:
        utfargs.append( a.decode('utf8'))
    options["text"] = u' '.join(utfargs)

    #if text: print text.encode('utf8')
    return options



def test():
    options = grabargs()
    print options
    text = options.get('text', "") 
    filename = options.get("filename",'')
    dict_action ={
    "affixate"    :	"Affixate",
    "collocation"    :	"show_collocations",
    "csv2data"    :	"CsvToData",
    "inverse"    :	"Inverse",
    "language"    :	"Language",
    "named"    :	"extractNamed",
    "normalize"    :"Normalize",	
    "num2word"    :	"NumberToLetters",
    "numbered"    :	"extractNumbered",
    "poetry"    :	"Poetry",
    "random"    :	"RandomText",
    "reduce"    :	"ReduceTashkeel",
    "romanize"    :	"Romanize",
    "stem"      :	"LightStemmer",
    "spell"    :	"SpellCheck",
    "strip"    :	"StripHarakat",
    "tashkeel"    :	"TashkeelText",
    "tokenize"    :	"Tokenize",
    "unshape"    :	"Unshape",
    "wordtag"    :	"Wordtag",
    }

    action = options.get("action",'')
    action = dict_action.get(action, "")
    limit = options.get('limit',1000000)
    progress = options.get('progress',1000000)

    if not text and not filename:
        usage()
        sys.exit(0)
        
    if not text:
        try:
            myfile = open(filename)
        except:
            print " Can't Open the given File ", filename
            sys.exit()
    else:
        lines = text.split('\n')
    counter = 1
    if not limit : 
        limit = 100000000

    nolimit = False
    if not text:
        line = (myfile.readline()).decode('utf8')
    else:
        if len(lines)>0:
            line = lines[0]
    while line and (nolimit or counter <= limit):
        if progress and not nolimit:
            #~percent = (counter * 100/ limit ) if (counter / limit * 100 >percent) else percent
            sys.stderr.write("\r[%d%%]%d/%d lines" %(counter * 100/ limit, counter, limit))
            #~sys.stderr.write("treatment of "+line.encode('utf8'))
            sys.stderr.flush()
        if not line.startswith('#'):
            result = core.adaat.DoAction(line, action)
            counter += 1
            print utf8repr.repr(result).encode('utf8')
        #get the next line
        if not text:
            line = (myfile.readline()).decode('utf8')
        else:
            if counter<len(lines):
                line = lines[counter]
            else:
                line = None
if __name__ == '__main__':
    test()
