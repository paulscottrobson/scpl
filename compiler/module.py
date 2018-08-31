# ****************************************************************************************
# ****************************************************************************************
#
#		Name:		module.py
#		Purpose:	SCPL Instruction Compiler
#		Date:		31st August 2018
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
from instruction import *
from dictionary import *

# ****************************************************************************************
# 									Instruction compiler
# ****************************************************************************************

class ModuleCompiler(object):
	#
	def __init__(self,dictionary,codeGenerator):
		self.dictionary = dictionary
		self.codeGenerator = codeGenerator
	#
	#	Compile a module
	#
	def compileModule(self,parser):
		self.parser = parser
		self.instructionCompiler = InstructionCompiler(parser,self.dictionary,self.codeGenerator)

		nextWord = self.parser.get()
		while nextWord != "":
			self.compileItem(nextWord)
			nextWord = self.parser.get()
		self.dictionary.endModule()
	#
	#	Compile a single item
	#
	def compileItem(self,word):
		if word == "var":
			self.instructionCompiler.compileVariableDefinition(False)
			return

		if word == "procedure":
			isLocalToModule = False
			procName = self.parser.get()
			if procName == "local":
				procName = self.parser.get()
				isLocalToModule = True
			if procName == "" or procName[0] < 'a' or procName[0] > 'z':
				raise CompilerException("Bad procedure name")
			procAddress = self.codeGenerator.getCurrentAddress()
			self.parser.checkNext("(")
			nextItem = self.parser.get()
			paramCount = 0
			while nextItem != ")":
				if nextItem == "" or nextItem[0] < 'a' or nextItem[0] > 'z':
					raise CompilerException("Bad parameter name")
				varAddress = self.codeGenerator.allocateVariableSpace(2)
				self.dictionary.add(nextItem,varAddress,0,True,True,True)
				self.codeGenerator.storeDirect(VariableTerm(varAddress),paramCount)
				paramCount += 1
				nextItem =self.parser.get()
				if nextItem == ",":
					nextItem =self.parser.get()
			self.dictionary.add(procName,procAddress,paramCount,False,False,isLocalToModule)
			self.instructionCompiler.compileInstruction()
			self.codeGenerator.compileReturn()
			self.dictionary.endProcedure()
			return

		raise CompilerException("Syntax error")
		
if __name__ == '__main__':
	txt = """
		var aa;
		var p1;
		var p2;
		var p3;
		var bb[42];
		var result;
		procedure local test1(p1,p2,p3) { 
			aa = 42;
			var p4;
			test1(@aa,bb);
			p1!0 = p2+p3; 
		}

		procedure test2() {
			test1('1',-2,"hello");
		}
	""".split("\n")
	tis = TextInputStream(txt)
	parser = SCPLParser(tis)
	xc = ModuleCompiler(Dictionary(),TestCodeGenerator())
	xc.compileModule(parser)
		