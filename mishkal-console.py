#! /usr/bin/python
# -*- coding: UTF-8 -*-

import getopt
import os
import sys
import os.path
import re
from glob import glob

sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), 'mishkal/lib/'))
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), 'mishkal'))


                
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
    print "\t[-p | --progress]  display progress status"
    print "\n\t* Tashkeel Actions\n\t-------------------"
    print "\t[-r | --reduced]  Reduced Tashkeel."    
    print "\t[-s | --strip]    Strip tashkeel (remove harakat)."
    print "\t[-c | --compare]  compare the vocalized text with the program output"
    print "\n\t* Tashkeel Options\n\t------------------"
    print "\t[-l | --limit]    vocalize only a limited number of line"
    print "\t[-x | --syntax]   disable syntaxic analysis"
    print "\t[-m | --semantic] disable semantic analysis"
    print "\t[-i | --ignore]   ignore the last Mark on output words."    
    print "\t[-t | --stat]     disable statistic tashkeel"
    print "\r\nThis program is licensed under the GPL License\n"

def grabargs():
#  "Grab command-line arguments"
    fname = ''
    suggestion = False
    ignore = False
    limit = False 
    compare = False
    disableSyntax = False
    disableSemantic = False
    disableStatistic = False
    strip_tashkeel = False
    reducedTashkeel = False  
    progress = False  
    if not sys.argv[1:]:
        usage()
        sys.exit(0)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hVtcpixsmrv:f:l:", 
                               ["help", "version", "stat", "compare", 
                               "reduced", "strip", "syntax", "progress", "semantic", 
                               "ignore", "limit=", "file="], )
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
            disableSyntax = True
        if o in ("-s", "--strip"):
            strip_tashkeel = True
        if o in ("-r", "--reduced"):
            reducedTashkeel = True
        if o in ("-m", "--semantic"):
            disableSemantic = True
        if o in ("-i", "--ignore"):
            ignore = True
        if o in ("-c", "--compare"):
            compare = True
        if o in ("-t", "--stat"):
            disableStatistic = True
        if o in ("-p", "--progress"):
            progress = True            
        if o in ("-l", "--limit"):
            try: limit = int(val)
            except: limit = 0

        if o in ("-f", "--file"):
            fname = val
    utfargs = []
    for a in args:
        utfargs.append( a.decode('utf8'))
    text = u' '.join(utfargs)

    #if text: print text.encode('utf8')
    return (fname, text, strip_tashkeel, reducedTashkeel, disableSyntax, 
    disableSemantic, disableStatistic, ignore, limit , compare, progress)

import tashkeel.tashkeel as ArabicVocalizer

def test():
    filename, text, strip_tashkeel, reducedTashkeel, disableSyntax, \
    disableSemantic, disableStat, ignore, limit, compare, progress = grabargs()
    #filename = "samples/randomtext.txt"    
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
    # all things are well, import library
    import core.adaat 
    import pyarabic.araby as araby

    counter = 1
    if not limit : 
        limit = 100000000
    if not strip_tashkeel: 
        vocalizer = ArabicVocalizer.TashkeelClass()
        if ignore : 
            vocalizer.disable_last_mark()
        if disableSemantic:
            vocalizer.disable_semantic_analysis()
        if disableSyntax:
            vocalizer.disable_syntaxic_analysis()
        if disableStat:
            vocalizer.disable_stat_tashkeel()

    #vocalizer.disableShowCollocationMark()
    #print "show delimiter", vocalizer.collo.showDelimiter
    #nolimit = True
    nolimit = False
    if not text:
        line = (myfile.readline()).decode('utf8')
    else:
        if len(lines)>0:
            line = lines[0]
    correct = 0
    incorrect = 0
    total = 0
    totLetters = 0
    LettersError = 0
    WLMIncorrect = 0
    percent = 0
    if compare:
        #dispaly stats for the current line
        print "id\tfully Correct\tStrip Correct\tfully WER\tStrip WER\tLER\tTotal\tline Fully correct\tline Strip correct"
        
    while line and (nolimit or counter <= limit):
        if progress and not nolimit:
            #~percent = (counter * 100/ limit ) if (counter / limit * 100 >percent) else percent
            sys.stderr.write("\r[%d%%]%d/%d lines" %(counter * 100/ limit, counter, limit))
            #~sys.stderr.write("treatment of "+line.encode('utf8'))
            sys.stderr.flush()
        if not line.startswith('#'):
            # lineIncorrect = 0
            lineCorrect = 0
            lineWLMIncorrect = 0
            if strip_tashkeel:
                result = araby.strip_tashkeel(line)
            else:    #vocalize line by line
                if compare:
                    vocalizedLine = line
                    line = araby.strip_tashkeel(line)
                result = vocalizer.tashkeel(line)
                #compare resultLine and vocalizedLine
                if compare:
                    list1 = vocalizer.analyzer.tokenize(vocalizedLine)
                    list2 = vocalizer.analyzer.tokenize(result)
                    total += len(list1)
                    lineTotal = len(list1)
                    if len(list1) != len(list2):
                        print "lists haven't the same length"
                    else:
                        for i in range(len(list1)):
                            simi = araby.vocalized_similarity(list1[i], 
                                    list2[i])
                            if simi<0:
                                LettersError += -simi
                                incorrect    += 1
                                # lineIncorrect  += 1
                                # evaluation without last haraka
                                simi2 = araby.vocalized_similarity(
                                araby.strip_lastharaka(list1[i]), 
                                araby.strip_lastharaka(list2[i]))
                                if simi2<0: 
                                    WLMIncorrect     += 1
                                    lineWLMIncorrect += 1                                

                            else:
                                correct += 1
                                lineCorrect  += 1
                    
            #compare resultLine and vocalizedLine
            if reducedTashkeel:
                result = araby.reduceTashkeel(result)
            # print result.encode('utf8')
            counter += 1

            #display stat for every line
            if compare:
                print "%d\t%0.2f%%\t%0.2f%%\t%d\t%d\t%d\t%d\t"%(
                        counter-1, #id
                        round(correct*100.00/total, 2), #fully Correct
                        round((total-WLMIncorrect)*100.00/total, 2), #Strip Correct
                        incorrect, #fully WER
                        WLMIncorrect, #Strip WER
                        LettersError, #LER
                        total, #Total
                        ), 
                if lineTotal:
                    print "%0.2f%%\t"%round(lineCorrect*100.00/lineTotal, 2), #line Fully correct
                    print "%0.2f%%\t"%round((lineTotal-lineWLMIncorrect)*100.00/lineTotal, 2), #line Strip correct
                        
            print result.encode('utf8')
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
