# ****************************************************************************************
# ****************************************************************************************
#
#		Name:		binary.py
#		Purpose:	SCPL Binary Stores
#		Date:		31st August 2018
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ****************************************************************************************
# ****************************************************************************************

from exceptions import *
import sys,os

# ****************************************************************************************
#									Base Binary Objects
# ****************************************************************************************

class BinaryObject(object):
	#
	#		Set up
	#
	def __init__(self):
		self.memory = [ 0 ] * self.getMemorySize() 						# allocate memory
		self.pointer = self.initialise(self.memory)
		self.highAddress = 0
	#
	#		Raw read write functions
	#
	def readRaw(self,addr):
		assert addr >= 0 and addr < len(self.memory)
		return self.memory[addr]
	def writeRaw(self,addr,data):
		assert addr >= 0 and addr < len(self.memory)
		assert data >= 0 and data < 256
		self.memory[addr] = data
		self.highAddress = max(self.highAddress,addr)
	#		
	#		Accessors/Mutators
	#
	def readByte(self,addr):
		return self.readRaw(addr)
	#
	def readWord(self,addr):
		return self.readRaw(addr) + (self.readRaw(addr+1) << 8)
	#
	def writeByte(self,addr,data):
		self.writeRaw(addr,data)
	#
	def writeWord(self,addr,data):
		self.highAddress = max(addr+1,self.highAddress)
		self.writeRaw(addr,data & 0xFF)
		self.writeRaw(addr+1,data >> 8)
	#
	def getPointer(self):
		return self.pointer 
	#
	def cByte(self,data):
		if self.echo is not None:
			c = '.' if (data & 0x7F) < 32 else chr(data & 0x7F)
			self.echo.write("\t{0:02x}:{1:04x}   {2:02x}   {3}\n".format(self.pointer >> 16,self.pointer & 0xFFFF,data,c))
		self.writeByte(self.pointer,data)
		self.pointer += 1
	#
	def cWord(self,data):
		if self.echo is not None:
			self.echo.write("\t{0:02x}:{1:04x}   {2:04x}\n".format(self.pointer >> 16,self.pointer & 0xFFFF,data))
		self.writeWord(self.pointer,data)
		self.pointer += 2	
	#
	#		Save memory out
	#
	def save(self,writeName):
		h = open(writeName+"."+self.getFileType(),"wb")
		h.write(bytes(self.getWriteChunk()))
		h.close()
	#
	#		Delete target
	#
	def deleteTarget(self,writeName):
		if os.path.exists(writeName+".sna"):
			os.remove(writeName+".sna")

# ****************************************************************************************
#								Spectrum 48k .SNA format
# ****************************************************************************************

class Spectrum48kSNA(BinaryObject):
	#
	#		Get Memory size
	#
	def getMemorySize(self):
		return 0x10000
	#
	#		Initialise
	#
	def initialise(self,memory):
		self.dataMemory = 0x6000
		self.startAddress = 0x5B00
		return 0x8000
	#
	#		Get the chunk of memory for writing
	#
	def getWriteChunk(self):
		self.pointer = 0x4000-27											# 27 byte SNA header
		self.echo = None
		self.cByte(0x3F)
		for i in range(0,9):
			self.cWord(0)
		for i in range(0,4):
			self.cByte(0)
		self.cWord(0x5AFE)													# SP, pop start addr from here
		self.cByte(1)
		self.cByte(7)
		assert self.pointer == 0x4000
		self.writeWord(0x5AFE,self.startAddress)			
		return self.memory[0x4000-27:0x10000]								# return the .SNA chunk.
	#
	#		Get the file type
	#
	def getFileType(self):
		return "sna"

if __name__ == '__main__':
	sna = Spectrum48kSNA()
	sna.save("test")

	