import cube_surface
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time

times = 0
rotate_x = 45
rotate_y = 45

surfase_internalList = []
surfaseList = []

default_color = ((0, 0, 1), (0, 1, 0), (1, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 1))
def Draw():
    glEnable(GL_DEPTH_TEST)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glDepthFunc(GL_LEQUAL)

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity()
    gluPerspective(45.0, 1.0, 0.5, 200.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    #gluLookAt(0, 0, -101, 0, 0, 0, 0, 1, 0)

    glTranslate(0.0, 0.0, -1.5)
    global rotate_x, rotate_y

    glRotatef(rotate_x, 1.0, 0.0, 0.0)
    glRotatef(rotate_y, 0.0, 1.0, 0.0)
    #glRotatef(45.0, 0.0, 0.0, 1.0)
    global surfaseList, surfase_internalList
    for surfase in surfaseList:
        colorMod = 0.6
        if (surfase.m_isSelected == True):
            colorMod = 1
        glColor3f(default_color[surfase.m_surfase_index][0] * colorMod, default_color[surfase.m_surfase_index][1] * colorMod, default_color[surfase.m_surfase_index][2] * colorMod)
        glBegin(GL_POLYGON)
        for point in surfase.m_pointlist:
            glVertex3f(point.x, point.y, point.z)
        glEnd()	
    glColor3f(0, 0, 0)
    for surfase_internal in surfase_internalList:
        glBegin(GL_POLYGON)
        for point in surfase_internal.m_pointlist:
            glVertex3f(point.x, point.y, point.z)
        glEnd()
    glFlush()


"""
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1.0,1.0,0.0,0.2)
    surfase = cube_surface.Cube_Surfase(0, 0.102, [0, 0], 3)
    glBegin(GL_POLYGON)
    for point in surfase.m_pointlist:
        glVertex3f(point.x, point.y, point.z)
    glEnd()
    glDisable(GL_BLEND)
"""


def init_cube():
    print "init_cube"
    global surfaseList, surfase_internalList
    for surfase_index in range(6):
        surfase_internal = cube_surface.Cube_Surfase(surfase_index, 0.298, [0, 0], 1)
        surfase_internalList.append(surfase_internal)
        for i in range(3):
            for j in range(3):
                surfase = cube_surface.Cube_Surfase(surfase_index, 0.1, [i - 1, j - 1], 3)
                surfaseList.append(surfase)
 
def PointinTriangle(A, B, C, P):
    v0 = B.minus(A)
    v1 = C.minus(A)
    v2 = P.minus(A)

    dot00 = v0.multiply(v0) 
    dot01 = v0.multiply(v1) 
    dot02 = v0.multiply(v2) 
    dot11 = v1.multiply(v1) 
    dot12 = v1.multiply(v2)
			
    inverDeno = 1.0 / (dot00 * dot11 - dot01 * dot01)
    u = (dot11 * dot02 - dot01 * dot12) * inverDeno
    if ((u < 0) or (u > 1)):
        return False
    v = (dot00 * dot12 - dot01 * dot02) * inverDeno
    if ((v < 0) or (v > 1)):
        return False
    return u + v <= 1

def SpecialKey(key,x,y):
    global rotate_x, rotate_y
    if (key==GLUT_KEY_RIGHT):
        for i in range(10):
            rotate_y = (rotate_y + 9) % 360
            Draw()
            time.sleep(0.1)
    if (key==GLUT_KEY_LEFT):
        for i in range(10):
            rotate_y = (rotate_y - 9) % 360
            Draw()
            time.sleep(0.1)
    if (key==GLUT_KEY_UP):
        for i in range(10):
            rotate_x = (rotate_x - 9) % 360
            Draw()
            time.sleep(0.1)
    if (key==GLUT_KEY_DOWN):
        for i in range(10):
            rotate_x = (rotate_x + 9) % 360
            Draw()
            time.sleep(0.1)
def MousePoint(button, state, x, y):
    global surfaseList
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    viewport = glGetIntegerv(GL_VIEWPORT)
    P = cube_surface.Point(x, y, 0)
			
    if(state==GLUT_DOWN):
        print("mouse click x=%d,y=%d", x, y)
        selectSurfase = 0
        old_Sum_y = 0
        for surfase in surfaseList:
            winpos = []
            sum_y = 0
            for point in surfase.m_pointlist:
                pos = gluProject(point.x,point.y,point.z,modelview,projection,viewport)
                winpos.append(cube_surface.Point(pos[0], viewport[3] - pos[1], 0))
                sum_y = sum_y + pos[2]
            if(PointinTriangle(winpos[0], winpos[1], winpos[2], P) or PointinTriangle(winpos[0], winpos[2], winpos[3], P)):
                if (selectSurfase == 0) :
                    selectSurfase = surfase
                    old_Sum_y = sum_y
                elif (sum_y < old_Sum_y):
                    selectSurfase = surfase
                    old_Sum_y = sum_y
                    print("changge m_isSelected surfase=%d", surfase.m_surfase_index)
        selectSurfase.m_isSelected = True
        Draw()


init_cube()
glutInit()
glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(400, 400)
glutCreateWindow("test")
glutDisplayFunc(Draw)
glutSpecialFunc(SpecialKey)
glutMouseFunc(MousePoint)
glutMainLoop()

