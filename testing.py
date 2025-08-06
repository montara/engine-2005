import sys, os, random, time
import string
from math import *
from OpenGL.GL import *
from OpenGL.GLE import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import ode

# geometric utility functions
def scalp (vec, scal):
    vec[0] *= scal
    vec[1] *= scal
    vec[2] *= scal

def length (vec):
    return sqrt (vec[0]**2 + vec[1]**2 + vec[2]**2)

# prepare_GL
def prepare_GL():
    """Prepare drawing.
    """

    # Viewport
    glViewport(0,0,800,600)

    # Initialize
    glClearColor(0.8,0.8,0.9,0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glEnable(GL_LIGHTING)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_FLAT)

    # Textures
#    glActiveTextureARB(GL_TEXTURE0_ARB)
#    LoadTexture('bkg.bmp')
#    glEnable(GL_TEXTURE_2D)
    
    # Projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective (45,1.3333,0.2,20)

    # Initialize ModelView matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Light source
    glLightfv(GL_LIGHT0,GL_POSITION,[0,0,1,0])
    glLightfv(GL_LIGHT0,GL_DIFFUSE,[1,1,1,1])
    glLightfv(GL_LIGHT0,GL_SPECULAR,[1,1,1,1])
    glEnable(GL_LIGHT0)

    # View transformation
    gluLookAt (2.4, 2.6, 2.0, 0.6, 1.4, 0, 0, 1, 0)

def LoadTexture(name):
	#global texture
	image = open(name)
	
	ix = image.size[0]
	iy = image.size[1]
	image = image.tostring("raw", "RGBX", 0, -1)
	
	# Create Texture	
	id = glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D, id)   # 2d texture (x and y size)
	
	glPixelStorei(GL_UNPACK_ALIGNMENT,1)
	glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
	
	return id


def create_scene(world, space):
    
    global group_2
    global crankOutputJoint

        
    crankRodLobe = create_sphere(world, space, 400, 0.10)
    crankRodLobe.setPosition((0.5, 0.80, -0.5))

    piston = create_cylinder(world, space, 400, .125, .250, 2)
    piston.setPosition((0.5, 1.400, -0.5))
    
    rod = create_cylinder(world, space, 400, 0.04, 0.475, 2)
    rod.setPosition((0.5, 1.1125, -0.5))
    
    crankOutputJoint = ode.HingeJoint(world, group_2)
    crankOutputJoint.attach(ode.environment, crankRodLobe)
    crankOutputJoint.setAxis((0,0,1))
    crankOutputJoint.setAnchor((0.5,1.000, -0.5))
    crankOutputJoint.setParam(ode.ParamVel, 50)
    crankOutputJoint.setParam(ode.ParamFMax, 1000)

    crankRodJoint = ode.HingeJoint(world, group_2)
    crankRodJoint.attach(crankRodLobe, rod)
    crankRodJoint.setAxis((0,0,1))
    crankRodJoint.setAnchor((0.5,0.80, -0.5))
    

    pistonCrankJoint = ode.HingeJoint(world, group_2)
    pistonCrankJoint.attach(piston, rod)
    pistonCrankJoint.setAxis((0,0,1))
    pistonCrankJoint.setAnchor((0.5,1.325, -0.5))
    
    cylinderJoint = ode.SliderJoint(world, group_2)
    cylinderJoint.attach(ode.environment, piston)
    cylinderJoint.setAxis((0,1,0))
    #cylinderJoint.setParam(ode.ParamLoStop, -0.5)
    #cylinderJoint.setParam(ode.ParamHiStop, 1.0)

    
    bodies.append(crankRodLobe)
    #bodies.append(crankCenter)
    bodies.append(piston)
    bodies.append(rod)
    
# draw_floor
def draw_floor(floor):
    """Draw the textured floor"""
    
    x,y,z = floor.getPosition()
    R = floor.getRotation()
    rot = [R[0], R[3], R[6], 0.,
           R[1], R[4], R[7], 0.,
           R[2], R[5], R[8], 0.,
           x, y, z, 1.0]
    glPushMatrix()
    gl.MultMatrixd(rot)
    


# draw_body
def draw_body(body):
    """Draw an ODE body.
    """

    x,y,z = body.getPosition()
    R = body.getRotation()
    rot = [R[0], R[3], R[6], 0.,
           R[1], R[4], R[7], 0.,
           R[2], R[5], R[8], 0.,
           x, y, z, 1.0]
    glPushMatrix()
    glMultMatrixd(rot)
    
    if body.shape=="box":
        sx,sy,sz = body.boxsize
        glScale(sx, sy, sz)
        glutSolidCube(1)

    if body.shape=="sphere":
        radius = body.radius
        glutSolidSphere(radius, 20, 20)
        
    if body.shape=="cylinder":
	axis, radius, length = body.cylDimensions
	quad = gluNewQuadric()
        #glScale(radius, length, radius)
        #glutSolidCube(1)
	glTranslated(0, length/2.0, 0)
	glRotated(90, 1,0,0)
	gluCylinder(quad, radius, radius, length, 20, 20)
	
    glPopMatrix()


