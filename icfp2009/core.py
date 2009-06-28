# -*- coding: utf-8 -*-
from decode import VmData, VmInstruction, DTYPE, STYPE
import math
import struct

CONFIG = 0x3e80

class Vm:
	def __init__(self, datapath):
		self.m_memory = MemoryManager()
		self.m_memory.loadVmData(VmData(datapath))
		self.dtype_handlers = [
			0,
			self.add,
			self.sub,
			self.mult,
			self.div,
			self.output,
			self.phi]
		self.stype_handlers = [
			self.noop,
			self.cmpz,
			self.sqrt,
			self.copy,
			self.input]
		self.comp_handlers = [
			lambda x: x < 0,
			lambda x: x <= 0,
			lambda x: x == 0,
			lambda x: x >= 0,
			lambda x: x > 0]
	def memory(self):
		return self.m_memory
	def cycle(self):
		self.inst_index = 0
		instruction = self.m_memory.instruction(self.inst_index)
		while self.inst_index <= self.memory().inst_count:
			if instruction.type() == DTYPE:
				self.dtype_handlers[instruction.opcode()](instruction)
			else:
				self.stype_handlers[instruction.opcode()](instruction)
			self.inst_index += 1
			instruction = self.m_memory.instruction(self.inst_index)
	def add(self, instruction):
		dr1, dr2 = self.dr1and2(instruction)
		self.result(dr1 + dr2)
	def sub(self, instruction):
		dr1, dr2 = self.dr1and2(instruction)
		self.result(dr1 - dr2)
	def mult(self, instruction):
		dr1, dr2 = self.dr1and2(instruction)
		self.result(dr1 * dr2)
	def div(self, instruction):
		dr1, dr2 = self.dr1and2(instruction)
		if dr2 == 0:
			result = 0
		else:
			result = dr1 / dr2
		self.result(result)
	def output(self, instruction):
		self.memory().setOutput(instruction.r1(), self.memory().data(instruction.r2()))
	def phi(self, instruction):
		if self.memory().status():
			res = self.memory().data(instruction.r1())
		else:
			res = self.memory().data(instruction.r2())
		self.result(res)
	def noop(self, instruction):
		pass
	def cmpz(self, instruction):
		self.memory().setStatus(self.comp_handlers[instruction.imm() >> 7](self.memory().data(instruction.r1())))
	def sqrt(self, instruction):
		self.result(math.sqrt(self.m_memory.data(instruction.r1())))
	def copy(self, instruction):
		self.result(self.m_memory.data(instruction.r1()))
	def input(self, instruction):
		self.result(self.m_memory.input(instruction.r1()))
	def dr1and2(self, instruction):
		return self.m_memory.data(instruction.r1()), self.m_memory.data(instruction.r2())
	def result(self, result):
		self.m_memory.setData(self.inst_index, result)

class MemoryManager:
	def __init__(self):
		self.address_space = 2**14
		self.m_instmem = [0 for x in xrange(self.address_space)]
		self.m_datamem = [0 for x in xrange(self.address_space)]
		self.m_output = [0 for x in xrange(self.address_space)]
		self.m_input = [0 for x in xrange(self.address_space)]
		self.m_status = False
	def loadVmData(self, vmdata):
		buff = vmdata.file.read(24)
		self.inst_count = 0
		while len(buff) == 24:
			words = struct.unpack('diid', buff)
			self.m_instmem[self.inst_count] = words[1]
			self.m_instmem[self.inst_count+1] = words[2]
			self.m_datamem[self.inst_count] = words[0]
			self.m_datamem[self.inst_count+1] = words[3]
			self.inst_count += 2
			buff = vmdata.file.read(24)
	def instruction(self, address):
		return VmInstruction(self.m_instmem[address])
	def setInstruction(self, address, instruction):
		self.m_instmem[address] = instruction.data
	def data(self, address):
		return self.m_datamem[address]
	def setData(self, address, data):
		self.m_datamem[address] = data
	def input(self, address):
		return self.m_input[address]
	def setInput(self, address, value):
		self.m_input[address] = value
	def output(self, address):
		return self.m_output[address]
	def setOutput(self, address, value):
		self.m_output[address] = value
	def status(self):
		return self.m_status
	def setStatus(self, status):
		self.m_status = status

