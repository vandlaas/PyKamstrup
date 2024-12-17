#!/usr/local/bin/python
#
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <phk@FreeBSD.ORG> wrote this file.  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.   Poul-Henning Kamp
# ----------------------------------------------------------------------------
#

from __future__ import print_function

# You need pySerial 
import serial

import math

#######################################################################
# These are the variables I have managed to identify
# Submissions welcome.

kamstrup_382_var = {

	0x0001: "Energy in",
	0x0002: "Energy out",

	0x000d: "Energy in hi-res",
	0x000e: "Energy out hi-res",

	0x041e: "Voltage p1",
	0x041f: "Voltage p2",
	0x0420: "Voltage p3",

	0x0434: "Current p1",
	0x0435: "Current p2",
	0x0436: "Current p3",

	0x0438: "Power p1",
	0x0439: "Power p2",
	0x043a: "Power p3",

	0x0056: "Current flow temperature",
	0x0057: "Current return flow temperature",
	0x0058: "Current temperature T3",
	0x007A: "Current temperature T4",
	0x0059: "Current temperature difference",
	0x005B: "Pressure in flow",
	0x005C: "Pressure in return flow",
	0x004A: "Current flow in flow",
	0x004B: "Current flow in return flow"
	0x03ff: "Power In",
	0x0438: "Power p1 In",
	0x0439: "Power p2 In",
	0x043a: "Power p3 In",

	0x0400: "Power In",
	0x0540: "Power p1 Out",
	0x0541: "Power p2 Out",
	0x0542: "Power p3 Out",
}

kamstrup_681_var = {
	1:	"Date",
	60:	"Heat",
	61:	"x",
	62:	"x",
	63:	"x",
	95:	"x",
	96:	"x",
	97:	"x",
}
# Values from "Multical 601 TECHNICAL DESCRIPTION 5512-301 GB/10.2008/Rev. H1"  page 86.
# YET TO BE VERIYFIED
kamstrup_MC601_var = {
	0x003C: "Energy register 1: Heat energy (E1)",
	0x005E: "Energy register 2: Control energy (E2)",
	0x003F: "Energy register 3: Cooling energy (E3)",
	0x003D: "Energy register 4: Flow energy (E4)",
	0x003E: "Energy register 5: Return flow energy (E5)",
	0x005F: "Energy register 6: Tap water energy (E6)",
	0x0060: "Energy register 7: Heat energy Y (E7)",
	0x0061: "Energy register 8: [m3 * T1] (E8)",
	0x006E: "Energy register 9: [m3 * T2] (E9)",
	0x0040: "Tariff register 2 (TA2)",
	0x0041: "Tariff register 3 (TA3)",
	0x0044: "Volume register V1 (V1)",
	0x0045: "Volume register V2 (V2)",
	0x0054: "Input register VA (VA)",
	0x0055: "Input register VB (VB)",
	0x0048: "Mass register V1 (M1)",
	0x0049: "Mass register V2 (M2)",
	0x03EC: "Operational hourcounter (HR)",
	0x0071: "Info-event counter (INFOEVENT)",
	0x03EA: "Current time (hhmmss) (CLOCK)",
	0x0063: "Infocode register, current (INFO)",
	0x0056: "Current flow temperature (T1)",
	0x0057: "Current return flow temperature (T2)",
	0x0058: "Current temperature T3 (T3)",
	0x007A: "Currenttemperature T4 (T4)",
	0x0059: "Current temperature difference (T1-T2)",
	0x005B: "Pressure in flow (P1)",
	0x005C: "Pressure in return flow (P2)",
	0x004A: "Current flow in flow (FLOW1)",
	0x004B: "Current flow in return flow (FLOW2)",
	0x0050: "Current power calculated on the basis of V1-T1-T2 (EFFEKT1)",
	0x007B: "Date for max. This year (MAX FLOW1DATE/ÅR)",
	0x007C: "Max. value this year (MAX FLOW1/ÅR)",
	0x007D: "Date for min. this year (MIN FLOW1DATE/ÅR)",
	0x007E: "Min. value this year (MIN FLOW1/ÅR)",
	0x007F: "Date for max. this year (MAX EFFEKT1DATE/ÅR)",
	0x0080: "Max. value this year (MAX EFFEKT1/ÅR)",
	0x0081: "Date for min. this myear (MIN EFFEKT1DATE/ÅR)",
	0x0082: "Min. value this year (MIN EFFEKT1/ÅR)",
	0x008A: "Date for max. this year (MAX FLOW1DATE/MÅNED)",
	0x008B: "Max. value this year (MAX FLOW1/MÅNED)",
	0x008C: "Date for min. this month (MIN FLOW1DATE/MÅNED)",
	0x008D: "Min. value this month (MIN FLOW1/MÅNED)",
	0x008E: "Date for max. this month (MAX EFFEKT1DATE/MÅNED)",
	0x008F: "Max. value this month (MAX EFFEKT1/MÅNED)",
	0x0090: "Date for min. this month (MIN EFFEKT1DATE/MÅNED)",
	0x0091: "Min. value this month (MIN EFFEKT1/MÅNED)",
	0x0092: "Year-to-date average for T1 (AVR T1/ÅR)",
	0x0093: "Year-to-date average for T2 (AVR T2/ÅR)",
	0x0095: "Month-to-date average for T1 (AVR T1/MÅNED)",
	0x0096: "Month-to-date average for T2 (AVR T2/MÅNED)",
	0x0042: "Tariff limit 2 (TL2)",
	0x0043: "Tariff limit 3 (TL3)",
	0x0062: "date (reading date) (XDAY)",
	0x0098: "Program no. ABCCCCCC (PROG NO)",
	0x0099: "1 Config no. DDDEE (CONFIG NO)",
	0x00A8: "2 Config. no. FFGGMN (CONFIG NO)",
	0x03E9: "Serial no. (unique number for each meter) (SERIE NO)",
	0x0070: "2 Customer number (8 most important digits) (METER NO)",
	0x03F2: "1 Customer number (8 less important digits) (METER NO)",
	0x0072: "VA Meter no. for VA (METER NO)",
	0x0068: "VB Meter no. for VB (METER NO)",
	0x03ED: "Software edition (METER TYPE)",
	0x009A: "1 Software check sum (CHECK SUM)",
	0x009B: "High-resolution energy register for testing purposes  (HIGH RES)",
	0x009D: "ID number for top module (TOPMODUL ID)",
	0x009E: "ID number for base module (BOTMODUL ID)"
}


