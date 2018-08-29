# ****************************************************************************************
# ****************************************************************************************
#
#		Name:		stream.py
#		Purpose:	SCPL Input Stream
#		Date:		29th August 2018
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ****************************************************************************************
# ****************************************************************************************

# ****************************************************************************************
#									Base Input Stream
# ****************************************************************************************

class InputStream(object):
	def get(self):
		assert False
	def getLineNumber(self):
		assert False
	def getSourceName(self):
		assert False

# ****************************************************************************************
#									Text Input Stream
# ****************************************************************************************

class TextInputStream(InputStream):
	#
	#		Set up
	#
	def __init__(self,source):
		# Remove tabs and spaces
		self.source = [x.replace("\t"," ").strip() for x in source]
		# Remove comment
		self.source = [x.strip() if x.find("//") < 0 else x[:x.find("//")].strip() for x in source]
		# Add space to every line so there is a gap.
		self.source = [x + " " for x in self.source]
		# Position in text
		self.charPosition = 0
		self.lineNumber = 0
	#
	#		Get character, return "" if none left.
	#
	def get(self):
		if self.lineNumber >= len(self.source):
			return ""
		if self.charPosition >= len(self.source[self.lineNumber]):
			self.charPosition = 0
			self.lineNumber += 1
			return self.get()
		ch = self.source[self.lineNumber][self.charPosition]
		self.charPosition += 1
		return ch
	#
	#		Get positional details on error.
	#
	def getSourceName(self):
		return "(text source)"
	def getLineNumber(self):
		return self.lineNumber + 1

		
if __name__ == '__main__':
	txt = """
	a b w 	// comment
	1234 	// hello world
	""".split("\n")
	tis = TextInputStream(txt)
	c = tis.get()
	while c != "":
		print(c,tis.getLineNumber(),tis.getSourceName())
		c = tis.get()

	