#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        anasem
# Purpose:     Arabic semantic analyzer Asmai
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     29-11-2012
# Copyright:   (c) Taha Zerrouki 2012
# Licence:     GPL
#-------------------------------------------------------------------------------
"""
    Arabic Semantic analyzer
"""
import sys
sys.path.append('../')
sys.path.append('../lib')
import  asmai.sem_const as sem_const
import  aranasyn.anasyn
#~import  qalsadi.stemmedword as stemmedword
#~import  aranasyn.stemmedsynword as stemmedsynword
debug  =  False
#debug  =  True
class SemanticAnalyzer:
    """
        Arabic Semantic analyzer
    """

    def __init__(self):
        pass
    def analyze(self, detailed_stemming_dict):
        """
        Semantic analysis of stemming and syntaxic results.

        morphological and analysis Result is a list of list of 
        StemmedSynWord class.
        The semantic result have the same structure, but we add a 
        field named 'semantic' to every word steming dictioionary
        @param detailed_stemming_dict: detailed stemming stemmedsynword.
        @type detailed_stemming_dict:list of list of stemmedsynword
        @return: detailed semantic result with semantic tags.
        @rtype: list of list of stemmedsynword
        """
        return self.context_analyze(detailed_stemming_dict)


    def calculate_scores(self, stemmed_synwordlistlist):
        """
        Calculate scores for every case, in order to allow the scoring 
        tashkeel choose.
        @param stemmed_synwordlistlist: detailed stemming, syntaxic and 
        semantic details.
        @type stemmed_synwordlistlist: list of list of stemmedsynword class
        @return: detailed semantic result with semantic tags.
        @rtype: list of list of stemmedsynword class
        """    
        initial_score  = 100
        #~final_score    = 100
        #initial  =  aranasyn.anasyn .stemmedsynword.stemmedSynWord()
        #initial.set_score(initial_score)
        #~counter  =  0
        previous_index = 0
        # study the relations between words stemmings
        # first level
        for current_index in range(len(stemmed_synwordlistlist)):
            #index used to handle stmd position
            #~current_case_position = 0
            #second level
            for current in stemmed_synwordlistlist[current_index]:
                # initialize the current score to 0
                current.score = 0
                if  current_index == 0:  # the initial case
                    """ the initial case"""
                    #~counter +=  1
                    if 0 in current.previous:
                        current.previous[0] =  initial_score
                        current.score = initial_score
                else:
                    previous_case_position  = 0  
                    for previous in stemmed_synwordlistlist[previous_index]:
                        #~counter +=  1
                        current.recalculate_score(previous_case_position,
                         previous.get_score())
                        previous_case_position  += 1  
                current.add_syntax(u'Scr:%d'%current.get_score())
                #~current_case_position  += 1
        return stemmed_synwordlistlist


    def context_analyze(self, stemmed_synwordlistlist):
        """
        Semantic analysis of stemming results.
        @param stemmed_synwordlistlist: detailed stemming and syntaxic details.
        @type stemmed_synwordlistlist: list of list of stemmedsynword class
        @return: detailed semantic result with semantic tags.
        @rtype: list of list of stemmedsynword class
        """
        # ignore if the current word is transparent
        ignore  =  False
        #~counter  =  0

        previous_index = 0    
        # study the relations between words stemmings
        for current_index in  range(len(stemmed_synwordlistlist)):
            #index used to handle stmd position
            stmword_case_position = 0
            for stmword in stemmed_synwordlistlist[current_index]:
                if  current_index == 0:  # the initial case
                    #~""" the initial case"""
                    #~counter +=  1
                    stmword  = self.bigram_analyze(None, stmword)[1]
                    
                else:
                    previous_case_position  = 0  
                    for previous in stemmed_synwordlistlist[previous_index]:
                        #~counter +=  1
                        previous, stmword  = self.bigram_analyze(previous, 
                        stmword, previous_case_position, stmword_case_position)
                        previous_case_position  += 1  
                            
                # if the current word is transparent, ignore it and fix 
                #~the previous index to the previous word.
                if stmword.is_transparent():
                    ignore = True
                else: ignore = False
                stmword_case_position  += 1
            # if the current word ha sall its cases as transparent
            # الكلمة الشفافة مثل اسم الإشارة تنقل 
