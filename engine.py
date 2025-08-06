import sys, os, random, time
import string
from math import *
from ogre import * 
#import ogre
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import ode
import OgreFramework

# my classes
import crankshaft, block, connecting_rod 

# Global engine object
engineObject = None

class EngineFrameListener(OgreFramework.FrameListener):
	def __init__(self, renderWindow, camera, sceneManager):
		OgreFramework.FrameListener.__init__(self,renderWindow,camera)
		
	def frameStarted(self, evt):
		#engineObject.loopfunc()
		#self.renderWindow.swapBuffers()
		return OgreFramework.FrameListener.frameStarted(self, evt)
	def frameEnded(self,evt):
		engineObject.loopfunc()
		return OgreFramework.FrameListener.frameEnded(self, evt)
	
	def _processUnbufferedKeyInput(self, frameEvent):
		global engineObject
		status = OgreFramework.FrameListener._processUnbufferedKeyInput(self, frameEvent)
		crankShaft = engineObject.crankShaft
		#self.Keyboard.capture()
		#self.Mouse.capture()
		if self.Keyboard.isKeyDown(OIS.KC_I):
			i = crankShaft.FrontMainJoint.getParam(ode.ParamVel)
			crankShaft.FrontMainJoint.setParam(ode.ParamVel, i+10)
			print "Velocity: " + str(crankShaft.FrontMainJoint.getParam(ode.ParamVel))
		if self.Keyboard.isKeyDown(OIS.KC_K):
			i = crankShaft.FrontMainJoint.getParam(ode.ParamVel)
			crankShaft.FrontMainJoint.setParam(ode.ParamVel, i-10)
			print "Velocity: " + str(crankShaft.FrontMainJoint.getParam(ode.ParamVel))
		if self.Keyboard.isKeyDown(OIS.KC_J):
			i = crankShaft.FrontMainJoint.getParam(ode.ParamFMax)
			crankShaft.FrontMainJoint.setParam(ode.ParamFMax, i-100)
			print "Torque: " + str(crankShaft.FrontMainJoint.getParam(ode.ParamFMax))
		if self.Keyboard.isKeyDown(OIS.KC_L):
			i = crankShaft.FrontMainJoint.getParam(ode.ParamFMax)
			crankShaft.FrontMainJoint.setParam(ode.ParamFMax, i+100)
			print "Torque: " + str(crankShaft.FrontMainJoint.getParam(ode.ParamFMax))			
			
		return status


