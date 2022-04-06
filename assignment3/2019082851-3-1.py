from tkinter import CURRENT
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gCamAng = 0.
gCamHeight = 1.

th = np.pi/18
T_10 = np.array([[np.cos(th), -np.sin(th),0.0], [np.sin(th), np.cos(th),0.0],[0.0,0.0,1.0]])
Q = np.array([1,0,-0.1,0,1,0,0,0,1])
Q= np.reshape(Q,(3,3)).astype(np.float)
E = np.array([1,0,0.1,0,1,0,0,0,1])
E = np.reshape(E,(3,3)).astype(np.float)
W = np.array([0.9,0,0,0,0.9,0,0,0,1])
W = np.reshape(W,(3,3)).astype(np.float)

global_matrix = np.identity(3)



# draw a cube of side 1, centered at the origin.
def drawUnitCube():
    glBegin(GL_QUADS)
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f( 0.5, 0.5, 0.5) 
                             
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f( 0.5,-0.5,-0.5) 
                             
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
                             
    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5,-0.5)
 
    glVertex3f(-0.5, 0.5, 0.5) 
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5) 
    glVertex3f(-0.5,-0.5, 0.5) 
                             
    glVertex3f( 0.5, 0.5,-0.5) 
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    glEnd()

def drawCubeArray():
    for i in range(5):
        for j in range(5):
            for k in range(5):
                glPushMatrix()
                glTranslatef(i,j,-k-1)
                glScalef(.5,.5,.5)
                drawUnitCube()
                glPopMatrix()

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()
def render():
    global gCamAng, gCamHeight
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    
    # draw polygons only with boundary edges
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )


    glMatrixMode(GL_PROJECTION)    
    glLoadIdentity()
    # test other parameter values
    # near plane: 10 units behind the camera
    # far plane: 10 units in front of the camera
    glOrtho(-5,5, -5,5, -10,10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(1*np.sin(gCamAng),gCamHeight,1*np.cos(gCamAng), 0,0,0, 0,1,0)

    drawFrame()
    glColor3ub(255, 255, 255)

    drawUnitCube()

    # test 
    # drawCubeArray()

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )
    glEnd()





def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight
    global global_matrix
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_Q:
            global_matrix = Q @ global_matrix
        elif key==glfw.KEY_E:
            global_matrix = E @ global_matrix
        elif key==glfw.KEY_A:
            global_matrix = global_matrix @ T_10
        elif key==glfw.KEY_D:
            global_matrix = global_matrix @ (T_10).T
        elif key==glfw.KEY_1:
            global_matrix = np.identity(3)
        elif key==glfw.KEY_W:
            global_matrix = W @global_matrix
        elif key==glfw.KEY_S:
            global_matrix = T_10 @ global_matrix

def main():
    if not glfw.init():
        return
    window = glfw.create_window(640,640,'glOrtho()', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)



    #I = np.identity(3)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(global_matrix)
        glfw.swap_buffers(window)
        

    glfw.terminate()

if __name__ == "__main__":
    main()
