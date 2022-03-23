import array
from ast import For
from telnetlib import STATUS
import glfw 
from OpenGL.GL import * 
import numpy as np

status = [GL_POLYGON,GL_POINTS,GL_LINES,GL_LINE_STRIP,GL_LINE_LOOP,GL_TRIANGLES,GL_TRIANGLE_STRIP,GL_TRIANGLE_FAN,GL_QUADS,GL_QUAD_STRIP]

global_num = 4


def render(num): 
    glClear(GL_COLOR_BUFFER_BIT) #Error
    glLoadIdentity()

    # 숫자 입력하면 Primitive Types 변함!
    glBegin(status[num])
    glColor3ub(255, 255, 255) 


    orign_t = np.array([1.0,0.0])
    for i in range(0, 12):
        th = np.pi/6 *i
        T = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
        glVertex2fv(T @ orign_t) 
    
    glEnd()

def key_callback(window, key, scancode, action, mods): 
    for i in range(0,10):
        if key==48+i: #KEY_0 = 48 ... KEY_9 =57 
            if action==glfw.PRESS: 
                global global_num
                global_num = i

def main(): 
    if not glfw.init(): 
        return 
    window = glfw.create_window(480,480, "2019082851", None,None) 
    if not window: 
        glfw.terminate() 
        return 
    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)
    
    while not glfw.window_should_close(window): 
        glfw.poll_events() 
        # 숫자 입력하면 Primitive Types 변함!
        render(global_num)
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__": 
    main()