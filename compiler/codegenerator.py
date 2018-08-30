# ****************************************************************************************
# ****************************************************************************************
#
#		Name:		codegenerator.py
#		Purpose:	SCPL Code Generators
#		Date:		30th August 2018
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ****************************************************************************************
# ****************************************************************************************

from term import *

class TestCodeGenerator(object):
	#
	def __init__(self):
		self.addr = 0x1000
		self.operators = { "+":"add","-":"sub","*":"mul","/":"div","%":"mod","&":"and","|":"orr","^":"xor", \
						   ">":"tgt","<":"tlt",">=":"tge","<=":"tle","==":"teq","!=":"tne" }

	#
	#	Generate code to load the given term into one of the three registers.
	#
	def loadTerm(self,register,term):
		if isinstance(term,ConstantTerm):
			print("{0:04x}   ldr r{1},#${2:04x}".format(self.addr,register,term.get()))
		if isinstance(term,VariableTerm):
			print("{0:04x}   ldr r{1},[${2:04x}]".format(self.addr,register,term.get()))
		if isinstance(term,StringConstantTerm):
			print("{0:04x}   ldr r{1},#'{2}'".format(self.addr,register,term.get()))
		self.addr += 1
	#
	#	Generate code to perform given operation on term between R0 and the given term.
	#
	#	optimisations +/- constants, shift constants for * / , and constants for mod (2^n-1)
	#	always present +/- zero
	#
	def operationTerm(self,operation,term):
		self.loadTerm(1,term)
		print("{0:04x}   {1} r0,r1".format(self.addr,self.operators[operation]))
		self.addr += 1
	#
	#	Do an indirect load through r0
	#
	def loadIndirect(self,isByte):
		print("{0:04x}   ldr r0,[{1}:r0]".format(self.addr,"BYTE" if isByte else "WORD"))
		self.addr += 1

