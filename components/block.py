import sys
from utility import *

class engineBlock:
	"""Engine Block class
	Given a set of parameters,
	calculate the engine block geometry
	"""
	def __init__(self):
		# Set some defaults
		self.isRadial = False
		self.Vangle = 90
		self.numCylBanks = 2
		self.numCylinders = 2
		self.deckHeightfromCrankCenter = 8.0
		self.cylinderBankAngles = []
		self.cylinderBanks = []
		self.bankCoordinates = []
		self.cylBankOrder = {}
		#self._init_banks()


	def _init_banks(self, crank, rods, x,y,z):
		# set and check the number of cylinders per bank
		self.cylPerBank = self.numCylinders/self.numCylBanks
		
		if self.cylPerBank < 1:
			sys.exit(1)
		
		if self.Vangle != 0:
			self.maxBankPerRad = 360/self.Vangle #4
		else:
			self.maxBankPerRad = 360
		
		if self.numCylBanks > self.maxBankPerRad:
			sys.exit(1)
		
		if self.numCylBanks == 1 or self.isRadial == True:
			self.startAngle = self.Vangle
		else:
			self.startAngle = self.Vangle/2

		i = 0
		
		# for each cylinder bank...
		while i < self.numCylBanks:
			# get the angle for the current bank
			bankAngle = None
			if i == 0:
				bankAngle = 0-self.startAngle
			else:
				bankAngle = (self.Vangle*i)-self.startAngle
			self.cylinderBankAngles.append(bankAngle)
			i += 1
			
		# Assign Cylinders to banks
		i = 0
		j = 0
		while i < self.numCylinders:
			self.cylinderBanks.append(j)
			j += 1
			if j == self.numCylBanks:
				j = 0
			i += 1
		
		cylPerBank = self.numCylinders/self.numCylBanks
		
		i = 0
		bankOrder = {}
		while i < self.numCylinders:
				bank = self.cylinderBanks[i]
				if bankOrder.has_key(bank):
					bankOrder[bank] += 1
				else:
					bankOrder[bank] = 0
				self.cylBankOrder[i] = (bank, bankOrder[bank])
				
				newY = y+((crank.stroke/2)+rods.length)+(crank.RodJournalDiameter/2)
				self.bankCoordinates.append(rotArbPoint(x,newY,z,x,y,z, radians(self.cylinderBankAngles[self.cylinderBanks[i]]), 3))
				i += 1
	
