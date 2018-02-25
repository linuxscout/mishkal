#! /usr/bin/python2
# -*- coding: UTF-8 -*-

import getopt
import os
import sys
import os.path
import re
from glob import glob
base_dir = os.path.dirname(os.path.realpath(__file__))
#~ sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '../support/'))
#~ sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '../mishkal'))
#~ sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '../')) # used for core
sys.path.append(os.path.join(base_dir, '../support/'))
sys.path.append(os.path.join(base_dir, '../mishkal'))
sys.path.append(os.path.join(base_dir, '../')) # used for core

                
scriptname = os.path.splitext(base_dir)[0]

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
    print "\t[-g | --train]     enable tranining option"
    print "\t[-i | --ignore]   ignore the last Mark on output words."    
    print "\t[-t | --stat]     disable statistic tashkeel"
    print "\r\nThis program is licensed under the GPL License\n"

def grabargs():
#  "Grab command-line arguments"
    options ={ "fname": '', 
    "suggestion" : False, 
    "ignore" : False,
    "limit" : False, 
    "compare" : False,
    "disableSyntax" : False,
    "disableSemantic" : False,
    "disableStatistic" : False,
    "strip_tashkeel" : False,
    "reducedTashkeel" : False,  
    "progress" : False,  
    "train" : False,  
    "nocache" : False,
    "text" : "",
    }
    if not sys.argv[1:]:
        usage()
        sys.exit(0)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hVtgcpixsmnrv:f:l:", 
                               ["help", "version", "stat", "compare", 
                               "reduced", "strip", "syntax", "progress", "semantic", 
                               "ignore", "nocache", "train", "limit=", "file="], )
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
            options["disableSyntax"] = True
        if o in ("-s", "--strip"):
            options["strip_tashkeel"] = True
        if o in ("-r", "--reduced"):
            options["reducedTashkeel"] = True
        if o in ("-m", "--semantic"):
            options["disableSemantic"] = True
        if o in ("-i", "--ignore"):
            options["ignore"] = True
        if o in ("-n", "--nocache"):
            options["nocache"] = True
        if o in ("-c", "--compare"):
            options["compare"] = True
        if o in ("-t", "--stat"):
            options["disableStatistic"] = True
        if o in ("-p", "--progress"):
            options["progress"] = True            
        if o in ("-g", "--train"):
            options["train"] = True            
        if o in ("-l", "--limit"):
            try: options["limit"] = int(val)
            except: options["limit"] = 0

        if o in ("-f", "--file"):
            options["fname"] = val
    utfargs = []
    for a in args:
        utfargs.append( a.decode('utf8'))
    options["text"] = u' '.join(utfargs)

    #if text: print text.encode('utf8')
    return (options)

import tashkeel.tashkeel as ArabicVocalizer

def test():
    options = grabargs()

    filename = options['fname']
    text     = options['text']
    strip_tashkeel  = options['strip_tashkeel']
    nocache         = options['nocache']
    reducedTashkeel = options['reducedTashkeel']
    disableSyntax   = options['disableSyntax']
    disableSemantic = options['disableSemantic']
    disableStat     = options['disableStatistic']
    ignore = options['ignore']
    limit  = options['limit']
    compare = options['compare']
    progress = options['progress']
    enable_syn_train = options['train']
        
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
        if nocache : 
            vocalizer.disable_cache()
            print "nocache"
        if ignore : 
            vocalizer.disable_last_mark()
        if disableSemantic:
            vocalizer.disable_semantic_analysis()
        if disableSyntax:
            vocalizer.disable_syntaxic_analysis()
        if disableStat:
            vocalizer.disable_stat_tashkeel()
        if enable_syn_train:
            vocalizer.enable_syn_train()
            print "mishkal-console, vocalizer.anasynt.syntax_train_enabled", vocalizer.anasynt.syntax_train_enabled

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
        print "id\tfully Correct\tStrip Correct\tfully WER\tStrip WER\tLER\tTotal\tline Fully correct\tline Strip correct\tLine"
        
    while line and (nolimit or counter <= limit):
        if not line.startswith('#'):
            line = line.strip()
            lineCorrect = 0
            lineWLMIncorrect = 0
            if strip_tashkeel:
                result = araby.strip_tashkeel(line)
            else:    #vocalize line by line
                if not compare:
                    result = vocalizer.tashkeel(line)                    
                if compare:
                    inputVocalizedLine = line
                    inputlist = vocalizer.analyzer.tokenize(inputVocalizedLine)
                    inputUnvocalizedLine = araby.strip_tashkeel(line)
                    vocalized_dict = vocalizer.tashkeel_ouput_html_suggest(inputUnvocalizedLine)


                    #stemmer=tashaphyne.stemming.ArabicLightStemmer()
                    #~texts = vocalizer.analyzer.split_into_phrases(inputVocalizedLine)
                    #~inputlist =[]
                    #~for txt in texts:
                        #~inputlist += vocalizer.analyzer.text_tokenize(txt)
                    outputlist = [x.get("chosen",'') for x in vocalized_dict]
                    result = u" ".join(outputlist)
                    outputlistsemi = [x.get("semi",'') for x in vocalized_dict]
                    total += len(inputlist)
                    lineTotal = len(inputlist)
                    if len(inputlist) != len(outputlist):
                        print "lists haven't the same length"
                        print len(inputlist), len(outputlist)
                        print u"#".join(inputlist).encode('utf8')
                        print u"#".join(outputlist).encode('utf8')
                    else:
                        for inword, outword, outsemiword in zip(inputlist, outputlist, outputlistsemi):
                            simi = araby.vocalized_similarity(inword, outword)
                            if simi<0:
                                LettersError += -simi
                                incorrect    += 1
                                # evaluation without last haraka
                                simi2 = araby.vocalized_similarity(inword, outsemiword)
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
        if progress and not nolimit:
            #~percent = (counter * 100/ limit ) if (counter / limit * 100 >percent) else percent
            sys.stderr.write("\r[%d%%]%d/%d lines    Full %0.2f Strip %0.2f     " %(counter * 100/ limit, counter, limit,
                        round(correct*100.00/total, 2), #fully Correct
                        round((total-WLMIncorrect)*100.00/total, 2), #Strip Correct

))
            #~sys.stderr.write("treatment of "+line.encode('utf8'))
            sys.stderr.flush()

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
