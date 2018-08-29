# ****************************************************************************************
# ****************************************************************************************
#
#		Name:		parser.py
#		Purpose:	SCPL Input Stream Parser
#		Date:		29th August 2018
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ****************************************************************************************
# ****************************************************************************************

from exceptions import *
from stream import *

# ****************************************************************************************
#									Text Input Stream
# ****************************************************************************************

class SCPLParser(InputStream):
	#
	#		Set up
	#
	def __init__(self,stream):
		self.stream = stream

		
if __name__ == '__main__':
	txt = """
	a.b _w > >= == <= != & % * 	// comment
	"Hello, World !"
	1234 	// hello world
	""".split("\n")
	tis = TextInputStream(txt)
	print(txt)
	