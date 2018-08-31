# ****************************************************************************************
# ****************************************************************************************
#
#		Name:		dictionary.py
#		Purpose:	SCPL Dictionary
#		Date:		31st August 2018
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ****************************************************************************************
# ****************************************************************************************

from exceptions import *

# ****************************************************************************************
#									Dictionary Class
# ****************************************************************************************

class Dictionary(object):
	#
	#		Set up
	#
	def __init__(self):
		self.locals = {}
		self.globals = {}
	#
	#		Find word, check local scope first then global scope
	#
	def find(self,word):
		if word in self.locals:
			return self.locals[word]["address"]
		if word in self.globals:
			return self.globals[word]["address"]
		return None
	#
	#		Add a word to the dictionary
	#
	def add(self,name,addr,paramCount,isLocal,isVariable,moduleOnly):

		target = self.locals if isLocal else self.globals		
		if name in target:
			raise CompilerException("Duplicate dictionary item "+name)
		target[name] = { "name":name,"address":addr,"paramcount":paramCount, \
					   	 "isvariable":isVariable,"moduleonly":moduleOnly }
	#
	#		End of procedure - clear locals
	#
	def endProcedure(self):
		self.locals = {}
	#
	#		End of modules - clear locals and globals marked 'moduleOnly'
	#
	def endModule(self):
		oldGlobals = self.globals
		self.locals = {}
		self.globals = {}
		for k in oldGlobals.keys():
			if not oldGlobals[k]["moduleonly"]:
				self.globals[k] = oldGlobals[k]
