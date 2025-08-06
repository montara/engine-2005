import sys
import ode
from utility import *

class piston:
	"""
	"""
	def __init__(self):
		self.bore = 2.1
		self.height = self.bore
		self.density = 5
		self.rodHeight = self.bore
		self.jointGroup = ode.JointGroup()
		
	def createBody(self, world, space, block, crank,rod,x,y,z, bankAngle, rodBody):
		# Create a piston
		position = (x, y, z)
		
		rotation = rot(3,0-bankAngle)
		piston = create_cylinder(world,
			space,
			self.density,
			self.bore/2,
			self.height,
			rotation,
			position)
		pistonRodJoint = ode.HingeJoint(world, rod.jointGroup)
		pistonRodJoint.attach(piston, rodBody)
		pistonRodJoint.setAxis((0,0,1))
		pistonRodJoint.setAnchor(piston.getRelPointPos((0,0-self.rodHeight,0)))
		
		piston.mesh = "piston"
		#pistonRodJoint.setAnchor(position)
		
		cylinderJoint = ode.SliderJoint(world, rod.jointGroup)
		cylinderJoint.attach(ode.environment, piston)
		cylinderJoint.setAxis(rotArbPoint(0,1,0,0,0,0,bankAngle, 3))
		
		return piston
