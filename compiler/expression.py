# ****************************************************************************************
# ****************************************************************************************
#
#		Name:		expression.py
#		Purpose:	SCPL Expression Compiler
#		Date:		30th August 2018
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ****************************************************************************************
# ****************************************************************************************

from exceptions import *
from stream import *
from parser import *
from term import *

# ****************************************************************************************
# 									Expression compiler
# ****************************************************************************************


if __name__ == '__main__':
	txt = """
	a.b a
	$a7f2 $00FF
	32766 15
	'*' 'x'
	-42
	&a.b
	"Hello, World !"
	""".split("\n")
	tis = TextInputStream(txt)
	parser = SCPLParser(tis)
	xtr = SCPLExtractor(parser,DummyDictionary())
	while True:
		print(xtr.get().toString())	
	