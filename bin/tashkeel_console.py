#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tashkeel_console.py
#  
#  Copyright 2020 zerrouki <zerrouki@majd4>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example code using Shakkala library
"""
import os
import sys
import pyarabic.araby as araby

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
        self.limit = 1000000
    def progress(self, compare = True):
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
    def compare(self, baseline, vocalized_output):
        """
        compare base line with automatic vocalized result
        """
        self.lineCorrect = 0
        self.lineWLMIncorrect = 0        
        inputVocalizedLine = baseline
        
        inputlist = araby.tokenize(inputVocalizedLine)
        if type(vocalized_output) == list:
            outputlist = [x.get("chosen", '') for x in vocalized_output]
            result = vocalized_output
            outputlistsemi = [x.get("semi", '') for x in vocalized_output]
        elif type(vocalized_output) == str:
            outputlist =   araby.tokenize(vocalized_output)
            outputlistsemi = [araby.strip_lastharaka(x) for x in outputlist] 
        else:
            print("Incompatible  vocaluzed output, must be dict or string", type(vocalized_output), vocalized_output)
            sys.exit()
            
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
        #~ self.counter += 1
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
            ), end="",
        )
        if self.lineTotal:
            print(
                "%0.2f%%\t" % round(self.lineCorrect * 100.00 / self.lineTotal, 2)
            , end="",
            )  # line Fully correct
            print(
                "%0.2f%%\t" % round((self.lineTotal - self.lineWLMIncorrect) * 100.00 / self.lineTotal, 2)
            )  # line Strip correct
    def footer(self):
        """
        print footer
        """
        sys.stderr.write("\n")
    

if __name__ == "__main__":
    filename = "samples/phrases.txt"
    limit = 20
    try:
        myfile = open(filename, encoding='utf8')
        print("input file:", filename)
    except:
        print(" Can't Open the given File ", filename)
        sys.exit()
    line = myfile.readline().strip()
    counter = 1 
    myconsole = Tashkeel_console() 
    myconsole.limit = limit
    myconsole.header()
    while line and (counter <= limit or not limit):
        text = "فإن لم يكونا كذلك أتى بما يقتضيه الحال وهذا أولى"
        unvoc = araby.strip_tashkeel(line)
        vocalized = unvoc
        myconsole.compare(line, vocalized)
        myconsole.display_line_stat()
        myconsole.progress()
        print(vocalized)
        line = myfile.readline().strip()
        counter += 1
    myconsole.footer()
        


