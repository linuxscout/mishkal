#!/usr/bin/python # -*- coding = utf-8 -*- 
#---------------------------------------------------------------------
# Name:        tashkeel 
# Purpose:     Arabic automatic vocalization. # 
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com) 
# Created:     31-10-2011 
#  Copyright:   (c) Taha Zerrouki 2011 # Licence:     GPL 
#---------------------------------------------------------------------
"""
    Arabic Tashkeel Class
"""
import sys
sys.path.append('../lib')
sys.path.append('../')
import re
import pyarabic.araby as araby
import tashkeel_const
import qalsadi.analex
import aranasyn.anasyn 
import asmai.anasem 
import maskouk.collocations as coll
import pyarabic.number
import pyarabic.named
# to debug program
debug = True
class TashkeelClass:
    """
        Arabic Tashkeel Class
    """
    def __init__(self):
        # to display internal messages for debugging
        #~debug = False
        # limit of words to vocalize, default value is 1000 words.
        self.limit = 1000
        
        #  set the option value to enable the Last mark on voaclize 
        # words in output
        # default value is True, can be disabled for debuging porpus
        self.enabled_last_mark = True
        
        # set the option to do statistical vocalization based 
        # on collocations
        # default value is True, can be disabled for debuging porpus
        self.enabled_stat_tashkeel = True    
            
        # set the option to show the collocations marks
        # default value is False, can be enabled for debuging porpus
        self.enabled_show_collocation_mark = False
        
        # set the option to use scoring teashkeel chosing.
        self.select_by_score_enabled = False
        # set the option to do syntaxic Analysis
        # default value is True, can be disabled for debuging porpus
        self.enabled_syntaxic_analysis = True

        # set the option to do allow ajusting voaclization result, 
        # for التقاء الساكنين
        # default value is True, can be disabled for debuging porpus
        self.enabled_ajust_vocalization = True        

        # set the option to do Semantic Analysis
        # default value is True, can be disabled for debuging porpus        
        self.enabled_semantic_analysis = True

        # enable the last mark (Harakat Al-I3rab) 
        self.allow_syntax_last_mark = True 

        # lexical analyzer
        self.analyzer = qalsadi.analex.Analex()

        # syntaxic analyzer
        self.anasynt = aranasyn.anasyn.SyntaxAnalyzer()
        # semantic analyzer
        self.anasem = asmai.anasem.SemanticAnalyzer()        
        #set the lexical analzer debugging
        self.analyzer.set_debug(debug)
        #set the lexical analzer  word limit
        self.analyzer.set_limit(self.limit)
        #collocations dictionary for statistical tashkeel
        self.collo = coll.CollocationClass(self.enabled_show_collocation_mark)

    
    def set_limit(self, limit):
        """
        set the limit length of words to vocalize
        """
        self.limit = limit
        #set the lexical analzer  wrd limit
        self.analyzer.set_limit(self.limit)

    def enable_stat_tashkeel(self):
        """
        Enable the stat tasheel option.
        """
        self.enabled_stat_tashkeel = True
    def disable_stat_tashkeel(self):
        """
        disable the stat tasheel option.
        """
        self.enabled_stat_tashkeel = False
    def get_enabled_stat_tashkeel(self):
        """
        return the  the stat tasheel option value.
        @return: True if enabled, false else.
        @rtype: boolean.
        """
        return self.enabled_stat_tashkeel
    def enable_show_collocation_mark(self):
        """
        Enable the show the collocation mark option.
        """
        self.enabled_show_collocation_mark = True
        self.collo.enable_show_delimiter()
    def disable_show_collocation_mark(self):
        """
        disable the show the collocation mark option.
        """
        self.enabled_show_collocation_mark = False
        self.collo.disable_show_delimiter()
    def get_show_collocation_mark(self):
        """
        return the  the show the collocation mark option value.
        @return: True if enabled, false else.
        @rtype: boolean.
        """
        return self.enabled_show_collocation_mark
    def enable_last_mark(self):
        """
        Enable the last mark option.
        """
        self.enabled_last_mark = True
    def disable_last_mark(self):
        """
        disable the last mark vocalization  option.
        """
        self.enabled_last_mark = False
    def get_enabled_last_mark(self):
        """
        return the  the last mark vocalization option value.
        @return: True if enabled, false else.
        @rtype: boolean.
        """
        return self.enabled_last_mark
    def enable_syntaxic_analysis(self):
        """
        Enable the syntaxic analysis option.
        """
        self.enabled_syntaxic_analysis = True
    def disable_syntaxic_analysis(self):
        """
        disable the syntaxic analysis option.
        """
        self.enabled_syntaxic_analysis = False
    def get_enabled_syntaxic_analysis(self):
        """
        return the  the syntaxic analysis option value.
        @return: True if enabled, false else.
        @rtype: boolean.
        """
        return self.enabled_syntaxic_analysis
    def enable_semantic_analysis(self):
        """
        Enable the Semantic analysis option.
        """
        self.enabled_semantic_analysis = True
    def disable_semantic_analysis(self):
        """
        disable the Semantic analysis option.
        """
        self.enabled_semantic_analysis = False
    def get_enabled_semantic_analysis(self):
        """
        return the  the Semantic analysis option value.
        @return: True if enabled, false else.
        @rtype: boolean.
        """
        return self.enabled_semantic_analysis
    def enable_ajust_vocalization(self):
        """
        Enable the Ajust Vocalization option.
        """
        self.enabled_ajust_vocalization = True
    def disable_ajust_vocalization(self):
        """
        disable the Ajust Vocalization option.
        """
        self.enabled_ajust_vocalization = False
    def get_enabled_ajust_vocalization(self):
        """
        return the  the Ajust Vocalization option value.
        @return: True if enabled, false else.
        @rtype: boolean.
        """
        return self.enabled_ajust_vocalization

    def full_stemmer(self, text):
        """
        Do the lexical, syntaxic  and semantic analysis of the text.
        @param text: input text.
        @type text: unicode.
        @return: syntaxic and lexical tags.
        rtype: list of list of stemmedSynWord class.
        """
        result = []
        result = self.analyzer.check_text(text)
        if self.get_enabled_syntaxic_analysis():
            result, synodelist = self.anasynt.analyze(result)
            # in this stpe we can't do semantic analysis without 
            # syntaxic analysis
            # we think it's can be done, 
            # To do: do semantic analysis without syntaxic one
            if self.get_enabled_semantic_analysis():
                result = self.anasem.analyze(result)    
        return result, synodelist

    def tashkeel(self, inputtext, suggestion = False, format_display = 'text'):
        """
        Vocalize the text and give suggestion to improve tashkeel by user.
        @param text: input text.
        @type text: unicode.
        @return: vocalized text.
        rtype: dict of dict or text.
        """
        inputtext = self.pre_tashkeel(inputtext)
        # print "PreTashkeel", inputtext.encode('utf8')
        # The statistical tashkeel must return a text.
        #comment this after tests
        if self.get_enabled_stat_tashkeel():
            inputtext = self.stat_tashkeel(inputtext)
    
        #split texts into phrases to treat one phrase in time
        texts = self.analyzer.split_into_phrases(inputtext)
        # texts = [inputtext, ]
        vocalized_text = u""
        previous = None
        output_suggest_list = []
        _chosen_list = []    
        suggests_list = []    
        for text in texts:
            
            #morpholigical analysis of text
            detailled_syntax, synodelist = self.full_stemmer(text)

            previous = None
            next_node = None
            pre_node = None
            for word_cases_list in detailled_syntax:

                current_chosen = self._choose_tashkeel(word_cases_list, 
                previous, pre_node, next_node)
                # ajust tanwin case
                # if previous and previous.canhave_tanwin() and not 
                # self.anasynt.is_related(previous, current_chosen):
                    # #vocalized_text += "1"
                    # _chosen_list[len(_chosen_list)-1].ajust_tanwin() 
                # o ajust relation between words
                # if the actual word is transparent don't change the previous
                # add this to Sytaxic Analyser
                if not current_chosen.is_transparent():
                    previous = current_chosen
                _chosen_list.append(current_chosen)

                # create a suggest list
                suggest = []
                for item in word_cases_list:
                    # ITEM IS A stemmedSynWord instance
                    voc = item.get_vocalized()
                    suggest.append(voc)
                    # if item.canhave_tanwin():
                        # # يمكن لهذا أن يولد صيغا جديدة بها تنوي
                        # # في بعض الحالات قد لا يكون شيئا جديدا 
 # # نقارنه مع الكلمة السابقة منوّنة
