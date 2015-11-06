#!/usr/bin/python
# -*- coding = utf-8 -*-
#************************************************************************
# $Id: ar_verb.py, v 0.7 2009/06/02 01:10:00 Taha Zerrouki $
#
# ------------
# Description:
# ------------
#  Copyright (c) 2009, Arabtechies, Arabeyes Taha Zerrouki
#
#  Elementary function to manipulate arabic texte
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
Basic routines to treat verbs
ar_verb
"""

import pyarabic.araby as araby
import libqutrub.triverbtable as triverbtable
TRIVERBTABLE_INDEX = {}

def create_index_triverbtable():
    """ Create index from the verb dictionary
    to accelerate the search in the dictionary for verbs
    @return: create the TRIVERBTABLE_INDEX
    @rtype: None
    """
    # the key is the vocverb + the bab number
    for key in triverbtable.TriVerbTable.keys():
        vocverb = triverbtable.TriVerbTable[key]['verb']
        unvverb = araby.strip_harakat(vocverb)
        normverb = araby.normalize_hamza(unvverb)
        if TRIVERBTABLE_INDEX.has_key(normverb):
            TRIVERBTABLE_INDEX[normverb].append(key)
        else:
            TRIVERBTABLE_INDEX[normverb] = [key, ]



def find_alltriverb(triverb, givenharaka = araby.FATHA, 
vocalised_entree = False):
    """
    Find the triliteral verb in the dictionary (TriVerbTable)
    return a list of possible verb forms
    each item contains:
        - 'root':
        - 'haraka:
        - 'bab':
        - 'transitive':
    @param triverb: given verb.
    @type triverb: unicode.
    @param givenharaka: given haraka of tuture type of the verb, 
    default(FATHA).
    @type givenharaka: unicode.
    @param VocalisedEntree: True if the given verb is vocalized, 
    default False.
    @type VocalisedEntree: Boolean.
    @return: list of triliteral verbs.
    @rtype: list of dicts.
    """
    liste = []

    if vocalised_entree:
        verb_nm = araby.strip_harakat(triverb)
    else:
        verb_nm = triverb

    normalized = araby.normalize_hamza(verb_nm)
    if TRIVERBTABLE_INDEX.has_key(normalized):
        for verb_voc_id in TRIVERBTABLE_INDEX[normalized]:
            if triverb == triverbtable.TriVerbTable[verb_voc_id]['verb'] and \
             givenharaka == triverbtable.TriVerbTable[verb_voc_id]['haraka']:
                liste.insert(0, triverbtable.TriVerbTable[verb_voc_id])
#            if VocalisedEntree:
                #if verb_voc_id[:-1] == triverb:
                #    liste.append(TriVerbTable[verb_voc_id])
            else:
                liste.append(triverbtable.TriVerbTable[verb_voc_id])
    else:
        print "triverb has no verb"
    return liste



def find_triliteral_verb(db_base_path, triliteralverb, givenharaka):
    """
    Find the triliteral verb in the dictionary, 
    return a list of possible verb forms
    @param db_base_path: the database path
    @type db_base_path: path string.
    @param triliteralverb: given verb.
    @type triliteralverb: unicode.
    @param givenharaka: given haraka of tuture type of the verb.
    @type givenharaka: unicode.
    @return: list of triliteral verbs.
    @rtype: list of unicode.
    """
    liste = []
    try:
        import sqlite3 as sqlite
        import os
#     db_path = os.path.join(_base_directory(req), "data/verbdict.db")
        db_path = os.path.join(db_base_path, "data/verbdict.db")
        conn  =  sqlite.connect(db_path)
        cursor  =  conn.cursor()
        verb_nm = araby.strip_harakat(triliteralverb)
        tup = (verb_nm, )
        cursor.execute("""select verb_vocalised, haraka, transitive 
                    from verbdict
                    where verb_unvocalised = ?""", tup)
        for row in cursor:
            verb_vocalised = row[0]
            haraka = row[1]
            transitive = row[2]
            # Return the transitivity option
            #MEEM is transitive
            # KAF is commun ( transitive and intransitive)
            # LAM is intransitive
            if transitive in (araby.KAF, araby.MEEM):
                transitive = True
            else:
                transitive = False
# if the given verb is the list, 
#it will be inserted in the top of the list, 
#to be treated in prior
            if triliteralverb == verb_vocalised and givenharaka == haraka:
                liste.insert(0, {"verb":verb_vocalised, 
                "haraka":haraka, "transitive":transitive})
# else the verb is appended in the liste
            else:
                liste.append({"verb":verb_vocalised, 
                "haraka":haraka, "transitive":transitive})
        cursor.close()
        return liste
    except IOError:
        return None
