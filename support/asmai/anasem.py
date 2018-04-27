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
import  asmai.sem_const_light as sem_const
import semdictionary 
#~ import  asmai.sem_const_heavy as sem_const
import  aranasyn.anasyn
import  aranasyn.syn_const as syc

import  aranasyn.cache
debug  =  False
#debug  =  True
PRIMATE_RELATION_LIST = [
                syc.PrimatePredicateMansoubRelation,
                syc.PrimateMansoubPredicateRelation,
                syc.DescribedAdjectiveRelation,
                syc.PrimatePredicateRelation,
                ]
class SemanticAnalyzer:
    """
        Arabic Semantic analyzer
    """

    def __init__(self, cache_path=False):
        
        self.semdict = semdictionary.SemanticDictionary()
        
        # a NoSql database for ferquent relationship between lexical words.
        self.syncache = aranasyn.cache.cache(cache_path)
        
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
                                                            stmword, 
                                                            previous_case_position,
                                                            stmword_case_position)
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
        if not previous or not current:
            return previous, current
        
        #~ # Choose predifined syntaxique semantique relation
        #~ freq_synt = self.syncache.is_related(origin_pre, origin_cur)
        #~ if freq_synt :
            #~ # return the first key
            #~ # to do add more options
            #~ return freq_synt.keys()[0]
        if self.is_syn_related(previous, current):
            # First use syntaxic trained database
            # if the actual relation existes in database, then 
            # The actual syntax relation is semantic
            syn_relation = previous.get_next_relation(current.get_order())

            # Choose predifined syntaxique semantique relation
            syn_relat_dict = self.syncache.is_related(previous.get_original(), 
                                                      current.get_original())
            # Choose predifined syntaxique semantique relation                                                      
            syn_relat_dict_invertd = self.syncache.is_related(current.get_original(), 
                                                      previous.get_original())
            if debug: print "anasem"
            if debug: print(u" ".join([previous.get_original(), current.get_original(), str(syn_relation), repr(syn_relat_dict)])).encode('utf8') 
            if syn_relat_dict:
                # if syntax relation exists in the given dict, ok , there is a relation
                # between the two words
                if syn_relation in syn_relat_dict:
                    
                    relation = syn_relation
                    confirmed = "ok0" # just for test, instead True is enough
                
                elif syn_relation ==  syc.VerbSubjectRelation and syc.SubjectVerbRelation in syn_relat_dict_invertd:
                # relation verb Subject and inverted Subject Verb
                    relation = syn_relation
                    confirmed = "ok0-verb-subject" 
                #~ elif syn_relation ==  syc.SubjectVerbRelation and syc.VerbSubjectRelation in syn_relat_dict_invertd:
                #~ # relation Subject  Verb and inverted Verb Subject
                    #~ relation = syn_relation
                    #~ confirmed = "ok0-subject-verb"
                #~ elif syn_relation ==  syc.VerbPassiveSubjectRelation and syc.VerbObjectRelation in syn_relat_dict:
                #~ # 
                    #~ relation = syn_relation
                    #~ confirmed = "ok0-paasiv-verb_object"                
                #~ elif syn_relation ==  syc.VerbObjectRelation  and syc.VerbPassiveSubjectRelation in syn_relat_dict:
                #~ # 
                    #~ relation = syn_relation
                    #~ confirmed = "ok0-verb_object"                
                elif syn_relation  in PRIMATE_RELATION_LIST  and  any(r in syn_relat_dict for r in PRIMATE_RELATION_LIST):
                    relation = syn_relation
                    confirmed = "ok0-primate"                      
                   #~ #ToDo: add compatible relations
                    #~ # like verb + subject => subject verb

            # second step
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
            if not relation:
                if previous.is_verb() and current.is_noun():
                    confirmed = ""
                    relation  = self.are_sem_related(previous, current)
                    #~ print "relation", relation
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
                    #~ print "#2", relation
                    confirmed = ""
                    if relation:
                        if relation == sem_const.Added :
                            #مضاف إليه
                            if current.is_majrour():
                                confirmed = "ok1"
                        #Todo    #نعت
                        elif relation  ==  sem_const.Adj:
                            if current.is_adj():
                                confirmed = 'ok4' 
                        #Todo    #نعت
                        elif relation  ==  sem_const.Subject:
                            if current.is_adj() and u"اسم فاعل" in current.get_type():
                                confirmed = 'ok5' 
                        #Todo    #نعت
                        elif relation  ==  sem_const.Predicate:
                            #~ print "x"
                            #~ print current.get_tags().encode('utf8');

                            #~ if current.is_adj() and not u"اسم فاعل" in current.get_tags():

                            if current.is_adj() and u"اسم مفعول"in  current.get_type():
                                confirmed = 'ok6'
                                #~ print confirmed
                            #فاعل
                    #        if not current.is_passive():
                    #            confirmed = "ok3"
                    #~ print "#2", confirmed
                       
        if relation and confirmed:
            # add to the previous a pointer to the next word order.
            # N for next
            if debug: print "anasem:r relation",relation, "confirmed", confirmed 
            previous.add_sem_next(current_position, relation)
            # add to the current word case a pointer to the previous word order.
            #p for previous
            current.add_sem_previous(previous_position, relation)
        return previous, current

    #~ @deprecated_func
    def are_sem_related3(self, previous, current):
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
        relation = ''
        if previous.is_proper_noun():
            preorigin  =  u'فلان'
        curorigin  =  current.get_original()
        if current.is_proper_noun():
            curorigin  =  u'فلان'
        if sem_const.SEM_RELATION_TABLE.get(preorigin, []):
            relation = sem_const.SEM_RELATION_TABLE[preorigin].get(curorigin, '')
        else:
            print "are_sem_related", (u" + ".join([preorigin, curorigin])).encode('utf8')

            for key in sem_const.SEM_DERIVATION_TABLE:
                #~ print "1"
                if sem_const.SEM_DERIVATION_TABLE[key]['subj'] == preorigin:
                    relation = sem_const.SEM_RELATION_TABLE[key].get(curorigin, '')
                    if relation == sem_const.Subject:
                        break
                    else: 
                        relation = ''
                # if the verb is transitive, we can test predicate (مفعولية) relation
                elif  (sem_const.SEM_DERIVATION_TABLE[key]['trans'] and
                sem_const.SEM_DERIVATION_TABLE[key]['obj'] == preorigin):
                    relation = sem_const.SEM_RELATION_TABLE[key].get(curorigin, '')
                    if relation == sem_const.Predicate:
                        break
                    else: 
                        relation = ''
                elif  sem_const.SEM_DERIVATION_TABLE[key]['add'] == preorigin:
                    relation = sem_const.SEM_RELATION_TABLE[key].get(curorigin, '')
                    if relation == sem_const.Added:
                        break
                    else: 
                        relation = ''
        print relation
        if relation == '':
            return False
        else: 
            return relation
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
        #~ return False
        origin_pre  =  previous.get_original()
        relation = ''
        if previous.is_proper_noun():
            origin_pre  =  u'فلان'
        origin_cur  =  current.get_original()
        if current.is_proper_noun():
            origin_cur  =  u'فلان'
        return self.semdict.lookup(origin_pre, origin_cur)
        
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
        return (( previous and  current ) and 
        previous.get_order() in current.get_previous() 
        and current.get_order() in previous.get_next()
        )

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
        return (( previous and  current ) and 
        previous.get_order() in current.get_sem_previous() 
        and current.get_order() in previous.get_sem_next()
        )
        
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
