#************************************************************************
# $Id: mosaref_main.py, v 0.7 2009/06/02 01:10:00 Taha Zerrouki $
#
# ------------
# Description:
# ------------
#  Copyright (c) 2009, Arabtechies, Arabeyes Taha Zerrouki
#
#  This file is used by the web interface to execute verb conjugation
#
# -----------------
# Revision Details:    (Updated by Revision Control System)
# -----------------
#  $Date: 2009/06/02 01:10:00 $
#  $Author: Taha Zerrouki $
#  $Revision: 0.7 $
#  $Source: arabtechies.sourceforge.net
#
#***********************************************************************/
"""
The main function to call qutrub conjugation from other programs.
"""
import libqutrub.classverb  as classverb
import libqutrub.ar_verb  as ar_verb
import libqutrub.verb_valid  as verb_valid
import libqutrub.verb_const  as vconst
import pyarabic.araby as araby
import libqutrub.verb_db  as verb_db
verb_db.create_index_triverbtable()
#~ """ you nedd to create the trileteral verb dictionary  
# index to search within triverbs."""

def do_sarf(word, future_type, alltense = True, past = False, future = False, 
passive = False, imperative = False, future_moode = False, confirmed = False,
 transitive = False, display_format = "HTML"):
    """
    The main function to conjugate verbs.
    You must specify all parameters.
    Can be used as an example to call the conjugation class.
    @param word: the givern verb. the given word must be vocalized, 
    if it's 3 letters length only, else, the verb can be unvocalized, 
     but the Shadda must be given, it' considered as letter.
    @type word: unicode.
    @param future_type: For Triliteral verbs, 
    you must give the mark of Ain in the future, 
    كة عين الفعل في المضارع. it's given as a name of haraka (فتحة، ضمة، كسرة).
    @type future_type: unicode(فتحة، ضمة، كسرة).
    @param all: conjugate in all arabic tenses.
    @type all: Boolean, default(True)
    @param past: conjugate in past tense ألماضي
    @type past: Boolean, default(False)
    @param future: conjugate in arabic present and future tenses المضارع
    @type future: Boolean, default(False)
    @param passive: conjugate in passive voice  المبني للمجهول
    @type passive: Boolean, default(False)
    @param imperative: conjugate in imperative tense الأمر
    @type imperative: Boolean, default(False)
    @param future_moode: conjugate in future moode tenses المضارع المنصوب والمجزوم
    @type future_moode: Boolean, default(False)
    @param confirmed: conjugate in confirmed cases tense المؤكّد
    @type confirmed: Boolean, default(False)
    @param transitive: the verb transitivity التعدي واللزوم
    @type transitive: Boolean, default(False)
    @param display_format: Choose the display format:
        - 'Text':
        - 'HTML':
        - 'HTMLColoredDiacritics':
        - 'DICT':
        - 'CSV':
        - 'GUI':
        - 'TABLE':
        - 'XML':
        - 'TeX':
        - 'ROWS':
    @type display_format: string, default("HTML") 
    @return: The conjugation result
    @rtype: According to display_format.
    """
    valid = verb_valid.is_valid_infinitive_verb(word)
    if valid:
        future_type = ar_verb.get_future_type_by_name(future_type)
        #~ bab_sarf = 0
        #init the verb class to treat the verb
        vbc = classverb.VerbClass(word, transitive, future_type)
        vbc.set_display(display_format)

        if alltense :
            result =  vbc.conjugate_all_tenses()
        else :
            listetenses = []
            if past :
                listetenses.append(vconst.TensePast)
            if (past and passive ) :
                listetenses.append(vconst.TensePassivePast)
            if future : 
                listetenses.append(vconst.TenseFuture)
            if (future and passive ) :
                listetenses.append(vconst.TensePassiveFuture)
            if (future_moode) :
                listetenses.append(vconst.TenseSubjunctiveFuture)
                listetenses.append(vconst.TenseJussiveFuture)
            if (confirmed) :
                if (future):
                    listetenses.append(vconst.TenseConfirmedFuture)
                if (imperative):
                    listetenses.append(vconst.TenseConfirmedImperative)
            if (future and transitive and confirmed) :
                listetenses.append(vconst.TensePassiveConfirmedFuture)
            if (passive and future_moode) :
                listetenses.append(vconst.TensePassiveSubjunctiveFuture)
                listetenses.append(vconst.TensePassiveJussiveFuture)
            if imperative :
                listetenses.append(vconst.TenseImperative)
            result  = vbc.conjugate_all_tenses(listetenses)
        return result
    else: return None

def get_future_form(verb_vocalised, haraka = araby.FATHA):
    """
    Get The future form of a verb. for example the future form of
     qal with Damma as a Haraka of future verb, we get yqolu.
    الحصول على صيغة الفعل في المضارع، فالفعل قال، وحركة عينه في المضارع صمة، نحصل على يقول.
    @param verb_vocalised: given verb.
    @type verb_vocalised:unicode.
    @param haraka: the future mark for triverbs.
    @type haraka: unicode.
    @return: The conjugated form in the future tense.
    @rtype: unicode.
    """
    word = verb_vocalised
    transitive = True
    future_type = haraka
    if future_type not in (araby.FATHA, araby.DAMMA, araby.KASRA):
        future_type = ar_verb.get_future_type_by_name(future_type)
    vbc = classverb.VerbClass(word, transitive, future_type)
    #vb.verb_class()
    return vbc.conjugate_tense_pronoun(vconst.TenseFuture, vconst.PronounHuwa)



