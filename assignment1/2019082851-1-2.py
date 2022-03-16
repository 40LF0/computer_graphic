import OpenGL
import numpy as np
import glfw


M = np.arange(2,27)
print(M)
M = M.reshape(5,5)
print(M)
for i in range(5):
    M[i][0]=0
print(M)
M = M@M
print(M)
v= M[0]
# print(v@v)
v_mg = np.sqrt(np.sum(v@v))
print(v_mg)