#تأثير الكلمة السابقة لها للكلمة اللاحقة لها# م
            # مثل رأيت هذا الرجل
            # if not the word is not transprent, change the previous index.
            # else: change the ignore state and save the previous index as it.
            if not ignore:
                previous_index  =  current_index
            else:
                # previous index is mantained.
                ignore = False

            # previous_index  =  current_index

        return stemmed_synwordlistlist


    def bigram_analyze(self, previous, current, previous_position = 0, 
    current_position = 0):
        """
        Syntaxic analysis of stemming results, two words.
        the positions are use to join related cases.
        @param previous    : the first item in bigram.
        @type previous    : stemmedSynWord
        @param current    : the second item in bigram.
        @type current    : stemmedSynWord
        @param previous_position    : the first item position 
        in the word case list.
        @type previous_position    : integer
        @param current_position    : the second item position 
        in the word case list.
        @type current_position    : integer
        @return: the updated previous and current stemmedSynWord.
        @rtype: (previous, current)
        """
        # if the two words are related syntaxicly
        relation = ""
        confirmed = ''
        if self.is_syn_related(previous, current):
            # if the first word is a verb and the second is a noun, 
            # the noun can be Suject of object or vice-object
            #إذا توالى فعل واسم، فيكون الاسم
            # إما فاعلا أو مفعولا أونائب فاعل
            #يكونفاعلا إذا كانت العلاقة فاعلية بين الفعل والاسم
            # ويكون مفعولا به أو نائب فعل إذا كانت
# العلاة مفعولية بين الفعل والاسم
            # تخزن المعلومات على شكل مصدر الفعل مضافا إلى الاسم
            # وجود الإضافة بين المصدر والاسم 
