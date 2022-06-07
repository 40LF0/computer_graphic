Programming Assignment #2 (Cow roller coaster)
====================

#  1. Project objective
---------------------

Understand how to generate spline curves.

#  2. My implementaion
----------------------
A. First step     
(Implement vertical dragging) 
-----------------------------
```
def onMouseDrag(window, x, y):
    global isDrag,cursorOnCowBoundingBox, pickInfo, cow2wld
    if isDrag: 
        print( "in drag mode %d\n"% isDrag);
        if  isDrag==V_DRAG:
            # vertical dragging
            # TODO:
            # create a dragging plane perpendicular to the ray direction, 
            # and test intersection with the screen ray.
            if cursorOnCowBoundingBox:
                ray=screenCoordToRay(window, x, y);
                pp=pickInfo;
                p=Plane(np.array((1/np.sqrt(2),0,1/np.sqrt(2))), pp.cowPickPosition);
                c=ray.intersectsPlane(p);
                currentPos=ray.getPoint(c[1])
                
                T=np.eye(4)
                setTranslation(T, currentPos-pp.cowPickPosition)
                cow2wld=T@pp.cowPickConfiguration;
                
                planes=[];
                cow=cowModel
                bbmin=cow.bbmin
                bbmax=cow.bbmax
                planes.append(makePlane(bbmin, bbmax, vector3(0,1,0)));
                planes.append(makePlane(bbmin, bbmax, vector3(0,-1,0)));
                planes.append(makePlane(bbmin, bbmax, vector3(1,0,0)));
                planes.append(makePlane(bbmin, bbmax, vector3(-1,0,0)));
                planes.append(makePlane(bbmin, bbmax, vector3(0,0,1)));
                planes.append(makePlane(bbmin, bbmax, vector3(0,0,-1)));
                o=ray.intersectsPlanes(planes);
                cursorOnCowBoundingBox=o[0]
                cowPickPosition=ray.getPoint(o[1])
                cowPickLocalPos=transform(np.linalg.inv(cow2wld),cowPickPosition)
                pickInfo=PickInfo( o[1], cowPickPosition, cow2wld, cowPickLocalPos)
                
            print('vdrag')
        else:
            ...
        

```
Vertical dragging and horizontal dragging have two differences.             
First is plane for cursor.
`p=Plane(np.array((1/np.sqrt(2),0,1/np.sqrt(2))), pp.cowPickPosition);`
Second is updating PickInfo.
During vertical dragging, PickInfo is updated every tick.
          
B. Second step     
(Implements the UI for control point) 
-----------------------------
Informations about the UI for control point is needed.    
```
# control point state
num_control_point = -1 # number of control points (if -1, there is no control point)
control_point_location = [] # location for control point
is_fulll_cotrol_point_location = False 
# if control_point_locatio is full ,true ; else, fasle.  
```
```
def onMouseButton(window,button, state, mods):
    global isDrag, V_DRAG, H_DRAG
    global num_control_point, control_point_location, is_fulll_cotrol_point_location
    global animStartTime
    ...
    if button == glfw.MOUSE_BUTTON_LEFT:
        ...
        elif state == GLFW_UP and isDrag!=0:
            isDrag=H_DRAG;
            if cursorOnCowBoundingBox:
                num_control_point += 1
                print("num_control_point %d\n" % num_control_point)
                if num_control_point > 0:
                    control_point_location.append(cow2wld.copy())
                    if num_control_point == 6:
                        is_fulll_cotrol_point_location = True
                        animStartTime = glfw.get_time();
                        isDrag = 0
                        
            print( "Left mouse up\n");
            # start horizontal dragging using mouse-move events.
    elif button == glfw.MOUSE_BUTTON_RIGHT:
        ...
```
```
def display():
    global cameraIndex, cow2wld
    global num_control_point, control_point_location, is_fulll_cotrol_point_location
    global animationStartTime,cowRotationPos,cowstart
    global cowstart
    ...   
    # TODO: 
    # update cow2wld here to animate the cow.
    #animTime=glfw.get_time()-animStartTime;
    #you need to modify both the translation and rotation parts of the cow2wld matrix every frame.
    # you would also probably need a state variable for the UI.
    if num_control_point < 6:
        drawCow(cow2wld, cursorOnCowBoundingBox);
        if -1 < num_control_point: 
            for i in control_point_location:
                drawCow(i, True)
        														# Draw cow.
    #elif num_control_point == 6:
    else:          
       ...
            												
    glFlush();
```

C. Third step     
(Implements Cow roller coaster) 
-----------------------------
Informations about  animate state is needed.    
```
# animate state
animationStartTime = 0
cowstart = None
```
Also function to decide the location of the cow roller coaster is needed.
```
def animlocation(time): #(aniTime%6)
    global control_point_location
    p0 = control_point_location[int(time)-1]
    p1 = control_point_location[int(time)]
    p2 = control_point_location[int(time)-5]
    p3 = control_point_location[int(time)-4]
    t = time - int(time)
    return (((1 - t) ** 3) * p0
     + (3 * (t ** 3) - 6 * (t ** 2) + 4) * p1
     + (-3 * (t ** 3) + 3 * (t ** 2) + 3 * t + 1) * p2
     + (t ** 3) * p3) / 6
```
```
def display():
    global cameraIndex, cow2wld
    global num_control_point, control_point_location, is_fulll_cotrol_point_location
    global animationStartTime,cowRotationPos,cowstart
    global cowstart
    glClearColor(0.8, 0.9, 0.9, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);				
    ...
    if num_control_point < 6:
    ...
    
    else :
            time = animTime % 6 #test
            # drawCow(control_point_location[int(time)],True) #test
            # animlocation by time and control_point_location information
            # drawCow(animlocation(time),True)
            animloc = animlocation(time)
            directionVec = normalize(getTranslation(animloc) - getTranslation(cow2wld))
            roll = 0
            pitch = np.arcsin(directionVec[1])
            yaw = np.arctan2(directionVec[2], directionVec[0])
            if yaw < 0 :
                pitch_n = -pitch
            else :
                pitch_n = pitch
            
            Rx = np.array([[1, 0, 0],
                 [0, np.cos(pitch_n), -np.sin(pitch)],
                 [0, np.sin(pitch), np.cos(pitch_n)]])
            Ry = np.array([[np.cos(yaw), 0, np.sin(yaw)],
                  [0, 1, 0],
                  [-np.sin(yaw), 0, np.cos(yaw)]])
            Rz = np.array([[np.cos(roll), -np.sin(roll), 0],
                  [np.sin(roll), np.cos(roll), 0],
                  [0, 0, 1]])
            cow2wld[:3, :3] = (Ry@Rx@Rz).T
            setTranslation(cow2wld, getTranslation(animloc))
            drawCow(cow2wld,True);
            												
    glFlush();
```