#######################################################################
# Units, provided by Erik Jensen

units = {
	0: '', 1: 'Wh', 2: 'kWh', 3: 'MWh', 4: 'GWh', 5: 'j', 6: 'kj', 7: 'Mj',
	8: 'Gj', 9: 'Cal', 10: 'kCal', 11: 'Mcal', 12: 'Gcal', 13: 'varh',
	14: 'kvarh', 15: 'Mvarh', 16: 'Gvarh', 17: 'VAh', 18: 'kVAh',
	19: 'MVAh', 20: 'GVAh', 21: 'kW', 22: 'kW', 23: 'MW', 24: 'GW',
	25: 'kvar', 26: 'kvar', 27: 'Mvar', 28: 'Gvar', 29: 'VA', 30: 'kVA',
	31: 'MVA', 32: 'GVA', 33: 'V', 34: 'A', 35: 'kV',36: 'kA', 37: 'C',
	38: 'K', 39: 'l', 40: 'm3', 41: 'l/h', 42: 'm3/h', 43: 'm3xC',
	44: 'ton', 45: 'ton/h', 46: 'h', 47: 'hh:mm:ss', 48: 'yy:mm:dd',
	49: 'yyyy:mm:dd', 50: 'mm:dd', 51: '', 52: 'bar', 53: 'RTC',
	54: 'ASCII', 55: 'm3 x 10', 56: 'ton x 10', 57: 'GJ x 10',
	58: 'minutes', 59: 'Bitfield', 60: 's', 61: 'ms', 62: 'days',
	63: 'RTC-Q', 64: 'Datetime'
}

#######################################################################
# Kamstrup uses the "true" CCITT CRC-16
#

