# ****************************************************************************************
# ****************************************************************************************
#
#		Name:		exceptions.py
#		Purpose:	SCPL Compiler Exception Class(es)
#		Date:		6th November 2018
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
		CompilerException.lineNumber = 0
		CompilerException.sourceFile = "(Unknown)"
	def getMessage(self):
		return "{0} in {1}:{2}".format(self.error,CompilerException.sourceFile,CompilerException.lineNumber)

if __name__ == '__main__':
	try:
		raise CompilerException("Hello world")
	except CompilerException as e:
		print(e.getMessage())

	