#يدل على وجود علاقة الفاعلية أو المفعولية
            if previous.is_verb() and current.is_noun():
                confirmed = ""
                relation  = self.are_sem_related(previous, current)
                if relation:
                    if relation == sem_const.Predicate :
                        #نائب فاعل
                        if previous.is_passive() and current.is_marfou3():
                            confirmed = "ok1"
                        #مفعول به
                        elif not previous.is_passive() and current.is_mansoub():
                            confirmed = "ok2"
                    elif relation == sem_const.Subject: 
                        #فاعل
                        if not previous.is_passive() and current.is_marfou3():
                            confirmed = "ok3"
                    
            elif previous.is_noun() and current.is_verb():
                relation  = self.are_sem_related(current, previous)
                confirmed = ""
                if relation:
                    if relation == sem_const.Predicate :
                        #نائب فاعل
                        if current.is_passive():
                            confirmed = "ok1"
                        #مفعول به
                        elif not current.is_passive():
                            confirmed = "ok2"
                    elif relation == sem_const.Subject: 
                        #فاعل
                        if not current.is_passive():
                            confirmed = "ok3"
            elif previous.is_noun() and current.is_noun():
                relation  = self.are_sem_related(current, previous)
                confirmed = ""
                if relation:
                    if relation == sem_const.Added :
                        #مضاف إليه
                        if current.is_majrour():
                            confirmed = "ok1"
                    #Todo    #نعت
                    elif relation  ==  sem_const.Adj:
                        if current.isAdj():
                            confirmed = 'ok4' 
                        #فاعل
                #        if not current.is_passive():
                #            confirmed = "ok3"

                       
        if relation and confirmed:
            # add to the previous a pointer to the next word order.
            # N for next
            #previous.add_syntax('@')
            #print '@'
            #current.add_syntax('@')            
            previous.add_sem_next(current_position)
            # add to the current word case a pointer to the previous word order.
            #p for previous
            current.add_sem_previous(previous_position)
        return previous, current

    def are_sem_related(self, previous, current):
        """
        verify the semantic relation between the previous 
        to current stemmed word.
        If the current word is related with the previous word, return True.
        The previous word can contain a pointer to the next word. 
        the current can have a pointer to the previous if they ara realated
        @param previous: the previous stemmed word, 
        choosen by the tashkeel process.
        @type previous:stemmedSynWord class 
        @param current: the current stemmed word.
        @type current:stemmedSynWord class 
        @return: return the relation between two words, else False
        @rtype: Unicode or False
        """
        preorigin  =  previous.get_original()
        if previous.is_proper_noun():
            preorigin  =  u'فلان'
        curorigin  =  current.get_original()
        if current.is_proper_noun():
            curorigin  =  u'فلان'
        key = u" ".join([preorigin, curorigin])
        relation  =  sem_const.SemanticTable.get(key, '')
        
        if relation == '':
            return False
        else: 
            return relation

    def is_syn_related(self, previous, current):
        """
        verify the syntaxic path from the previous 
        to current stemmed word.
        If the current word is related with the previous word, return True.
        The previous word can contain a pointer to the next word. 
        the current can have a pointer to the previous if they ara realated
        @param previous: the previous stemmed word, 
        choosen by the tashkeel process.
        @type previous:stemmedSynWord class 
        @param current: the current stemmed word.
        @type current:stemmedSynWord class 
        @return: return if the two words are related syntaxicly.
        @rtype: boolean
        """
        if ( previous and  current ) and \
        previous.get_order() in current.get_previous() \
        and current.get_order() in previous.get_next():
            return True
        else:
            return False

    def is_related(self, previous, current):
        """
        verify the syntaxic path from the previous to current stemmed word.
        If the current word is related with the previous word, return True.
        The previous word can contain a pointer to the next word. 
        the current can have a pointer to the previous if they ara realated
        @param previous: the previous stemmed word, 
        choosen by the tashkeel process.
        @type previous:stemmedSynWord class 
        @param current: the current stemmed word.
        @type current:stemmedSynWord class 
        @return: return if the two words are related syntaxicly.
        @rtype: boolean
        """
        if ( previous and  current ) and \
        previous.get_order() in current.get_sem_previous() \
        and current.get_order() in previous.get_sem_next():
            return True
        else: return False        
        
    def decode(self, stemmed_synwordlistlist):
        """
        Decode objects result from analysis. helps to display result.
        @param stemmed_synwordlistlist: list of  list of StemmedSynWord.
        @type word_result: list of  list of StemmedSynWord
        @return: the list of list of dict to display.
        @rtype: list of  list of dict
        """    
        newresult  =  []
        for rlist in stemmed_synwordlistlist:
            tmplist  =  []
            for item in rlist:
                tmplist.append(item.get_dict())
            newresult.append(tmplist)    
        return  newresult

    def display(self, stemmed_synwordlistlist):
        """
        display objects result from analysis
        @param stemmed_synwordlistlist: list of  list of StemmedSynWord.
        @type word_result: list of  list of StemmedSynWord
        """    
        text  =  u"["
        for rlist in stemmed_synwordlistlist:
            text +=  u'\n\t['
            for item in rlist:
                text +=  u'\n\t\t{'
                stmword  =  item.get_dict()
                for key in stmword.keys():
                    text +=  u"\n\t\tu'%s'  =  u'%s', " % (key, stmword[key])
                text +=  u'\n\t\t}'
            text +=  u'\n\t]'
        text +=  u'\n]'
        return text
def mainly():
    """
    main test
    """
    text  =  u"يعبد الله منذ أن تطلع الشمس"

    import qalsadi.analex     
    result  =  []
    analyzer  =  qalsadi.analex.Analex()
    anasynt  =  aranasyn.anasyn.SyntaxAnalyzer()
    anasem  =  SemanticAnalyzer()    
    result  =  analyzer.check_text(text)
    result  =  anasynt.analyze(result)
    # semantic result
    result  =  anasem.analyze(result)    
    # the result contains objets
    #print repr(result)
    text2display  = anasynt.display(result)
    print text2display.encode('utf8')

if __name__  ==  "__main__":
    mainly()
