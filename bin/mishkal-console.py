#! /usr/bin/python2
# -*- coding: UTF-8 -*-
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
    division,
    )
import os
import os.path

import sys
if sys.version_info.major < 3:
    reload(sys)
    sys.setdefaultencoding('utf-8')
import re
import getopt
from glob import glob
from io import open


base_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(base_dir, '../'))  # used for core
import pyarabic.araby as araby
import mishkal.tashkeel as ArabicVocalizer
scriptname = os.path.splitext(base_dir)[0]

scriptversion = '0.2'
AuthorName = "Taha Zerrouki"
import argparse

def grabargs():
    parser = argparse.ArgumentParser(description='Mishkal : arabic text vocalizer on console .')
    # add file name to import and filename to export
    
    parser.add_argument("-f", dest="filename", required=False,
    help="input file to vocalize", metavar="FILE")
    parser.add_argument("-t", dest="text", required=False,
    help="input text to convert", metavar="TEXT")
    parser.add_argument("-c", dest="command", nargs='?',default="", metavar="COMMAND",
        help="""Command to run : (tashkeel, strip, reduce, compare) """,)    
    parser.add_argument("-o", dest="outfile", nargs='?', 
        help="Output file to convert", metavar="OUTFILE")
   
    parser.add_argument("-l", dest="limit", type=int, nargs='?',default = 1000,
                        help="Limit line to treat", metavar="LIMIT")

    parser.add_argument("--progress", dest="progress", type=bool, nargs='?',default = False, const = True,
                        help="show progress bar", metavar="PROGRESS")
    parser.add_argument("-a",  dest="verbose", type=bool, nargs='?', default = False, const = True,
                        help="enable verbosity", metavar="VERBOSE") 


    # options for Tahkeel
    parser.add_argument("--ignore", dest="ignore", type=bool, nargs='?',default = False, const = True,
                        help="ignore the last Mark on output words.", metavar="IGNORE") 
    parser.add_argument("--syntax", dest="syntax", type=bool, nargs='?',default = False, const = True,
                        help="disable syntaxic analysis", metavar="SYNTAX") 
    parser.add_argument("--semantic", dest="semantic", type=bool, nargs='?',default = False, const = True,
                        help="disable semantic analysis", metavar="SEMANTIC") 
    parser.add_argument("--train", dest="train", type=bool, nargs='?',default = False, const = True,
                        help="enable training options", metavar="TRAIN") 
    parser.add_argument("--stat", dest="stat", type=bool, nargs='?',default = False, const = True,
                        help="disable statistic tashkeel", metavar="STAT")                         
    parser.add_argument("--cache", dest="cache", type=bool, nargs='?',default = False, const = True,
                        help="enable Cache use for tashkeel", metavar="CACHE")                         
    args = parser.parse_args()
    return args
    
class Tashkeel_console:
    def __init__(self,):
        self.correct = 0
        self.incorrect = 0
        self.total = 0
        self.LettersError = 0
        self.WLMIncorrect = 0
        self.lineCorrect = 0
        self.lineWLMIncorrect = 0
        self.total_line = 0
        self.counter = 0
    def progress(self):
        """
        Progress
        """
        pass
    
    def show_progress(self, compare = True):
        """
        Progress bar
        """
        if compare:
            sys.stderr.write(
                "\r[%d%%]%d/%d lines    Full %0.2f Strip %0.2f     " % (
                    self.counter * 100 / self.limit, self.counter, self.limit,
                    round(self.correct * 100.00 / self.total, 2),  # fully Correct
                    round((self.total - self.WLMIncorrect) * 100.00 / self.total, 2)  # Strip Correct
                )
            )
        else:
            sys.stderr.write(
                "\r[%d%%]%d/%d lines " % (
                    self.counter * 100 / self.limit, self.counter, self.limit,
                )
            )
            
        sys.stderr.flush()
    def header(self,):
        # display stats for the current line
        columns = ['id', 'fully Correct', 'Strip Correct', 'fully WER', 'Strip WER',
         'LER', 'Total', 'line Fully correct', 
         'line Strip correct', 'Line']
        print("\t".join(columns))
    def compare(self, line, vocalized_dict):
        inputVocalizedLine = line
        inputlist = araby.tokenize(inputVocalizedLine)
        #~ inputUnvocalizedLine = araby.strip_tashkeel(line)
        #~ vocalized_dict = vocalizer.tashkeel_ouput_html_suggest(inputUnvocalizedLine)
        
        outputlist = [x.get("chosen", '') for x in vocalized_dict]
        result = u" ".join(outputlist)
        outputlistsemi = [x.get("semi", '') for x in vocalized_dict]
        self.total += len(inputlist)
        self.lineTotal = len(inputlist)
        if len(inputlist) != len(outputlist):
            print("lists haven't the same length")
            print(len(inputlist), len(outputlist))
            print(u"# ".join(inputlist).encode('utf8'))
            print(u"# ".join(outputlist).encode('utf8'))
        else:
            for inword, outword, outsemiword in zip(inputlist, outputlist, outputlistsemi):
                simi = araby.vocalized_similarity(inword, outword)
                if simi < 0:
                    self.LettersError += -simi
                    self.incorrect += 1
                    # evaluation without last haraka
                    simi2 = araby.vocalized_similarity(inword, outsemiword)
                    if simi2 < 0:
                        self.WLMIncorrect += 1
                        self.lineWLMIncorrect += 1
                else:
                    self.correct += 1
                    self.lineCorrect += 1
    def display_line_stat(self,):
        print(
            "%d\t%0.2f%%\t%0.2f%%\t%d\t%d\t%d\t%d\t" % (
                self.counter - 1,  # id
                round(self.correct * 100.00 / self.total, 2),  # fully Correct
                round((self.total - self.WLMIncorrect) * 100.00 / self.total, 2),  # Strip Correct
                self.incorrect,  # fully WER
                self.WLMIncorrect,  # Strip WER
                self.LettersError,  # LER
                self.total  # Total
            )
        )
        if self.lineTotal:
            print(
                "%0.2f%%\t" % round(self.lineCorrect * 100.00 / self.lineTotal, 2)
            )  # line Fully correct
            print(
                "%0.2f%%\t" % round((self.lineTotal - self.lineWLMIncorrect) * 100.00 / self.lineTotal, 2)
            )  # line Strip correct
    def footer(self):
        """
        print footer
        """
        sys.stderr.write("\n")
                
