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
		if item == "if":													# conditional block
			self.compileCondition()											# test
			branchAddress = self.codeGenerator.compileBranch("z")			# if zero skip
			self.compileInstruction()										# compiled instruction
			self.codeGenerator.completeBranch(branchAddress)
			return
		#
		#	while statement
		#
		if item == "while":													# main loop.
			loopAddress = self.codeGenerator.getCurrentAddress()			# top of while
			self.compileCondition()
			branchAddress = self.codeGenerator.compileBranch("z")			# exit loop if zero
			self.compileInstruction()										# otherwise do code
			returnBranch = self.codeGenerator.compileBranch("")				# and loop back
			self.codeGenerator.completeBranch(returnBranch,loopAddress)				
			self.codeGenerator.completeBranch(branchAddress)				# fix up branch out
			return
		#
		#	repeat statement
		#
		if item == "repeat":												# simple repeat n times
			self.compileCondition()											# actually a count.
			repeatLoop = self.codeGenerator.getCurrentAddress()				# come back here.
			branchAddress = self.codeGenerator.compileBranch("z")			# if zero, completed.
			self.codeGenerator.operationTerm("-",ConstantTerm(1))			# decrement it.
			self.codeGenerator.save(0)										# code to save R0
			self.compileInstruction()										# do instruction
			self.codeGenerator.restore(0)									# get R0 back.
			returnBranch = self.codeGenerator.compileBranch("")				# loop back
			self.codeGenerator.completeBranch(returnBranch,repeatLoop)
			self.codeGenerator.completeBranch(branchAddress)				# fix up branch out
			return
		#
		#	variable definition
		#
		if item == "var":													# variable definition
			self.compileVariableDefinition(True)
			return
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
					term1 = self.termExtractor.get()					
					self.codeGenerator.loadTerm(paramCount,term1)
					paramCount += 1
					if paramCount == 4:
						raise CompilerException("Bad parameter count")
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
		self.codeGenerator.storeDirect(term,0)								# and write it out
		self.parser.checkNext(";")
	#
	#		Compile a condition with optional brackets
	#
	def compileCondition(self):
		nextToken = self.parser.get()
		if nextToken == "(":
			self.expressionCompiler.compileExpression()
			self.parser.checkNext(")")
		else:
			self.parser.put(nextToken)
			self.expressionCompiler.compileExpression()
	#
	#		Variable definition.
	#
	def compileVariableDefinition(self,isLocal):
		varName = self.parser.get()											# get name
		if varName == "" or varName[0] < 'a' or varName[0] > 'z':			# check legal
			raise CompilerException("Bad variable name")
		size = 2															# size of element
		nextItem = self.parser.get()										# check for [
		if nextItem == "[":	
			size = self.termExtractor.get()
			if not isinstance(size,ConstantTerm):
				raise CompilerException("Variable size must be a constant")
			size = int(size.get())
			self.parser.checkNext("]")
		else:
			self.parser.put(nextItem)

		varAddress = self.codeGenerator.allocateVariableSpace(size)			# allocate it
		self.dictionary.add(varName,varAddress,0,isLocal,True,True)			# add to dictionary
		self.parser.checkNext(";")

if __name__ == '__main__':
	txt = """
	{
	a = b + 1;
	a!4 = a * 2;	
	a?4 = 'c';
	routine($101,a,b);
	if (a == 0) b = b + 1;
	while (b) b = b - 1;
	repeat (24) { a = a + 1; b = b - 1 ;}
	var x[42];
	var y;
	var aa;
	aa(x,y);
	}
	""".split("\n")
	tis = TextInputStream(txt)
	parser = SCPLParser(tis)
	xc = InstructionCompiler(parser,DummyDictionary(),TestCodeGenerator())
	xc.compileInstruction()
		