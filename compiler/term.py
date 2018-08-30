# ****************************************************************************************
# ****************************************************************************************
#
#		Name:		term.py
#		Purpose:	SCPL Term Extractor
#		Date:		30th August 2018
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ****************************************************************************************
# ****************************************************************************************

from exceptions import *
from stream import *
from parser import *

# ****************************************************************************************
#									   Term classes
# ****************************************************************************************

class Term(object):
	def __init__(self,value):
		self.value = value
	def get(self):
		return self.value

class ConstantTerm(Term):
	def toString(self):
		return "C_TERM:${0:04x}".format(self.get())

class VariableTerm(Term):
	def toString(self):
		return "V_TERM:${0:04x}".format(self.get())

class StringConstantTerm(Term):
	def toString(self):
		return "S_TERM:\"{0}\"".format(self.get())

# ****************************************************************************************
#									SCPL Term Extractor
# ****************************************************************************************

class SCPLExtractor(object):
	#
	def __init__(self,parser,dictionary):
		self.parser = parser
		self.dictionary = dictionary
	#
	def get(self):
		term = self.parser.get()
		if term == "":
			raise CompilerException("Missing term")
		#
		#	identifier
		#
		if (term[0] >= 'a' and term[0] <= 'z') or term[0] == '_':
			addr = self.dictionary.find(term)
			if addr is None:
				raise CompilerException("Identifier {0} is not known".format(term))
			return VariableTerm(addr)
		#		
		# 	constant hexadecimal
		#
		if term[0] == '$':
			return ConstantTerm(int(term[1:],16) & 0xFFFF)
		#
		# 	constant decimal
		#
		if term[0] >= '0' and term[0] <= '9':
			return ConstantTerm(int(term,10) & 0xFFFF)
		#
		# 	constant character
		#
		if term[0] == "'":
			ch = self.parser.get()
			if len(ch) != 1:
				raise CompilerException("Bad character constant")
			self.parser.checkNext("'")
			return ConstantTerm(ord(ch))
		#
		# 	negative
		#
		if term == "-":
			t = self.get()
			if not isinstance(t,ConstantTerm):
				raise CompilerException("Can only negate constant terms")
			return ConstantTerm((-t.get()) & 0xFFFF)
		#
		# 	identifier address
		#
		if term == "@":
			t = self.get()
			if not isinstance(t,VariableTerm):
				raise CompilerException("Can only find address of identifier")
			return ConstantTerm(t.get())
		#
		# 	string constant
		#
		if term[0] == '"':
			return StringConstantTerm(term[1:-1])

		raise CompilerException("Cannot find term at {0}".format(term))




class DummyDictionary(object):
	def __init__(self):
		self.dict = { "a":0x1000,"b":0x2000,"a.b":0x3000,"routine":0x8000 }
	def find(self,word):
		return self.dict[word] if word in self.dict else None

if __name__ == '__main__':
	txt = """
	a.b a
	$a7f2 $00FF
	32766 15
	'*' 'x'
	-42
	@a.b
	"Hello, World !"
	""".split("\n")
	tis = TextInputStream(txt)
	parser = SCPLParser(tis)
	xtr = SCPLExtractor(parser,DummyDictionary())
	while True:
		print(xtr.get().toString())	
