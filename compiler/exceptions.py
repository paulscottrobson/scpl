# ****************************************************************************************
# ****************************************************************************************
#
#		Name:		exceptions.py
#		Purpose:	SCPL Compiler Exception Class(es)
#		Date:		29th August 2018
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ****************************************************************************************
# ****************************************************************************************

# ****************************************************************************************
#										Compiler Exception
# ****************************************************************************************

class CompilerException(Exception):
	def __init__(self,msg):
		Exception.__init__(self)
		self.error = msg
		print("Raised "+msg)
	def getMessage(self):
		return self.error

if __name__ == '__main__':
	raise CompilerException("Hello world")
	