# ومن ثمّ نقرر إضافتها أولا
                        # item.ajust_tanwin()
                        # vocTnwn = item.get_vocalized()
                        # if vocTnwn! = voc:
                            # suggest.append(vocTnwn)
                suggest.sort()
                suggests_list.append(suggest)
        output_suggest_list = []
        #create texts from chosen cases
        for i in range(len(_chosen_list)):
            word = _chosen_list[i].get_vocalized()
            # omit the last haraka if the option LastMark is False
            if not self.get_enabled_last_mark():
                word = araby.strip_lastharaka(word)
            vocalized_text = u" ".join([vocalized_text, 
            self.display(word, format_display)])
            output_suggest_list.append({'chosen':word, 
            'suggest':u";".join(suggests_list[i])})
        
        # correct the resulted text to ajust some case of consonant neighbor
        #معالجة حالات التقاء الساكنين
        if self.get_enabled_ajust_vocalization():
            vocalized_text = self._ajust_vocalized_result(vocalized_text)
        if suggestion:
            output_suggest_list = self.ajust_vocalized_suggestion(
            output_suggest_list)
            return output_suggest_list
        else:
            return vocalized_text

    def _choose_tashkeel(self, curcaseslist, previous_chosen_case = None,
     pre_node = None, next_node = None):
        """
        Choose a tashkeel for the current word, according to the previous one.
        @param : list of steming result of the word.
        @type curcaseslist: list of stemmedSynword
        @param : the choosen previous word stemming.
        @type previous_chosen_case:stemmedSynword
        @return: the choosen stemming of the current word.
        @rtype:stemmedSynword.
        """
        # toDo
        #curcaseslist = self.anasynt.is_related(previous_chosen_case,
        # curcaseslist)

        # select the first chosen tashkeel
        # if len(curcaseslist)>0:
            # chosen = curcaseslist[0]
        chosen = None
        previous = previous_chosen_case
        # test selct by score
        if self.select_by_score_enabled:
            chosen = self._select_by_score(curcaseslist, previous)
            if chosen:
                return chosen 
        chosen = False
        # and lets other methode to choices by semantic and syntaxic
        if not previous or previous.is_initial():
            curcaseslist = self._filter_for_initial(curcaseslist)

        # print "before Semantic", len(curcaseslist)
        if  self.get_enabled_syntaxic_analysis() and \
        self.get_enabled_semantic_analysis():
            curcaseslist = self._filter_by_semantic(curcaseslist,
             previous)

        # filter results accorind to  word frequency
        # print "After Semantic", len(curcaseslist)        
        if  self.get_enabled_syntaxic_analysis():
            curcaseslist = self._filter_by_syntaxic(curcaseslist,
             previous)
            # print "After Syntax", len(curcaseslist)
            curcaseslist = self._frequency_filter(curcaseslist)
        # print "After Frequency", len(curcaseslist)
        #todo select the evident case if exists.
        #~forced = False
        # How to choose a vocalized case
        # and lets other methode to choices by semantic and syntaxic
        # choose a case is a stop, word and has next relation  
        if   self.get_enabled_syntaxic_analysis():
            if not chosen:
                for current in curcaseslist:
                    if current.is_stopword() and current.has_next():
                        chosen = current
                        break 

        # choose a case with two semantic  relation previous and next
        if   self.get_enabled_syntaxic_analysis() and \
        self.get_enabled_semantic_analysis():
            for current in curcaseslist:
                if self.anasem.is_related(previous, current) \
                and current.has_sem_next():
                    chosen = current
                    break 
            # choose a case with one semantic  relation previous,
            # and the previous has a syntaxic relation
            if not chosen:
                for current in curcaseslist:
                    if self.anasem.is_related(previous, current) and \
                    previous.has_next():
                        chosen = current
                        break 
            # choose a case with one semantic  relation previous
            if not chosen:
                for current in curcaseslist:
                    if self.anasem.is_related(previous, current):
                        chosen = current
                        break 
            # choose a case with one semantic  relation  next with a 
            #syntaxic relation between previous and current                    
            if not chosen:
                for current in curcaseslist:
                    if self.anasynt.is_related(previous, current) and \
                    current.has_sem_next():
                        chosen = current
                        break 
            # choose a case with one semantic  relation  next   
            if not chosen:
                for current in curcaseslist:
                    if  current.has_sem_next():
                        # print "15", current.get_vocalized().encode('utf8')
                        chosen = current
                        break 
        if  self.get_enabled_syntaxic_analysis():
            # choose a case with two syntaxic  relation previous and next
            if not chosen :
                for current in curcaseslist:
                    if self.anasynt.is_related(previous, current) and \
                    current.has_next() and not current.is_passive():
                        chosen = current
                        break
                else:
                    for current in curcaseslist:
                        if self.anasynt.is_related(previous, current) and\
                         current.has_next():
                            chosen = current
                            break
                    else:
                    # choose a case with one syntaxic  relation previous 
                    #select active voice
                        for current in curcaseslist:
                            if self.anasynt.is_related(previous, current) \
                            and not current.is_passive():
                                chosen = current
                                break
                        else:
            #select passive voice
                            for current in curcaseslist:
                                if self.anasynt.is_related(previous, current) :
                                    chosen = current
                                    break                         
            # choose a case with one syntaxic  relation next 
            if not chosen:
                for current in curcaseslist:
                    if current.has_next():
                        chosen = current
                        break 
                else:
                #---------------------------
                #no relation no nexts
                #----------------------------
                # choose a case of stop word
                    for current in curcaseslist:
                        if current.is_stopword():
                            # print "25"
                            # # if previous: previous.vocalized += "*"
                            chosen = current
                            break 
                    else:
                # choose a case with mansoub Noun
                        for current in curcaseslist:
                            if current.is_noun() and current.is_mansoub():
                                chosen = current
                                break 
                        else:
                        # choose a case marfou3 verb
                            for current in curcaseslist:
                                if current.is_verb() and not current.is_passive()\
                                 and current.is_marfou3():
                                    chosen = current
                                    break 
                            else:
                            # choose a case verb
                                for current in curcaseslist:
                                    if current.is_verb() and not \
                                    current.is_passive()and (current.is_marfou3()\
                                     or current.is_past()):
                                        chosen = current
                                        break 
                                else:
                                # choose a case marfou3 verb if there 
                                # are no active voice
                                    for current in curcaseslist:
                                        if current.is_verb():
                                            chosen = current
                                            break
        if not chosen and len(curcaseslist)>0:
            chosen = curcaseslist[0]        
        return chosen
        
    #~def choose_tashkeel_old(self, curcaseslist, 
    #~previous_chosen_case = None, _next_cases_list = None):
        #~"""
        #~Choose a tashkeel for the current word, according to the previous one.
        #~@param curcaseslist: list of steming result of the word.
        #~@type curcaseslist: list of stemmedSynword
        #~@param : the chosen previous word stemming.
        #~@type previous_chosen_case:stemmedSynword
        #~@return: the chosen stemming of the current word.
        #~@rtype:stemmedSynword.
        #~"""
