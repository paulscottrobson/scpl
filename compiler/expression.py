# ****************************************************************************************
# ****************************************************************************************
#
#		Name:		expression.py
#		Purpose:	SCPL Expression Compiler
#		Date:		30th August 2018
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ****************************************************************************************
# ****************************************************************************************

from exceptions import *
from stream import *
from parser import *
from term import *
from codegenerator import *

# ****************************************************************************************
# 									Expression compiler
# ****************************************************************************************

class ExpressionCompiler(object):
	#
	def __init__(self,parser,dictionary,codeGenerator):
		self.parser = parser
		self.dictionary = dictionary
		self.codeGenerator = codeGenerator
		self.termExtractor = SCPLExtractor(parser,dictionary)
		self.operators = { "+":"","-":"","*":"","/":"","%":"","!":"","?":"","&":"","|":"","^":"", \
						   ">":"","<":"",">=":"","<=":"","==":"","!=":"" }
	#
	#	Compile an expression
	#
	def compileExpression(self):
		lTerm = self.termExtractor.get()									# get first term
		self.codeGenerator.loadTerm(0,lTerm)								# load term into register 0
		operator = self.parser.get() 										# get the next operator, maybe

		while operator in self.operators:									# while a known operator.
			if operator == "!" or operator == "?":
				self.codeGenerator.operationTerm("+",self.termExtractor.get())
				self.codeGenerator.loadIndirect(operator == "?")
			else:
				self.codeGenerator.operationTerm(operator,self.termExtractor.get())
			operator = self.parser.get()

		self.parser.put(operator)											# put it back, not operator

if __name__ == '__main__':
	txt = """

	a == a
	a.b + 8
	42 * 5 >= 8
	"hello" != b
	@a.b
	a?4
	a!4
	a+0
	a*1
	a|0
	a % 7
	a % 16
	""".split("\n")
	tis = TextInputStream(txt)
	parser = SCPLParser(tis)
	xc = ExpressionCompiler(parser,DummyDictionary(),TestCodeGenerator())
	while True:
		xc.compileExpression()
		print("----------------------------")	

		