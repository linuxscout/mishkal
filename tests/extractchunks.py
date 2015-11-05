#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
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
import pyarabic.arabrepr as arabrepr
myrepr  = arabrepr.ArabicRepr()
import qalsadi.analex
import naftawayh.wordtag
MyTagger = naftawayh.wordtag.WordTagger();
import aranasyn.anasyn
import aranasyn.synnode
# lexical analyzer
morphanalyzer = qalsadi.analex.Analex()
# syntaxic analyzer
anasynt = aranasyn.anasyn.SyntaxAnalyzer();
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
def ispunct(word):
    return word and word[0] in u'!"#$%&\'()*+,،-./:;؛،.,<=>?@[\\]^_`{|}~';
def isBreakPrefix(word):
    return word and word[0] in (araby.WAW, araby.BEH, araby.KAF, araby.FEH, araby.LAM);
# tags consants for detecting chunks
_TRANSPARENT ='T'
_MIDDLE         ='I' # inside
_BEGIN         ='B'  # begin
_END          ='O'  # outside
def treatLine(words):
    """ treat one line at once with action"""
    """ split line into words"""
    tmpchunkPos=[]

    for word in words:
        if MyTagger.is_stopword(word):
            tmpchunkPos.append(_BEGIN);
        elif isBreakPrefix(word):
            tmpchunkPos.append(_BEGIN);
        elif ispunct(word):
            # the pounct word is at the clause end
            tmpchunkPos.append(_END);
        else:
            tmpchunkPos.append(_MIDDLE);
    return tmpchunkPos 
def treatLineBySynode(text):
    """ treat one line at once with action
    split line into words"""
    #morpholigical analysis of text
    detailled_stem =  morphanalyzer.check_text(text);
    #syntaxical analysis of text
    detailled_syntax, synnodeList =  anasynt.analyze(detailled_stem);
    # print detailled_syntax;
    syno_tags = u" ‫"
    tmpchunkPos=[]
    for synnode in synnodeList:
        if synnode.is_break():
            tmpchunkPos.append(_BEGIN);
        elif synnode.is_break_end():
            # the pounct word is at the clause end
            tmpchunkPos.append(_END);
        else:
            tmpchunkPos.append(_MIDDLE);
    return tmpchunkPos


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
        limit=    100000000
    else: limit =0;

    nolimit = False;
    line = (myfile.readline()).decode('utf8');

    while line and (nolimit or counter<=limit):
        line = line.strip('\n')
        #line = araby.strip_tashkeel(line.strip('\n'));
        words = araby.tokenize(line);
        chunkPos = treatLineBySynode(line);
        phrase = []
        for tag, word in zip(chunkPos, words):
            #print u'\t'.join([tag, word]).encode('utf8');
            if tag == _BEGIN:
                if len(phrase)>1: 
                    print u" ".join(phrase).encode('utf-8')
                # new phrase
                phrase = [word, ]
                #print word.encode('utf8'),
            elif tag == _MIDDLE:
                phrase.append(word) 

                #print word.encode('utf8');
            else:
                if len(phrase)>1: 
                    print u" ".join(phrase).encode('utf-8')
                phrase=[]
        if phrase:
            if len(phrase)>1: 
               print u" ".join(phrase).encode('utf-8')
            #print u" ".join(phrase).encode('utf-8')
        counter+=1;
        #get the next line
        line=(myfile.readline()).decode('utf8');