#~
        #~# select the first chosen tashkeel
        #~if not curcaseslist:
            #~return None
        #~len_ccs = len(curcaseslist) # Len CCS
        #~
        #~# if there are one case only
        #~if len_ccs == 1:
            #~chosen = curcaseslist[0]
            #~return chosen
        #~
        #~chosen = None
        #~previous = previous_chosen_case
        #~
        #~# test selct by score
        #~if self.select_by_score_enabled:
            #~chosen = self._select_by_score(curcaseslist, previous)
            #~if chosen:
                #~return chosen 
#~
#~
        #~# How to choose a vocalized case
        #~# and lets other methode to choices by semantic and syntaxic
        #~# choose a case is a stopword and has next relation
        #~if not chosen:
            #~for current in curcaseslist:
                #~if current.is_stopword() and current.has_next():
                    #~chosen = current
                    #~break 
#~
        #~if not chosen:
            #~chosen_list = []
            #~if not previous or previous.is_initial():
                #~condidate_sem_list = [] # semantic previous
                #~#condidate_syn_list = [] # syntaxic previous            
                #~condidate_syn_list = [i for i in range(len_ccs) \
                  #~if curcaseslist[i].has_previous()]
                #~print 'initial cases', len(condidate_syn_list)
            #~else: #if previous:
                #~condidate_sem_list = previous.get_sem_next()  
                #~# semantic previous
                #~condidate_syn_list = previous.get_next()  
                #~# syntaxic previous            