def crc_1021(message):
        poly = 0x1021
        reg = 0x0000
        for byte in message:
                mask = 0x80
                while(mask > 0):
                        reg<<=1
                        if byte & mask:
                                reg |= 1
                        mask>>=1
                        if reg & 0x10000:
                                reg &= 0xffff
                                reg ^= poly
        return reg

#######################################################################
# Byte values which must be escaped before transmission
#

escapes = {
	0x06: True,
	0x0d: True,
	0x1b: True,
	0x40: True,
	0x80: True,
}

#######################################################################
# And here we go....
#
class kamstrup(object):

	def __init__(self, serial_port = "/dev/cuaU0"):
		self.debug_fd = open("/tmp/_kamstrup", "a")
		self.debug_fd.write("\n\nStart\n")
		self.debug_id = None

		self.ser = serial.Serial(
		    port = serial_port,
		    baudrate = 1200,
		    timeout = 1.0)

	def debug(self, dir, b):
		for i in b:
			if dir != self.debug_id:
				if self.debug_id != None:
					self.debug_fd.write("\n")
				self.debug_fd.write(dir + "\t")
				self.debug_id = dir
			self.debug_fd.write(" %02x " % i)
		self.debug_fd.flush()

	def debug_msg(self, msg):
		if self.debug_id != None:
			self.debug_fd.write("\n")
		self.debug_id = "Msg"
		self.debug_fd.write("Msg\t" + msg)
		self.debug_fd.flush()

	def wr(self, b):
		b = bytearray(b)
		self.debug("Wr", b);
		self.ser.write(b)

	def rd(self):
		a = self.ser.read(1)
		if len(a) == 0:
			self.debug_msg("Rx Timeout")
			return None
		b = bytearray(a)[0]
		self.debug("Rd", bytearray((b,)));
		return b

	def send(self, pfx, msg):
		b = bytearray(msg)

		b.append(0)
		b.append(0)
		c = crc_1021(b)
		b[-2] = c >> 8
		b[-1] = c & 0xff

		c = bytearray()
		c.append(pfx)
		for i in b:
			if i in escapes:
				c.append(0x1b)
				c.append(i ^ 0xff)
			else:
				c.append(i)
		c.append(0x0d)
		self.wr(c)

	def recv(self):
		b = bytearray()
		while True:
			d = self.rd()
			if d == None:
				return None
			if d == 0x40:
				b = bytearray()
			b.append(d)
			if d == 0x0d:
				break
		c = bytearray()
		i = 1;
		while i < len(b) - 1:
			if b[i] == 0x1b:
				v = b[i + 1] ^ 0xff
				if v not in escapes:
					self.debug_msg(
					    "Missing Escape %02x" % v)
				c.append(v)
				i += 2
			else:
				c.append(b[i])
				i += 1
		if crc_1021(c):
			self.debug_msg("CRC error")
		return c[:-2]

	def readvar(self, nbr):
		# I wouldn't be surprised if you can ask for more than
		# one variable at the time, given that the length is
		# encoded in the response.  Havn't tried.

		self.send(0x80, (0x3f, 0x10, 0x01, nbr >> 8, nbr & 0xff))

		b = self.recv()
		if b == None:
			return (None, None)

		if b[0] != 0x3f or b[1] != 0x10:
			return (None, None)

		if b[2] != nbr >> 8 or b[3] != nbr & 0xff:
			return (None, None)

		if b[4] in units:
			u = units[b[4]]
		else:
			u = None

		# Decode the mantissa
		x = 0
		for i in range(0,b[5]):
			x <<= 8
			x |= b[i + 7]

		# Decode the exponent
		i = b[6] & 0x3f
		if b[6] & 0x40:
			i = -i
		i = math.pow(10,i)
		if b[6] & 0x80:
			i = -i
		x *= i

		if False:
			# Debug print
			s = ""
			for i in b[:4]:
				s += " %02x" % i
			s += " |"
			for i in b[4:7]:
				s += " %02x" % i
			s += " |"
			for i in b[7:]:
				s += " %02x" % i

			print(s, "=", x, units[b[4]])

		return (x, u)
			

if __name__ == "__main__":

	import time

	foo = kamstrup()

	for i in kamstrup_382_var:
		x,u = foo.readvar(i)
		print("%-25s" % kamstrup_382_var[i], x, u)
