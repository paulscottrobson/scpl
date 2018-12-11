# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		democodegenerator.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		11th December 2018
#		Purpose :	Imaginary language code generator.
#
# ***************************************************************************************
# ***************************************************************************************

class DemoCodeGenerator(object):
	def __init__(self):
		self.addr = 0x1000
		self.strAddr = 0x2000

	def stringConstant(self,str):
		print("{0:04x} : db    '{1}',0".format(self.strAddr,str))
		strAddr = self.strAddr
		self.strAddr = self.strAddr + len(str) + 1
		return strAddr

