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

# ****************************************************************************************
#								Code Generator base class
# ****************************************************************************************

class CodeGenerator(object):
	def __init__(self):
		self.powers2 = [ 2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768 ]
	#
	#	Basic optimiser +- 0 */ 1 and -1 or 0 xor 0 do nothing, mod 2^n becomes quicker AND
	#
	def operationTerm(self,operation,term):
		reject = False
		#
		#	mod 2^n becomes AND
		#
		if isinstance(term,ConstantTerm) and operation == "%":
			termValue = int(term.get())
			if termValue in self.powers2:
				self.operationTermRaw("&",ConstantTerm(termValue-1))
				return
		#
		#	Chuckable operations.
		#
		if isinstance(term,ConstantTerm):
			termValue = int(term.get())
			if ("+-^|").find(operation) >= 0 and termValue == 0:
				reject = True
			if ("*/").find(operation) >= 0 and termValue == 1:
				reject = True
			if operation == "&" and termValue == 0xFFFF:
				reject = True 				
		if not reject:
			self.operationTermRaw(operation,term)

# ****************************************************************************************
#		Testing Code Generator, for an imaginary assembler which hides verbosity
# ****************************************************************************************

class TestCodeGenerator(CodeGenerator):
	#
	def __init__(self):
		CodeGenerator.__init__(self)
		self.addr = 0x1000
		self.varAddr = 0xF000
		self.operators = { "+":"add","-":"sub","*":"mul","/":"div","%":"mod","&":"and","|":"orr","^":"xor", \
						   ">":"tgt","<":"tlt",">=":"tge","<=":"tle","==":"teq","!=":"tne" }
	#
	#	Get current code address
	#
	def getCurrentAddress(self):
		return self.addr
	#
	#	Allocate memory for a variable
	#
	def allocateVariableSpace(self,size):
		addr = self.varAddr
		self.varAddr += size
		return addr
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
	def operationTermRaw(self,operation,term):
		self.loadTerm(1,term)
		print("{0:04x}   {1} r0,r1".format(self.addr,self.operators[operation]))
		self.addr += 1
	#
	#	Do an indirect load through r0
	#
	def loadIndirect(self,isByte):
		print("{0:04x}   ldr r0,[{1}:r0]".format(self.addr,"BYTE" if isByte else "WORD"))
		self.addr += 1
	#
	#	Store R0 directly.
	#
	def storeDirect(self,term):
		print("{0:04x}   str r0,[${1:04x}]".format(self.addr,term.get()))
		self.addr += 1
	#
	#	Save R0 to the index register or similar
	#
	def saveAddress(self):
		print("{0:04x}   str r0,rx".format(self.addr))
		self.addr += 1
	#
	#	Store R0 indirectly through the index register
	#
	def storeIndirect(self,isByte):
		print("{0:04x}   str r0,[{1}:x]".format(self.addr,"BYTE" if isByte else "WORD"))
		self.addr += 1
	#
	#	Generate a call to the given address
	#
	def callRoutine(self,term):
		print("{0:04x}   call ${1:04x}".format(self.addr,term.get()))
		self.addr += 1
	#
	#	Generate part code for a branch with the given test on R0 (z,nz, or empty string)
	#	to be completed later.
	#
	def compileBranch(self,condition):
		condition = "mp" if condition == "" else condition
		assert condition == "mp" or condition == "z","Unsupported "+condition
		print("{0:04x}   j{1}  <somewhere>".format(self.addr,condition))
		self.addr += 1
		return self.addr-1
	#
	#	Patch branch at address to go to given address
	#
	def completeBranch(self,branchAddress,targetAddress = None):
		targetAddress = self.addr if targetAddress is None else targetAddress
		print("       ; patch branch at ${0:04x} to branch to ${1:04x}".format(branchAddress,targetAddress))
	#
	#	Push/Pull rn off the stack
	#
	def save(self,register):
		print("{0:04x}   push r{1}".format(self.addr,register))
		self.addr += 1
	#
	def restore(self,register):
		print("{0:04x}   pull r{1}".format(self.addr,register))
		self.addr += 1