#~
            #~condidate_sem_sem_list = [] #semantic previous semantic Next
            #~condidate_sem_syn_list = [] #semantic previous syntaxic Next
            #~condidate_syn_sem_list = [] #syntaxic previous semantic Next 
            #~condidate_syn_syn_list = [] #syntaxic previous syntaxic Next 
            #~condidate_next_sem_list = [] # only semantic Next 
            #~condidate_next_syn_list = [] # only syntaxic Next 
#~
            #~# look up for semantic semantic and semantic syntaxic 
            #~for i in condidate_sem_list:
                #~# one relation with previous
                #~if i < len(curcaseslist) and \
                #~curcaseslist[i].has_next():
                #~#one relation with a next
                    #~condidate_sem_syn_list.append(i) 
                    #~# semantic previous syntaxic Next                
                    #~if curcaseslist[i].has_sem_next():
                    #~#one relation with a next
                        #~condidate_sem_sem_list.append(i)
                         #~# semantic previous semantic Next
#~
            #~#lookup for syntaxic syntaxic and syntaxic semantic
#~
            #~if condidate_syn_list and max(condidate_syn_list)>len_ccs:
                #~print "Warrning, ----------------------------"
                #~print 'Nexts', condidate_syn_list
                #~print 'curre', 
                #~print (hash(previous), previous.getWord().encode('utf8'), 
                 #~curcaseslist[0].getWord().encode('utf8'))
                #~for i in range(len_ccs):
                    #~print i, ':', curcaseslist[i].get_order(), ', ', 
                #~print 
