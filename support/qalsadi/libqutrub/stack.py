#!/usr/bin/python
# -*- coding=utf-8 -*-
#************************************************************************
# from arabic_const import *
from pyarabic.araby import *
from verb_const import *
class Stack :
	def __init__(self,text="") :
		self.items = list(text);

	def push(self, item) :
		self.items.append(item)

	def pop(self) :
		if not self.isEmpty():
			return self.items.pop()
		else:
			return None;

	def isEmpty(self) :
		return (self.items == [])


def separate(word):
	"""
	separate the letters from the vowels, in arabic word,
	if a letter hasn't a haraka, the not definited haraka is attributed.
	return ( letters,vowels);
	"""
	#debug=True;
	stack1=Stack(word)
	# the word is inversed in the stack
	stack1.items.reverse();
	letters=Stack()
	marks=Stack()
	vowels=('a','u')
	last1=stack1.pop();
	# if the last element must be a letter,
	# the arabic word can't starts with a haraka
	# in th stack the word is inversed
	while last1 in vowels: last1=stack1.pop();
	while  last1!=None:
		if last1 in vowels:
			# we can't have two harakats beside.
			# the shadda is considered as a letter
			marks.pop();
			marks.push(last1);
		elif last1==SHADDA:
			# is the element is a Shadda,
			# the previous letter must have a sukun as mark,
			# and the shadda take the indefinate  mark
			marks.pop();
			marks.push(SUKUN);
			marks.push(NOT_DEF_HARAKA);
			letters.push(SHADDA);
		else:
			marks.push(NOT_DEF_HARAKA);
			letters.push(last1);
		last1=stack1.pop();
	return (''.join(letters.items),''.join(marks.items))


def joint(letters,marks):
	"""
	joint the letters with the marks
	the length ot letters and marks must be equal
	return word;
	"""
	#debug=True;
	debug=False;
	# The length ot letters and marks must be equal
	if len(letters)!=len(marks): return "";

	stackLetter=Stack(letters)
	stackLetter.items.reverse();
	stackMark=Stack(marks)
	stackMark.items.reverse();
	wordStack=Stack();
	last1=stackLetter.pop();
	last2=stackMark.pop();

	vowels=('a','u','o','i',SUKUN)
	while  last1!=None and  last2!=None:
		if last1 == SHADDA:
			top=wordStack.pop();
			if top not in vowels:
				wordStack.push(top);
			wordStack.push(last1);
			if last2!= NOT_DEF_HARAKA:
				wordStack.push(last2);
		else:
			wordStack.push(last1);
			if last2!= NOT_DEF_HARAKA:
				wordStack.push(last2);

		last1=stackLetter.pop();
		last2=stackMark.pop();
	if not (stackLetter.isEmpty() and stackMark.isEmpty()):
		return False;
	else:
		#wordStack.items.reverse();
		return ''.join(wordStack.items);

def vocalizedlike(word1,word2):
	"""
	if the two words has the same letters and the same harakats, this fuction return True.
	The two words can be full vocalized, or partial vocalized
	"""
	debug=False;
	stack1=Stack(word1)
	stack2=Stack(word2)
	last1=stack1.pop();
	last2=stack2.pop();
	if debug: print "+0", stack1, stack2;
	vowels=('a','u')
	while  last1!=None and  last2!=None:
		if last1==last2:
			if debug: print "+2", stack1.items,last1, stack2.items,last2
			last1=stack1.pop();
			last2=stack2.pop();
		elif last1 in vowels and last2 not in vowels:
			if debug: print "+2", stack1.items,last1, stack2.items,last2
			last1=stack1.pop();
		elif last1 not in vowels and last2 in vowels:
			if debug: print "+2", stack1.items,last1, stack2.items,last2
			last2=stack2.pop();
		else:
			if debug: print "+2", stack1.items,last1, stack2.items,last2
			break;
	if not (stack1.isEmpty() and stack2.isEmpty()):
		return False;
	else: return True;
#-------------------------
# Function def vaznlike(word1,wazn):
#-------------------------
def waznlike(word1,wazn):
	"""
	if the  word1 is like a wazn (pattern),
	the letters must be equal,
	the wazn has FEH, AIN, LAM letters.
	this are as generic letters.
	The two words can be full vocalized, or partial vocalized
	"""
	debug=False;
	stack1=Stack(word1)
	stack2=Stack(wazn)
	root=Stack()
	last1=stack1.pop();
	last2=stack2.pop();
	if debug: print "+0", stack1, stack2;
	vowels=('a','u')
	while  last1!=None and  last2!=None:
		if last1==last2 and last2 not in (FEH, AIN,LAM):
			if debug: print "+2", stack1.items,last1, stack2.items,last2
			last1=stack1.pop();
			last2=stack2.pop();
		elif last1 not in vowels and last2 in (FEH, AIN,LAM):
			if debug: print "+2", stack1.items,last1, stack2.items,last2
			root.push(last1);
			print "t";
			last1=stack1.pop();
			last2=stack2.pop();
		elif last1 in vowels and last2 not in vowels:
			if debug: print "+2", stack1.items,last1, stack2.items,last2
			last1=stack1.pop();
		elif last1 not in vowels and last2 in vowels:
			if debug: print "+2", stack1.items,last1, stack2.items,last2
			last2=stack2.pop();
		else:
			if debug: print "+2", stack1.items,last1, stack2.items,last2
			break;
	# reverse the root letters
	root.items.reverse();
	print " the root is ", root.items#"".join(root.items);
	if not (stack1.isEmpty() and stack2.isEmpty()):
		return False;
	else: return True;
