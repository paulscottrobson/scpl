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
		self.pending = None
		self.putBuffer = None
	#
	#		Get a character
	#
	def _getCh(self):
		if self.pending is not None:
			ch = self.pending
			self.pending = None
		else:
			ch = self.stream.get()
		return ch
	#
	#		Put a character back
	#
	def _putCh(self,ch):
		assert self.pending is None
		self.pending = ch
	#
	#		Put a parsed item back
	#
	def put(self,item):
		assert self.putBuffer is None
		self.putBuffer = item
	#
	#		Check the next item is the given item, throw error if it isn't.
	#
	def checkNext(self,expected):
		if self.get() != expected.lower():
			raise CompilerException("Missing '{0}'".format(expected.lower()))
	#
	#		Get a parsed item. This can be
	#
	#		empty string : 			end of file
	#		quoted string :			string constant
	#		decimal constant :		integer
	#		$ and hex constant :	hexadecimal number
	#		identifier :			variable or procedure
	#		control character : 	non alphanumeric ; may also include >= <= == !=, all others one char
	#
	def get(self):
		#
		#	Check the buffer to see if something has been returned.
		#
		if self.putBuffer is not None:
			ch = self.putBuffer
			self.putBuffer = None
			return ch
		#
		#	get next character
		#
		ch = self._getCh()
		#
		#	end, return nothing (empty string)
		#
		if ch == "":
			return ""
		#
		# 	space, try again
		#
		if ch == " ":
			return self.get()
		#	
		# 	quoted string. "hello world"
		#
		if ch == '"':
			qString = ""
			ch = self._getCh()
			while ch != '"':
				if ch == "":
					return CompilerException("Unclosed quoted string")
				qString += ch
				ch = self._getCh()
			return '"'+qString+'"'
		#
		ch = ch.lower()
		#
		#	identifier (_ or a-z, followed by a-z 0-9 . _)
		#
		if ch == '_' or (ch >= 'a' and ch <= 'z'):
			identifier = ch
			ch = self._getCh().lower()
			while ch == "_" or (ch >= 'a' and ch <= 'z') or (ch >= '0' and ch <='9') or ch == '.':
				identifier += ch
				ch = self._getCh().lower()
			self._putCh(ch)
			return identifier
		#
		#	decimal integer (sequence of digits 0-9)
		#
		if ch >= '0' and ch <= '9':
			integer = ch 
			ch = self._getCh().lower()
			while ch >= '0' and ch <= '9':
				integer += ch
				ch = self._getCh().lower()
			self._putCh(ch)
			return integer			
		#
		#	hexadecimal integer ($ followed by sequence of hex digits)
		#
		if ch == '$':
			hexInt = "$"
			ch = self._getCh().lower()
			while (ch >= '0' and ch <= '9') or (ch >= 'a' and ch <= 'f'):
				hexInt += ch
				ch = self._getCh().lower()
			self._putCh(ch)
			if len(hexInt) == 1:
				raise CompilerException("Missing hexadecimal constant")
			return hexInt
		#
		#	control character. < > = and ! may be followed by an equals.
		#
		if ch == ">" or ch == "<" or ch == "=" or ch == "!":
			c2 = self._getCh()
			if c2 == '=':
				ch = ch + c2
			else:
				self._putCh(c2)
		return ch

if __name__ == '__main__':
	txt = """
	a.b _w+count.test > >= == <= != & % * 	// comment
	"Hello, World !"
	1234+$a7f2!42 	// hello world
	""".split("\n")
	tis = TextInputStream(txt)
	parser = SCPLParser(tis)
	item = parser.get()
	while item != "":
		print(item)
		item = parser.get()
	