class Engine(OgreFramework.Application):
	def _createScene(self):

		self.bodyCounter = 0
		
		sceneManager = self.sceneManager
		sceneManager.setAmbientLight(ogre.ColourValue(1.0,1.0,1.0))
		#sceneManager.setWorldGeometry("terrain.cfg")
		#sceneManager.setSkyDome(True, "CloudySky", 5, 8)
		# Initialize Ogre

		# Open a window

		# my starting coordinates
		x = 500
		y = 40
		z = 500
		width = 1024
		height = 768
		# Create a world object
		self.world = ode.World()
		world = self.world
		# Set the world parameters
		world.setGravity( (0,-9.81,0) )
		#world.setGravity( (0,0,0) )
		world.setERP(0.8)
		world.setCFM(1E-5)
		# Create a space object
		self.space = ode.Space()
		space = self.space
		# A list with ODE bodies
		self.bodies = []
		self.nodes = []

		# Add our table
		self.draw_table(x,y,z)
		# Create a plane geom which prevent the objects from falling forever
		#floor = ode.GeomPlane(space, (0,1,0), -1.0)
		

		# Define the idle combustion force
		combustionForce = -50.0
		
		# A joint group for the contact joints that are generated whenever
		# two bodies collide
		self.contactgroup = ode.JointGroup()
		
		# ODE joint group
		self.group_2 = ode.JointGroup()
		
		# Initialize the engine components
		self.engineBlock = block.engineBlock()
		engineBlock = self.engineBlock
		self.crankShaft = crankshaft.crankshaft()
		crankShaft = self.crankShaft
		
		
		# Set the engine component attributes
		crankShaft.density = 5
		crankShaft.numRodJournals = 6  # 2 cylinder
		engineBlock.Vangle = 180
		engineBlock.isRadial = False
		engineBlock.numCylBanks = 2
		engineBlock.numCylinders =12
		
		# Examples for other engines
		#crankShaft.numRodJournals = 2  # 4 cylinder
		#engineBlock.numCylinders = 4
		#crankShaft.numRodJournals = 3  # 6 cylinder
		#engineBlock.numCylinders = 6
		#crankShaft.numRodJournals = 4  # 8 cylinder
		#engineBlock.numCylinders = 8
		#crankShaft.numRodJournals = 5  # 10 cylinder
		#engineBlock.numCylinders = 10
		#crankShaft.numRodJournals = 6  # 12 cylinder
		#engineBlock.numCylinders = 12
		
		# Initialize connecting rods, must be done after other engine components
		self.connectingRods = connecting_rod.connectingRod()  
		connectingRods = self.connectingRods
		
		# Add special connecting rod parameters here.
		
		# Initialize the cylinder banks in the block. This is used for reference
		engineBlock._init_banks(crankShaft, connectingRods, x,y,z)
		
		# add the ode.Body objects to the global array. The pistons are automatically
		# added with connecting rods for now.
		self.bodies += crankShaft.createBodies(world,space, x,y,z,200, engineBlock)
		self.bodies += connectingRods.createBodies(engineBlock,crankShaft,
			world,
			space,
			x,y,z,
			50)
		
		
		
		# Some variables used inside the simulation loop
		self.fps = 100
		self.dt = 0.75/self.fps
		self.running = True
		state = 0
		self.counter = 0
		objcount = 0
		self.lasttime = time.time()
		
		for body in self.bodies:
			self.draw_body(body)
		

	#def _createCamera(self):
	#	pass
		#self.camera = self.sceneManager.createCamera("PlayerCam")
		#self.camera.nearClipDistance = 5

	def _createFrameListener(self):
		#pass
		self.frameListener = EngineFrameListener(self.renderWindow, self.camera, self.sceneManager)
		self.root.addFrameListener(self.frameListener)
		self.frameListener.showDebugOverlay(True)




	def loopfunc (self):
		#global counter, state, lasttime
	
		t = self.dt - (time.time() - self.lasttime)
	
		if (t > 0):
			time.sleep(t)
		# Simulate
		n = 1
		for i in range(n):
			# Detect collisions and create contact joints
			self.space.collide((self.world,self.contactgroup), self.near_callback)
			# Simulation step
			self.world.step(self.dt/n)
			# Remove all contact joints
			self.contactgroup.empty()
		self.lasttime = time.time()
		n = 0
		# Update the body positions
		for b in self.bodies:
			posVector = ogre.Vector3(b.getPosition())
			(w,x,y,z) = b.getQuaternion()
			orientation = ogre.Quaternion(w,x,y,z)
			orientation.normalise()
			node = self.nodes[n]
			
			node.orientation = orientation
			node.position = posVector
			n += 1
			
	# Draw table
	def draw_table(engine, x,y,z):
		sceneManager = engine.sceneManager
		ent = sceneManager.createEntity("Table", "Table.mesh")
		node = sceneManager.rootSceneNode.createChildSceneNode("TableNode",
			 ogre.Vector3((x,y-20,z+8)),
			 )
		node.yaw(ogre.Degree(-90))
		
		node.attachObject(ent)
		#engine.nodes.append(node)

	# draw_body
	def draw_body(engine, body):
		"""Draw an ODE body.
		"""
		sceneManager = engine.sceneManager
		(x,y,z) = body.getPosition()
	
		(qw,qx,qy,qz) = body.getQuaternion()
		quart = ogre.Quaternion(qw,qx,qy,qz)
		quart.normalise()
		if body.shape=="box":
			sx,sy,sz = body.boxsize
			
		if body.shape=="sphere":
			radius = body.radius
			
		if body.shape=="cylinder":
			axis, radius, length = body.cylDimensions
			if body.mesh == "piston":
				ent = sceneManager.createEntity("ODEEntity"
				+str(engine.bodyCounter),
				"Piston.mesh")
			else:
				ent = sceneManager.createEntity("ODEEntity"
				+str(engine.bodyCounter),
				"Cylinder.mesh")
			#ent.setMaterialName('Grey')
			node = sceneManager.rootSceneNode.createChildSceneNode("ODENode"
				+str(engine.bodyCounter), 
				ogre.Vector3(body.getPosition())
				)
			node.scale = radius,length/2,radius
			node.orientation = quart
			node.attachObject(ent)
			engine.nodes.append(node)
		engine.bodyCounter += 1
	
	# Collision callback
	def near_callback(self, args, geom1, geom2):
		"""Callback function for the collide() method.
	
		This function checks if the given geoms do collide and
		creates contact joints if they do.
		"""
	
		# Check if the objects do collide
		contacts = ode.collide(geom1, geom2)
	
		# Create contact joints
		world,contactgroup = args
		for c in contacts:
			c.setBounce(0.1)
			c.setMu(500)
			j = ode.ContactJoint(world, contactgroup, c)
			j.attach(geom1.getBody(), geom2.getBody())


if __name__ ==  '__main__':
	engineObject = Engine()
	engineObject.go()


######################################################################