#~
            #~for i in condidate_syn_list:
                #~#print condidate_syn_list, i, len(curcaseslist), 
                #~#curcaseslist[i].get_order()
                #~# one relation with previous
                #~if i < len(curcaseslist) and \
                #~curcaseslist[i].has_next():
                #~#one relation with a next
                    #~condidate_syn_syn_list.append(i) 
                    #~# syntaxic previous syntaxic Next
                    #~if curcaseslist[i].has_sem_next():
                    #~#one relation with a next
                        #~condidate_syn_sem_list.append(i) 
                        #~# syntic previous semantic Next
#~
            #~#look up for Cases with only next smeantic or only next syntaxic
            #~for i in range(len_ccs):
                #~# one relation with previous
                #~if curcaseslist[i].has_next():
                #~#one relation with a next
                    #~condidate_next_syn_list.append(i) # syntaxic Next 
                    #~if curcaseslist[i].has_sem_next():
                    #~#one relation with a next
                        #~condidate_next_sem_list.append(i) # semantic Next
#~
            #~# priority to choose a table of cases
            #~# previous/next    semantic    syntaxic    Not
            #~# semantic        1            2            3
            #~# syntaxic        4            6            7
            #~# not            5            8            9
            #~#1
            #~if condidate_sem_sem_list:
                #~chosen_list = condidate_sem_sem_list
            #~#2
            #~elif condidate_sem_syn_list:
                #~chosen_list = condidate_sem_syn_list
            #~#3
            #~elif condidate_sem_list:
                #~chosen_list = condidate_sem_list
            #~#4
            #~elif condidate_syn_sem_list:
                #~chosen_list = condidate_syn_sem_list
            #~#5
            #~elif condidate_next_sem_list:
                #~chosen_list = condidate_next_sem_list
            #~#6
            #~elif condidate_syn_syn_list:
                #~chosen_list = condidate_syn_syn_list
            #~#7
            #~elif condidate_syn_list:
                #~chosen_list = condidate_syn_list
            #~#8
            #~elif condidate_next_syn_list:
                #~chosen_list = condidate_next_syn_list
            #~#9
            #~else:
                #~chosen_list = []
            #~# look for a best case in condidates
            #~if chosen_list:
                #~#to do select
                #~# temporary
                #~if debug: 
                    #~print ("chosen", len(chosen_list), 
                    #~round(float(len(chosen_list))*100/len(curcaseslist)),
                     #~len(curcaseslist))
                    #~for i in chosen_list:
                        #~print ('\t', 
                        #~curcaseslist[i].get_vocalized().encode('utf8'), 
                        #~curcaseslist[i].get_freq(), 
                        #~curcaseslist[i].is_forced_case())
                #~if chosen_list[0] < len(curcaseslist): #valid cases
                    #~if len(chosen_list) == 1:
                        #~chosen = curcaseslist[chosen_list[0]]
                    #~else:
                    #~#temporary
                    #~#To do: use another method to select case
                    #~# 1- Select high frequency
                        #~high_score = curcaseslist[chosen_list[0]].get_freq()
                        #~high_score_index = chosen_list[0]
                        #~for i in chosen_list:
                            #~if curcaseslist[i].get_freq()>high_score:
                                #~high_score = \
                                #~curcaseslist[chosen_list[0]].get_freq()
                                #~high_score_index = chosen_list[0]
                        #~chosen = curcaseslist[high_score_index]
                #~else: #warning chosen tashkeel out of range
                    #~print "warning: chosen tashkeel out of range"