# create_box
def create_box(world, space, density, lx, ly, lz):
    """Create a box body and its corresponding geom."""

    # Create body
    body = ode.Body(world)
    M = ode.Mass()
    M.setBox(density, lx, ly, lz)
    body.setMass(M)

    # Set parameters for drawing the body
    body.shape = "box"
    body.boxsize = (lx, ly, lz)

    # Create a box geom for collision detection
    geom = ode.GeomBox(space, lengths=body.boxsize)
    geom.setBody(body)

    return body

#create_cylinder
def create_cylinder(world, space, density, radius, length, axis):

    # Create body
    body = ode.Body(world)
    M = ode.Mass()
    M.setCylinder(density, axis, radius, length)
    body.setMass(M)

    # Set parameters for drawing the body
    body.shape = "cylinder"
    body.cylDimensions = (axis, radius, length)

    # Create a box geom for collision detection
    geom = ode.GeomCCylinder(space, radius=radius, length=length)
    geom.setBody(body)

    return body

# create_sphere
def create_sphere(world, space, density, radius):
    """Create a Sphere body and it's corresponding geom."""
    
    # Create body
    body = ode.Body(world)
    M = ode.Mass()
    M.setSphere(density, radius)
    body.setMass(M)
    
    # Set parameters for drawing body
    body.shape = "sphere"
    body.radius = radius
    
    geom = ode.GeomSphere(space, radius)
    geom.setBody(body)
    
    return body

# Collision callback
def near_callback(args, geom1, geom2):
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



######################################################################

# Initialize Glut
glutInit ([])

# Open a window
glutInitDisplayMode (GLUT_RGB | GLUT_DOUBLE)

x = 0
y = 0
width = 800
height = 600
glutInitWindowPosition (x, y);
glutInitWindowSize (width, height);
glutCreateWindow ("testode")

# Create a world object
world = ode.World()
world.setGravity( (0,-9.81,0) )
world.setERP(0.8)
world.setCFM(1E-5)

# Create a space object
space = ode.Space()

# Create a plane geom which prevent the objects from falling forever
floor = ode.GeomPlane(space, (0,1,0), -0.5)

# A list with ODE bodies
bodies = []

crankOutputJoint = None

group_2 = ode.JointGroup()

create_scene(world, space)



# A joint group for the contact joints that are generated whenever
# two bodies collide
contactgroup = ode.JointGroup()


# Some variables used inside the simulation loop
fps = 50
dt = 0.5/fps
running = True
state = 0
counter = 0
objcount = 0
lasttime = time.time()


# keyboard callback
def _keyfunc (c, x, y):
    
    key = string.upper(c)
    if key == 'W':
	i = crankOutputJoint.getParam(ode.ParamVel)
	crankOutputJoint.setParam(ode.ParamVel, i+5)
	print str(crankOutputJoint.getParam(ode.ParamVel))
    elif key == 'S':
	i = crankOutputJoint.getParam(ode.ParamVel)
	crankOutputJoint.setParam(ode.ParamVel, i-5)
	print str(crankOutputJoint.getParam(ode.ParamVel))
    elif key == 'Q':
	sys.exit (0)

glutKeyboardFunc (_keyfunc)

# draw callback
def _drawfunc ():
    # Draw the scene
    prepare_GL()
    
    
    for b in bodies:
        draw_body(b)

    glutSwapBuffers ()

glutDisplayFunc (_drawfunc)

# idle callback
def _idlefunc ():
    global counter, state, lasttime

    t = dt - (time.time() - lasttime)

    if (t > 0):
        time.sleep(t)

    counter += 1
    #if counter == 100:
#	crankOutputJoint.setParam(ode.ParamVel, 7.5)
	#crankOutputJoint.setParam(ode.ParamFMax, 500)
#	counter = 1

#    elif counter >= 50:
#	crankOutputJoint.setParam(ode.ParamVel, -7.5)
	#crankOutputJoint.setParam(ode.ParamFMax, 500)
    

    glutPostRedisplay ()

    # Simulate
    n = 2

    for i in range(n):
        # Detect collisions and create contact joints
        space.collide((world,contactgroup), near_callback)

        # Simulation step
        world.step(dt/n)

        # Remove all contact joints
        contactgroup.empty()

    lasttime = time.time()

glutIdleFunc (_idlefunc)

glutMainLoop ()
