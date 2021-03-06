# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		dictionary.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		9th December 2018
#		Purpose :	Dictionary Class
#
# ***************************************************************************************
# ***************************************************************************************

from identifiers import *
from errors import *

# ***************************************************************************************
#									Dictionary class
# ***************************************************************************************

class Dictionary(object):
	def __init__(self):
		self.globals = {}
		self.locals = {}
	#
	#	Add an identifier to the dictionary.
	#
	def add(self,identifier):
		target = self.globals if identifier.isGlobal() else self.locals
		if identifier.getName() in target:
			raise CompilerException("Duplicate idenifier "+identifier.getName())
		target[identifier.getName()] = identifier
	#
	#	Get an identifier from the dictionary.
	#
	def find(self,identifier):
		identifier = identifier.strip().lower()
		if identifier in self.locals:
			return self.locals[identifier]
		if identifier in self.globals:
			return self.globals[identifier]
		return None
	#
	#	Purge all locals
	#
	def purgeLocals(self):
		self.locals = {}
	#
	#	Purge all non externals
	#
	def purgeNonExternals(self):
		self.purgeLocals()
		globalIDs = self.globals
		self.globals = {}
		for x in globalIDs.keys():
			ident = globalIDs[x]
			if isinstance(ident,ProcedureIdentifier):
				if ident.isExternal():
					self.globals[ident.getName()] = ident
	#
	#	Convert dictionary to text to print
	#
	def toString(self):
		return "Globals:\n"+self.toStringSub(self.globals)+"Locals:\n"+self.toStringSub(self.locals)
	#
	def toStringSub(self,dict):
		keys = [x for x in dict.keys()]
		keys.sort()
		return "\n".join(["\t{0}".format(dict[x].toString()) for x in keys])+"\n"


class TestDictionary(Dictionary):
	def __init__(self):
		Dictionary.__init__(self)
		w = ProcedureIdentifier("hello",0x123456,True)
		w.addParameter(0x8011)
		w.addParameter(0x8013)
		self.add(w)
		self.add(VariableIdentifier("locvar",0x1234,False))
		self.add(VariableIdentifier("glbvar",0x5678,True))
		self.add(ConstantIdentifier("const1",0xABCD))


if __name__ == "__main__":
	td = TestDictionary()
	print("0-----------------------------------------")
	print(td.toString())
	print("1-----------------------------------------")
	td.purgeLocals()
	print(td.toString())
	print("2-----------------------------------------")
	td.purgeNonExternals()
	print(td.toString())
	print("3-----------------------------------------")
