# -*- coding: utf-8 -*-
import struct as str

STYPE = 0
DTYPE = 1
UNKNOWNTYPE = 2

class VmInstruction:
	def __init__(self, data):
		self.data = data
		self.m_type = UNKNOWNTYPE
		self.m_opcode = -1
	def setType(self):
		if (self.data >> 28) == 0:
			self.m_type = STYPE
		else:
			self.m_type = DTYPE
	def type(self):
		if self.m_type == UNKNOWNTYPE:
			self.setType()
		return self.m_type
	def opcode(self):
		if self.m_opcode == -1:
			if self.type() == STYPE:
				return self.data >> 24
			else:
				return self.data >> 28
	def r1(self):
		if self.type() == DTYPE:
			return (self.data >> 14) & 0x3fff
		else:
			return self.data & 0x3fff
	def r2(self):
		if self.type() == STYPE:
			return -1
		else:
			return self.data & 0x3fff
	def imm(self):
		if self.type() == DTYPE:
			return -1
		else:
			return ((self.data >> 14) & 0x3ff)

class VmFrame:
	def __init__(self, data, index):
		self.index = index
		self.raw = data
		self.m_words = None
		self.m_instruction = None
		self.m_data = -1
	def words(self):
		if not self.m_words:
			if self.index % 2 == 0:
				self.m_words = str.unpack('di', self.raw)
			else:
				self.m_words = [ str.unpack('i', self.raw[:4])[0], str.unpack('d', self.raw[4:])[0] ]
		return self.m_words
	def instruction(self):
		if not self.m_instruction:
			if self.index % 2 == 0:
				self.m_instruction = VmInstruction(self.words()[1])
			else:
				self.m_instruction = VmInstruction(self.words()[0])
		return self.m_instruction
	def data(self):
		if self.m_data == -1:
			if self.index % 2 == 0:
				self.m_data = self.m_words[0]
			else:
				self.m_data = self.m_words[1]
		return self.m_data

class VmData:
	def __init__(self, filename):
		self.file = open(filename)
		self.framendx = 0
	def nextFrame(self):
		data = self.file.read(12)
		if len(data) == 12:
			frame = VmFrame(data, self.framendx)
			self.framendx += 1
			return frame
		else:
			return None

