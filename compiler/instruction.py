# ****************************************************************************************
# ****************************************************************************************
#
#		Name:		instruction.py
#		Purpose:	SCPL Instruction Compiler
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
from expression import *

# ****************************************************************************************
# 									Instruction compiler
# ****************************************************************************************

class InstructionCompiler(object):
	#
	def __init__(self,parser,dictionary,codeGenerator):
		self.parser = parser
		self.dictionary = dictionary
		self.codeGenerator = codeGenerator
		self.termExtractor = SCPLExtractor(parser,dictionary)
		self.expressionCompiler = ExpressionCompiler(parser,dictionary,codeGenerator)
	#
	#	Compile an instruction
	#
	def compileInstruction(self):
		item = self.parser.get()											# get first term
		if item == "":
			raise CompilerException("Missing instruction")
		#
		#	Handle code blocks
		#
		if item == "{":														# code block.
			nextItem = self.parser.get()									# what follows
			while nextItem != "}":											# keep going till block end.
				self.parser.put(nextItem)
				self.compileInstruction()
				nextItem = self.parser.get()
			return
		#
		#	if statement
		#

		#
		#	while statement
		#

		#
		#	for statement
		#

		#
		#	Check for a known identifier.
		#
		if item[0] < 'a' or item[0] > 'z':									# give up :)
			raise CompilerException("Syntax error")
		self.parser.put(item) 												# put back and get as a term.
		term = self.termExtractor.get()

		nextItem = self.parser.get() 										# what follows the identifier ?
		if nextItem == "(":													# procedure call
			paramCount = 0
			nextItem = self.parser.get()
			if nextItem != ")":
				self.parser.put(nextItem)
				while nextItem != ")":
					term = self.termExtractor.get()					
					self.codeGenerator.loadTerm(paramCount,term)
					paramCount += 1
					if paramCount == 4:
						raise CompilerException("Bad parameter")
					nextItem = self.parser.get()
			if nextItem != ")":
				raise CompilerException("Missing ) in procedure call")
			self.parser.checkNext(";")
			self.codeGenerator.callRoutine(term)
			return

		if nextItem == "!" or nextItem == "?":								# indirect
			self.codeGenerator.loadTerm(0,term)								# load first part
			rTerm = self.termExtractor.get()								# add second part
			self.codeGenerator.operationTerm("+",rTerm)
			self.codeGenerator.saveAddress()								# save the address.
			self.parser.checkNext("=")
			self.expressionCompiler.compileExpression()						# compile the value to assign
			self.codeGenerator.storeIndirect(nextItem == "?")				# and write it out
			self.parser.checkNext(";")
			return
		if nextItem != "=":													# must be an assignment
			raise CompilerException("Missing = in assignment")
		self.expressionCompiler.compileExpression()							# compile the value to assign
		self.codeGenerator.storeDirect(term)								# and write it out
		self.parser.checkNext(";")

if __name__ == '__main__':
	txt = """
	{
	a = b + 1;
	a!4 = a * 2;	
	a?4 = 'c';
	routine($101,a,b);
	}
	""".split("\n")
	tis = TextInputStream(txt)
	parser = SCPLParser(tis)
	xc = InstructionCompiler(parser,DummyDictionary(),TestCodeGenerator())
	xc.compileInstruction()
		