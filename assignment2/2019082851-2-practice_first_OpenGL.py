
import numpy as np
import glfw
from OpenGL.GL import *


def render(): 
    #pass
    glClear(GL_COLOR_BUFFER_BIT) 
    glLoadIdentity() 
    glBegin(GL_TRIANGLES) 
    glVertex2f(0.0, 1.0) 
    glVertex2f(-1.0,-1.0) 
    glVertex2f(1.0,-1.0) 
    glEnd()

def main(): 
    # Initialize the library 
    if not glfw.init(): 
        return
# Create a windowed mode window and its OpenGL context 
    window = glfw.create_window(640,480,"Hello World", None,None) 
    if not window: 
        glfw.terminate() 
        return
# Make the window's context current 
    glfw.make_context_current(window)

# Loop until the user closes the window 
    while not glfw.window_should_close(window): 
    # Poll events glfw.poll_events()
        glfw.poll_events()
    # Render here, e.g. using pyOpenGL 
        render()
    # Swap front and back buffers 
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__": main()