#~
        #~#---------------------------
        #~#no relation no nexts
        #~#----------------------------
        #~#choose a case of stop word
        #~# and lets other methode to choices by semantic and syntaxic
        #~if not previous or previous.is_initial():
            #~curcaseslist = self._filter_for_initial(curcaseslist)
        #~# print "before Semantic", len(curcaseslist)
        #~curcaseslist = self._filter_by_semantic(curcaseslist, previous)
        #~# filter results accorind to  word frequency
        #~# print "After Semantic", len(curcaseslist)        
        #~curcaseslist = self._filter_by_syntaxic(curcaseslist, previous)
        #~# print "After Syntax", len(curcaseslist)
        #~curcaseslist = self._frequency_filter(curcaseslist)
        #~# print "After Frequency", len(curcaseslist)
        #~if not chosen:
            #~for current in curcaseslist:
                #~if current.is_stopword():
                    #~chosen = current
                    #~break 
            #~else:
            #~# choose a case with marfou3 verb
                #~for current in curcaseslist:
                    #~if current.is_noun() and current.is_mansoub():
                        #~chosen = current
                        #~break 
                #~else:
                    #~for current in curcaseslist:
                        #~if current.is_verb():
                            #~if current.isPresent() and not current.is_passive()\
                           #~and not (current.is_mansoub() or current.is_majzoum()):
                                #~chosen = current
                                #~break
                            #~elif current.is_past() and not current.is_passive():
                                #~chosen = current
                                #~break
        #~if not chosen and len(curcaseslist)>0:
            #~chosen = curcaseslist[0]
        #~return chosen

    def _select_by_score(self, word_analyze_list, previous):
        """
        Choose the word according a score estimation
        @param word_analyze_list: list of steming result of the word.
        @type word_analyze_list: list of  stemmedSynWord
        @param previous: previous word.
        @type previous: stemmedSynWord        
        @return: filtred list of stemming result.
        @rtype: list of stemmedSynWord.
        """    
        #choose by score
        chosen = False
        high_score = 0
        # if previous has next, we choose from nexts only, 
        # else we choose the highscore from the current word case
        if previous and (previous.has_next() or previous.has_sem_next()):
            for current in word_analyze_list:
                current_score = current.get_score()
                # if the current is related to previous
                # if not self.anasem.is_related(previous, current)  
                # and not  self.anasynt.is_related(previous, current):
                    # current_score = 0
                if self.anasem.is_related(previous, current) or \
                self.anasynt.is_related(previous, current) :
                    if current_score > high_score:
                        high_score = current_score
                        chosen = current
        else:
            for current in word_analyze_list:
                current_score = current.get_score()
                if  current_score > high_score:
                    high_score = current_score
                    chosen = current
            
        return chosen


    def _filter_by_semantic(self, word_analyze_list, previous):
        """
        filter results according to the word semantic relation
        @param word_analyze_list: list of steming result of the word.
        @type word_analyze_list: list of  stemmedSynWord
        @param previous: previous word.
        @type previous: stemmedSynWord        
        @return: filtred list of stemming result.
        @rtype: list of stemmedSynWord.
        """    
        temp_list = []
        for current in word_analyze_list:
            if  self.anasem.is_related(previous, current):
                temp_list.append(current)
            elif current.has_sem_next() or current.is_stopword():
                temp_list.append(current)
        if temp_list:
            return temp_list
        else:
            return word_analyze_list

    def _filter_for_initial(self, word_analyze_list):
        """
        filter results according to the initial position in the sentence
        @param word_analyze_list: list of steming result of the word.
        @type word_analyze_list: list of  stemmedSynWord
        @return: filtred list of stemming result.
        @rtype: list of stemmedSynWord.
        """    
        temp_list = []
        for current in word_analyze_list:
            if  current.is_stopword():
                temp_list.append(current)
            elif current.is_marfou3() and not current.is_passive(): 
                # noun or verb
                temp_list.append(current)
            elif current.is_past():
                temp_list.append(current)    
        if temp_list:
            return temp_list
        else:
            return word_analyze_list        
    def _filter_by_syntaxic(self, word_analyze_list, previous):
        """
        filter results according to the word syntaxic relation
        @param word_analyze_list: list of steming result of the word.
        @type word_analyze_list: list of  stemmedSynWord
        @param previous: previous word.
        @type previous: stemmedSynWord        
        @return: filtred list of stemming result.
        @rtype: list of stemmedSynWord.
        """    
        temp_list = []
        for current in word_analyze_list:
            if  self.anasynt.is_related( previous, current):
                temp_list.append(current)
            if  current.is_stopword():
                temp_list.append(current)
            elif current.has_next():
                temp_list.append(current)
        if temp_list:
            return temp_list
        else:
            return word_analyze_list

    def _frequency_filter(self, word_analyze_list):
        """
        filter results according to the word frequency
        @param : list of steming result of the word.
        @type word_analyze_list: list of dict
        @return: filtred list of stemming result.
        @rtype: list of stemmedSynWord.
        """    
        if not word_analyze_list:
            return None
        # select according to  word frequency
        freq = 0
        chosen_freq = 0
        #first chose the frequncy
        for item_dict in word_analyze_list:
            freq = item_dict.get_freq()
            if freq >= chosen_freq:
                chosen_freq = freq
                
        new_list = []
        #sort the stemmed words
        # endlist is used to add forced case in the end of the list
        end_list = []
        for item_dict in word_analyze_list:
            # select max frequency
            if item_dict.get_freq() == chosen_freq:
                new_list.append(item_dict)
            # add the forced cases
            elif  self.get_enabled_syntaxic_analysis() and \
            item_dict.is_forced_case() or item_dict.is_forced_wordtype()\
             or item_dict.is_stopword():
                end_list.append(item_dict)
        new_list += end_list
        return new_list

    def tashkeel_ouput_html_suggest(self, text):
        """
        Vocalize the text and give suggestion to improve tashkeel by user.
        @param text: input text.
        @type text: unicode.
        @return: vocalized text.
        rtype: dict of dict.
        """
        return self.tashkeel(text, suggestion = True, format_display = "html")
    def tashkeel_output_text(self, text):
        """
        Vocalize the text witthout suggestion
        @param text: input text.
        @type text: unicode.
        @return: vocalized text.
        rtype: text.
        """
        return self.tashkeel(text, suggestion = False, format_display = "text")
    def _ajust_vocalized_result(self, text):
        """
        Ajust the resulted text after vocalization to correct some case 
        like 'meeting of two queiscents = ألتقاء الساكنين'
        @param text: vocalized text
        @type text: unicode
        @return: ajusted text.
        @rtype: unicode
        """
        # min = > mina
        text = re.sub(ur'\sمِنْ\s+ا', u' مِنَ ا', text)
        # man = > mani
        text = re.sub(ur'\sمَنْ\s+ا', u' مَنِ ا', text)
        #An = > ani
        text = re.sub(ur'\sعَنْ\s+ا', u' عَنِ ا', text)
        #sukun + alef = > kasra +alef
        text = re.sub(ur'\s%s\s+ا'%araby.SUKUN, u' %s ا' % araby.SUKUN, text)
        #ajust pounctuation
        text = re.sub(ur" ([.?!, :)”—]($| ))", ur"\1", text)
        #binu = > bin 
        # temporary, to be analysed by syntaxical analyzer
        text = re.sub(ur'\sبْنُ\s', u' بْن ', text)        
        # # # اختصارات مثل حدثنا إلى ثنا وه تكثر في كتب التراث
        # text = re.sub(ur'\seثِنَا\s', u' ثَنَا ', text)        
        return text

    def ajust_vocalized_suggestion(self, _suggest_list):
        """
        Ajust the resulted text after vocalization to correct some case 
        like 'meeting of two queiscents = ألتقاء الساكنين'
        @param text: _suggest_list
        @type text: list of dict of unicode
        @return: _suggest_list.
        @rtype: list of dict of unicode
        """
        for i in range(len(_suggest_list)-1):
            if _suggest_list[i]['chosen'] in (u'مَنْ', u'مِنْ', u'عَنْ'):
                if i+1 < len(_suggest_list) and \
                _suggest_list[i+1].has_key('chosen') \
                and _suggest_list[i+1]['chosen'].startswith(araby.ALEF):
                    if _suggest_list[i]['chosen'] == u'مِنْ':
                        _suggest_list[i]['chosen'] = u'مِنَ'
                    elif _suggest_list[i]['chosen'] == u'عَنْ':
                        _suggest_list[i]['chosen'] = u'عَنِ'
                    elif _suggest_list[i]['chosen'] == u'مَنْ':
                        _suggest_list[i]['chosen'] = u'مَنِ'
            # if _suggest_list[i]['chosen'] == u'بْنُ':
                # _suggest_list[i]['chosen'] = u'بْن'
        return _suggest_list

    def display(self, word, format_display = "text"):
        """
        format the vocalized word to be displayed on web interface.
        @param word: input vocalized word.
        @type word: unicode.
        @return: html code.
        rtype: unicode.
        """
        format_display = format_display.lower()
        if format_display == "html":
            return u"<span id='vocalized' class='vocalized'>%s</span>" % word
        elif format_display == 'text':
            return word
        else:
            return word

    def assistanttashkeel(self, text):
        """
        Vocalize the text.
        @param text: input text.
        @type text: unicode.
        @return: vocalized text.
        rtype: unicode.
        """    
        detailled_syntax = self.full_stemmer(text)
        vocalized_text = u""

        for word_analyze_list in detailled_syntax:
            # o ajust relation between words 
            #previous = word_stemming_dict
            for item in word_analyze_list:
                voc = item.get_vocalized()
                vocalized_text = u"".join([vocalized_text, voc])
        return vocalized_text

    def pre_tashkeel(self, text):
        """
        Vocalize the text by evident cases and by detecting numbers clauses
        @param text: input text.
        @type text: unicode.
        @return: statisticlly vocalized text.
        rtype: unicode.
        """
        # get the word list
        # اختصارات مثل حدثنا إلى ثنا وه تكثر في كتب التراث
        for abr in tashkeel_const.CorrectedTashkeel.keys():
            text = re.sub(ur"\s%s\s"%abr, ur" %s " % \
            tashkeel_const.CorrectedTashkeel[abr], text)
        wordlist = self.analyzer.tokenize(text)
        prevocalized_list = pyarabic.number.pre_tashkeel_number(wordlist)
        #Todo ajust prevocalization of named enteties
        prevocalized_list = pyarabic.named.pretashkeel_named(prevocalized_list)
        return u" ".join(prevocalized_list)


    def stat_tashkeel(self, text):
        """
        Vocalize the text by statistical method according to the collocation dictionary
        @param text: input text.
        @type text: unicode.
        @return: statisticlly vocalized text.
        rtype: unicode.
        """
        text = self.collo.lookup4long_collocations(text)
        
        # get the word list
        wordlist = self.analyzer.tokenize(text)
        #~vocalized_text = u""
        #~previous = u""
        #~list_dict = [] # returned resultat
        # temporarly used
        #~suggest = []
        #~liste = wordlist
        # use a list as a stack, 
        # give two element from the end.
        # test the tow elements if they are collocated, 
        # if collocated return the vocalized text
        # if else, delete the last element, and return the other to the list.
        newlist = self.collo.lookup(wordlist)
        #todo: return a text from the statistical tashkeel
        text = u" ".join(newlist)
        return text

def mainly():
    """
    main test
    """
    print "test"        
    vocalizer = TashkeelClass()
    # text = u"""تجف أرض السلام بالسلام الكبير.    مشى على كتاب السلام.
    # جاء الولد السمين من قاعة القسم الممتلئ"""
    text = u"يعبد الله تطلع الشمس"
    voc = vocalizer.tashkeel(text)
    print voc.encode('utf8')
if __name__ == "__main__":
    mainly()
