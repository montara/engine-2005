import sys
import ode
from utility import *


class crankshaft:
	"""Crankshaft class
		The crank is the center of the motor, and all other bottom end points
		are in relation to it. The first lobe is centered at 0 degrees
	"""
	def __init__(self):
		#self.length = 8        # Z axis length
		self.stroke = 2.5       # rotating point diameter  
		self.density = 8
		self.numRodJournals = 1     
		self.RodJournalWidth = 1.5
		self.MainJournalWidth = 1.0
		self.MainJournalDiameter = 1.7
		self.RodJournalDiameter = 1.50
		self.RodMainJournalDistance = 1.0
		self.crankOutputShaftDiameter = 0.75
		self.crankOutputShaftLength = 2.0
		self.shearTorque = 50000
		self.startingTorque = 1000
		self.joints = []
		self.RodJournalPositions = []
		self.MainJournalPositions = []
		self.jointGroup = ode.JointGroup()
		self.MainJoints = []
		self.RodJoints = []

	def getCylPerBank(self,block):
		CylPerBank = block.numCylinders/self.numRodJournals
		return CylPerBank

	def createBodies(self, world, space, x, y, z, density, block):
		"""Returns an array of bodies representing the Crankshaft
		"""
		
		bodies = []
		
		# The first body to build is the front shaft.		
		position = (x, y, z-(self.crankOutputShaftLength/2))
		rotation = rot(1,radians(90)) # Rotate it 90
		body = create_cylinder(world, 
									  space, 
									  self.density,
									  self.crankOutputShaftDiameter/2,
									  self.crankOutputShaftLength,
									  rotation,
									  position)
		self.FrontMainJoint = ode.HingeJoint(world,self.jointGroup)
		self.FrontMainJoint.attach(body,ode.environment)
		self.FrontMainJoint.setAnchor(body.getPosition())
		self.FrontMainJoint.setAxis((0,0,1))
		self.FrontMainJoint.setParam(ode.ParamVel, 10)
		self.FrontMainJoint.setParam(ode.ParamFMax, 1000) #self.startingTorque)
		
		#
		# Now generate the front main joint
		#
		
		position = (x, y, z+(self.MainJournalWidth/2) )
		rotation = rot(1,radians(90)) # Rotate it 90
		
		#main.setRotation(rotation)
		main = create_cylinder(world, 
									  space, 
									  self.density,
									  self.MainJournalDiameter/2,
									  self.MainJournalWidth,
									  rotation,
									  position)
		
		joint = ode.HingeJoint(world,self.jointGroup)
		joint.attach(body,main)
		joint.setAnchor((x,y,z))
		joint.setAxis((0,0,1))
		joint.setParam(ode.ParamVel, 0)
		joint.setParam(ode.ParamFMax,self.shearTorque)
		self.MainJoints.append(self.FrontMainJoint)
		bodies.append(body)
		bodies.append(main)
		
		#
		# Now create the rod lobes
		#
		
		i = 0
		# For each rod journal..
		self.angles = []
		if self.numRodJournals == 1:
			self.angles = [radians(0)]
		elif self.numRodJournals == 2:
			self.angles = [radians(0),radians(180)]
		elif self.numRodJournals == 3:
			self.angles = [radians(0),radians(240),radians(120)]
		elif self.numRodJournals == 4:
			self.angles = [radians(0),radians(90),radians(270),radians(180)]
		elif self.numRodJournals == 5:
			self.angles = [radians(0),radians(144),radians(288),radians(72),radians(216)]
		elif self.numRodJournals == 6:
			self.angles = [radians(0),radians(60),radians(240),radians(120),radians(300),radians(180)]
		else:
			print "Not yet supported"
			sys.exit(0)
			
		while i < self.numRodJournals:
			#
			# Build each rod journal body, create its joints, 
			# create its collision space, and.. stuff
			#
			# Find the location
			angleFromTDC = self.angles[i]
			# Set the center coordinates
			myZ = z+(self.RodJournalWidth/2)+(self.RodMainJournalDistance*(i+1))+(self.MainJournalWidth*(i+1))+(self.RodJournalWidth*i)+self.RodMainJournalDistance/2
			position = rotArbAxis((x,y+self.stroke/2,myZ), angleFromTDC, (x,y,z), (x,y,z+1))
			body = create_cylinder(world,
										  space, 
										  self.density, 
										  self.RodJournalDiameter/2, 
										  self.RodJournalWidth, 
										  rotation, 
										  position)
			#Adjust the center of mass to fudge balancing
			body.getMass().setZero() #(cgx=0,cgy=0,cgz=myZ)
			
			#record  the starting coordinates
			self.RodJournalPositions.append(position)
			# Add the joint from crank to rod
			joint = ode.HingeJoint(world, self.jointGroup)
			joint.attach(body,bodies[len(bodies)-1])
			joint.setAxis((0,0,1))
			joint.setAnchor(body.getPosition())
			joint.setParam(ode.ParamVel,0)
			joint.setParam(ode.ParamFMax,self.shearTorque)
			self.RodJoints.append(joint)
			bodies.append(body)
			
			# Create the next main bearing along the Z axis
			#
			#
			myZ = z+(self.MainJournalWidth/2)+(self.RodMainJournalDistance*(i+2))+(self.MainJournalWidth*(i+1))+(self.RodJournalWidth*(i+1))
			position = (x,y,myZ)
			body = create_cylinder(world, 
										  space, 
										  self.density, 
										  self.MainJournalDiameter/2, 
										  self.MainJournalWidth, 
										  rotation, 
										  position)	
			# Create the joints
			joint = ode.HingeJoint(world, self.jointGroup)
			joint.attach(body, ode.environment)
			joint.setAxis((0,0,1))
			joint.setAnchor((x,y,myZ))
			joint.setParam(ode.ParamVel,0)
			joint.setParam(ode.ParamFMax,0)
			joint2 = ode.HingeJoint(world, self.jointGroup)
			joint2.attach(body, bodies[len(bodies)-1])
			joint2.setAxis((0,0,1))
			joint2.setAnchor(bodies[len(bodies)-1].getPosition())
			joint2.setParam(ode.ParamVel,0)
			joint2.setParam(ode.ParamFMax,self.shearTorque)
			
			self.MainJoints.append(joint)
			bodies.append(body)
			i += 1
				
			
		return bodies
	