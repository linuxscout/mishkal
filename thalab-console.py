#!/usr/bin/python
#-*- coding: UTF-8 -*-
import sys
sys.path.append('/opt/mishkal/lib');
sys.path.append('mishkal/');
sys.path.append('mishkal/lib/');
from itertools import tee, islice, chain, izip

def previous_and_next(some_iterable):
    prevs, items, nexts =  tee(some_iterable, 3)
    prevs =  chain([None], prevs)
    nexts =  chain(islice(nexts, 1, None), [None])
    return izip(prevs, items, nexts)
import re
import string
import datetime
import getopt
import os
# join the actual dirctory to lib path
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), 'lib'));
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), 'mishkal/lib/'));
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), 'mishkal/'));
import pyarabic.araby as araby
import qalsadi.analex
import aranasyn.anasyn
import aranasyn.synnode
scriptname =  os.path.splitext(os.path.basename(sys.argv[0]))[0]
scriptversion =  '0.1'
AuthorName = "Taha Zerrouki"
def usage():
# "Display usage options"
    print "(C) CopyLeft 2012, %s"%AuthorName
    print "Usage: %s -f filename [OPTIONS]" % scriptname
    print (u"       %s 'السلام عليكم' [OPTIONS]\n" % scriptname).encode('utf8');
#"Display usage options"
    print "\t[-f | --file =  filename]input file to %s"%scriptname
    print "\t[-h | --help]     outputs this usage message"
    print "\t[-v | --version]  program version"
    print "\n\t* Tashkeel Actions\n\t-------------------"
    print "\t[-r | --reduced]  Reduced Tashkeel."    
    print "\t[-s | --strip]    Strip tashkeel (remove harakat)."
    print "\t[-c | --compare]  compare the vocalized text with the program output"
    print "\n\t* Tashkeel Options\n\t------------------"
    print "\t[-l | --limit]    vocalize only a limited number of line"
    print "\t[-p | --progress]    show execution progress"
    print "\t[-x | --syntax]   disable syntaxic analysis"
    print "\t[-m | --semantic] disable semantic analysis"
    print "\t[-i | --ignore]   ignore the last Mark on output words."    
    print "\t[-t | --stat]     disable statistic tashkeel"
    print "\r\nThis program is licensed under the GPL License\n"

def grabargs():
#  "Grab command-line arguments"
    fname =  ''
    suggestion = False;
    ignore =  False;
    limit = False; 
    compare =  False;
    disableSyntax =  False;
    disableSemantic =  False;
    disableStatistic =   False;
    stripTashkeel =  False
    reducedTashkeel =  False    
    if not sys.argv[1:]:
        usage()
        sys.exit(0)
    try:
        opts, args =  getopt.getopt(sys.argv[1:], "hVtcixsmrv:f:l:", 
                               ["help", "version", "stat", "compare", "reduced", 
                               "strip", "syntax", "semantic", "ignore", "limit = ", "file = "], )
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
        if o in ("-x", "--syntax"):
            disableSyntax =  True
        if o in ("-s", "--strip"):
            stripTashkeel =  True
        if o in ("-r", "--reduced"):
            reducedTashkeel =  True
        if o in ("-m", "--semantic"):
            disableSemantic =  True
        if o in ("-i", "--ignore"):
            ignore =  True;
        if o in ("-c", "--compare"):
            compare =  True;
        if o in ("-t", "--stat"):
            disableStatistic =  True;
        if o in ("-l", "--limit"):
            try: limit =  int(val);
            except: limit = 0;

        if o in ("-f", "--file"):
            fname =  val
    utfargs = []
    for a in args:
        utfargs.append( a.decode('utf8'));
    text =  u' '.join(utfargs);

    #if text: print text.encode('utf8');
    return (fname, text, stripTashkeel, reducedTashkeel, disableSyntax, disableSemantic, disableStatistic, ignore, limit , compare)

import tashkeel
if __name__ ==  '__main__':
    filename, text, stripTashkeel, reducedTashkeel, disableSyntax, disableSemantic, disableStat, ignore, limit, compare = grabargs()
    #filename = "samples/randomtext.txt"    
    if not text and not filename:
        usage()
        sys.exit(0)        
    if not text:
        try:
            myfile = open(filename)
        except:
            print " Can't Open the given File ", filename;
            sys.exit();
    else:
        lines =  text.split('\n');
    counter = 1;
    if not limit : 
        limit =     100000000
    nolimit =  False;
    if not text:
        line = (myfile.readline()).decode('utf8');
    else:
        if lines:
            line =  lines[0];
            
    # lexical analyzer
    morphanalyzer = qalsadi.analex.Analex()
    # syntaxic analyzer
    anasynt = aranasyn.anasyn.SyntaxAnalyzer();    
    while line and (nolimit or counter <= limit):
        # lineIncorrect =  0;
        #strip harakat from line
        line =  araby.strip_tashkeel(line);
        #split texts into phrases to treat one phrase in time
        texts =  morphanalyzer.split_into_phrases(line);
        # texts = [inputtext, ]
        for texty in texts:
            #morpholigical analysis of text
            detailled_stem =  morphanalyzer.check_text(texty);
            #syntaxical analysis of text
            detailled_syntax, synnodeList =  anasynt.analyze(detailled_stem);
            # print detailled_syntax;
            for synnode in synnodeList:
                if synnode.get_break_type() in ("break", "mostBreak"):
                    print "break";
                print synnode.get_word().encode('utf8'),                 
            for previous, currents, nxt in previous_and_next(detailled_syntax):
                for wordcase in currents:
                    print wordcase.get_word().encode('utf8'), wordcase.get_next();
                    nextWordCasePositions =  wordcase.get_next();
                    previousWordCasePositions =  wordcase.get_previous();

                    if previous and previousWordCasePositions:    
                        for p in previousWordCasePositions:
                            if p <len(previous):
                                if nxt and  nextWordCasePositions:
                                    for n in nextWordCasePositions:
                                        if n<len(nxt):
                                            print u' '.join([ previous[p].get_vocalized(), wordcase.get_vocalized(), nxt[n].get_vocalized(), ]).encode('utf8')
                                        else:
                                            print u' '.join([ previous[p].get_vocalized(), wordcase.get_vocalized()]).encode('utf8')
                                else:
                                    print u' '.join([ previous[p].get_vocalized(), wordcase.get_vocalized()]).encode('utf8')
                    else:
                        if nxt and  nextWordCasePositions:
                            for n in nextWordCasePositions:
                                if n<len(nxt):
                                    print u' '.join([ wordcase.get_vocalized(), nxt[n].get_vocalized(), ]).encode('utf8')
                                else:
                                    print u' '.join([ wordcase.get_vocalized(), ]).encode('utf8')
                        else:
                            print u' '.join([ wordcase.get_vocalized(), ]).encode('utf8')

        counter += 1;
        #get the next line
        if not text:
            line = (myfile.readline()).decode('utf8');
        else:
            if counter<len(lines):
                line =  lines[counter];
            else:
                line = None;