def test():
    args = grabargs()

    filename = args.filename
    outfilename = args.outfile
    text = args.text
    if not text and not filename:
        print('Try: mishkal-console.py -h')
        sys.exit(0)
    # tashkeel command
    command = args.command
    strip_tashkeel = False
    compare = False
    reducedTashkeel = False
    commandTashkeel = False
    if command == "strip":
        strip_tashkeel = True
    elif command == "compare":
        compare = True
    elif command == "reduce":
        reducedTashkeel = True
    else:
        commandTashkeel = True
    # general options
    limit = args.limit
    progress = args.progress
    verbose = args.verbose

    # options 
    ignore = args.ignore
    cache = args.cache
    disableSyntax = args.syntax
    disableSemantic = args.semantic
    disableStat = args.stat
    enable_syn_train = args.train

    # Open file
    if not text:
        try:
            myfile = open(filename, encoding='utf8')
            print("input file:", filename)
            if not outfilename:
                outfilename = filename + ".Tashkeel.txt"
            print("output file:", outfilename)
            outfile = open(outfilename, "w")
        except:
            print(" Can't Open the given File ", filename)
            sys.exit()
    else:
        lines = text.split('\n')
    # all things are well, import library

    myconsole = Tashkeel_console()
    #~ myconsole.counter = 1
    myconsole.limit = limit
    if not limit:
        # count lines in files if filename, otherwise count lines in text
        if filename:
            with open(filename) as f:
                limit = sum(1 for line in f)
        else:
            limit = len(lines)
    if not strip_tashkeel:
        vocalizer = ArabicVocalizer.TashkeelClass()
        if cache:
            vocalizer.enable_cache()
            sys.stderr.write(" Mishkal use a cache")
        if ignore:
            vocalizer.disable_last_mark()
        if disableSemantic:
            vocalizer.disable_semantic_analysis()
        if disableSyntax:
            vocalizer.disable_syntaxic_analysis()
        if disableStat:
            vocalizer.disable_stat_tashkeel()
        if enable_syn_train:
            vocalizer.enable_syn_train()
        # if verbose option, then activate logger in ArabicVocalizer
        if verbose:
            vocalizer.enable_verbose()

    if not text:
        line = (myfile.readline())#.decode('utf8')
    else:
        if len(lines) > 0:
            line = lines[0]

    if compare:
        myconsole.header()


    while line and myconsole.counter <= limit:
        line = line.strip()
        myconsole.lineCorrect = 0
        myconsole.lineWLMIncorrect = 0
        if strip_tashkeel:
            result = araby.strip_tashkeel(line)
        #~ else:    # vocalize line by line
        elif not compare:
            result = vocalizer.tashkeel(line)
            myconsole.total += len(araby.tokenize(line))
        elif compare:
            inputUnvocalizedLine = araby.strip_tashkeel(line)
            vocalized_dict = vocalizer.tashkeel_ouput_html_suggest(inputUnvocalizedLine)
            outputlist = [x.get("chosen", '') for x in vocalized_dict]
            result = u" ".join(outputlist)
            myconsole.compare(line, vocalized_dict)
            # display stat for every line
            myconsole.display_line_stat()
        # compare resultLine and vocalizedLine
        if reducedTashkeel:
            result = araby.reduceTashkeel(result)


        if text:
            print(result.strip('\n'), end='')
        else:
            result_line = result
            if verbose:
                print(result_line)
            # add line and new line to output file
            outfile.write(result_line)
            outfile.write("\n")

        if progress:
            # show progress bar
            myconsole.show_progress(compare)

        # get the next line
        if not text:
            line = (myfile.readline())
        else:
            if counter < len(lines):
                line = lines[counter]
            else:
                line = None
        myconsole.counter += 1
    if progress:
        myconsole.footer()


if __name__ == '__main__':
    test()
