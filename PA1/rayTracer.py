#!/usr/bin/env python3
# -*- coding: utf-8 -*
# see examples below
# also read all the comments below.

import os
from pickle import TRUE
import sys
import pdb  # use pdb.set_trace() for debugging
# or use code.interact(local=dict(globals(), **locals()))  for debugging.
import code
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image


class Color:
    def __init__(self, R, G, B):
        self.color = np.array([R, G, B]).astype(np.float)

    # Gamma corrects this color.
    # @param gamma the gamma value to use (2.2 is generally used).
    def gammaCorrect(self, gamma):
        inverseGamma = 1.0 / gamma
        self.color = np.power(self.color, inverseGamma)

    def toUINT8(self):
        return (np.clip(self.color, 0, 1)*255).astype(np.uint8)


class Shader:
    def __init__(self, type):
        self.t = type


class ShaderPhong(Shader):
    def __init__(self, diffuse, specular, exponent):
        self.d = diffuse
        self.s = specular
        self.e = exponent


class ShaderLambertian(Shader):
    def __init__(self, diffuse):
        self.d = diffuse


class Sphere:
    def __init__(self, center, radius, shader):
        self.c = center
        self.r = radius
        self.s = shader


class Box:
    def __init__(self, minPt, maxPt, shader):
        self.minPt = minPt
        self.maxPt = maxPt
        self.s = shader


class View:
    def __init__(self, viewPoint, viewDir, viewUp, viewProjNormal, viewWidth, viewHeight, projDistance, intensity):
        self.viewPoint = viewPoint
        self.viewDir = viewDir
        self.viewUp = viewUp
        self.viewProjNormal = viewProjNormal
        self.viewWidth = viewWidth
        self.viewHeight = viewHeight
        self.projDistance = projDistance
        self.intensity = intensity


class Light:
    def __init__(self, position, intensity):
        self.position = position
        self.intensity = intensity

def raytrace (surface,point,dir):
    distance = sys.maxsize
    idx = -1
    cnt = -1
    inter_p = np.array([0,0,0])
    for i in surface:
        cnt = cnt + 1
        if i.__class__.__name__ == 'Sphere':
            cen = i.c
            r = i.r
            del_t = (np.dot(dir,point-cen)*np.dot(dir,point-cen)-np.dot(point-cen,point-cen)+r*r) # root_part_t
            
            if( del_t >=0 ): #일반화 하기
                #print(point,cen)
                #print(point-cen)
                a = ((np.dot(dir,(cen - point)) -np.sqrt(del_t)))
                b = ((np.dot(dir,(cen - point)) +np.sqrt(del_t)))
                if(a >=0) :
                    intersetion_p =  point + a*dir
                    dis = np.linalg.norm(point - intersetion_p)
                    if(dis < distance):
                        idx = cnt
                        distance = dis
                        inter_p = intersetion_p
                if(b >=0) :
                    intersetion_p =  point + b*dir
                    dis = np.linalg.norm(point - intersetion_p)
                    if(dis < distance):
                        idx = cnt
                        distance = dis
                        inter_p = intersetion_p
        elif i.__class__.__name__ == 'Box':
            tmin = (i.minPt-point)
            tmax = (i.maxPt-point)
            id = 1

            for i in range(0,3) :
                tmin[i] = tmin[i]/dir[i]
                tmax[i] = tmax[i]/dir[i]

                if tmin[i] > tmax[i] :
                    tmin[i],tmax[i] = tmax[i],tmin[i]

            if tmin[0] > tmax[1] or tmin[1] > tmax[0] :
                continue
            min_ = max(tmin[0],tmin[1])
            max_ = min(tmax[0],tmax[1])
            if min_ > tmax[2] or tmin[2] > max_ :
                continue
            min_ = max(min_,tmin[2])
            max_ = min(max_,tmax[2])

            dis = min_
            if dis < distance:
                distance = dis
                idx = cnt
                inter_p = point + distance*dir                
        

    # return gamma and index of closest figure in list
    #print(inter_p)
    return [idx,inter_p]

def shading(idx,interset_p,point,dir,surface,light):
    intersetion_p = interset_p
    norm_p = np.array([0, 0, 0]).astype(np.float)
    pix_v = np.array([0,0,0]).astype(np.float)
    col =Color(0,0,0)

    if (idx == -1) :
        return np.array([0, 0, 0])
    else :
        #print(interset_p)
        if surface[idx].__class__.__name__ == 'Sphere':
            #print('Sphere')
            cen = surface[idx].c
            norm_p = intersetion_p - cen
            #if(abs(np.sqrt(np.dot(norm_p,norm_p)) - surface[idx].r)>0.000001):
                #print('check', abs(np.sqrt(np.dot(norm_p,norm_p))), surface[idx].r)
            norm_p = norm_p/np.linalg.norm(norm_p)
            #print(norm_p)

        elif surface[idx].__class__.__name__ == 'Box':
            num = -1
            id = 0
            id_c = 0
            for i in range(0,3):
                if abs(intersetion_p[i] - surface[idx].minPt[i]) < 0.000001:
                    num = i
                    id = -1
                elif abs(intersetion_p[i] - surface[idx].maxPt[i]) < 0.000001:
                    num = i
                    id = 1
            if(surface[idx].maxPt[num] > surface[idx].minPt[num]):
                id_c = 1
            else:
                id_c = -1
            norm_p[num] = id*id_c
            #print(norm_p,interset_p,num,id,id_c)
        
            
        
        for i in light:
            
            # sum of the reflected light
            l_i= i.position - intersetion_p
            l_i = l_i/np.linalg.norm(l_i)
            #print(-l_i)
            #print(i.position)
            check = raytrace(surface,i.position,-l_i)
            #print(interset_p,norm_p)
            #if surface[idx].__class__.__name__ == 'Sphere':
            #    print(interset_p,idx,check)

            if check[0] == idx :
                #print('check com')
                
                n_l = np.dot(norm_p,l_i)
                #print(n_l)
                h = l_i - dir
                h = h / np.linalg.norm(h)
                n_h = np.dot(norm_p,h)
                if surface[idx].s.__class__.__name__ == 'ShaderPhong':
                    #print('Phong')
                    pix_v += (surface[idx].s.d*i.intensity)*max(0,n_l)
                    #print(pix_v)
                    pix_v += (surface[idx].s.s*i.intensity)*(max(0,n_h) ** surface[idx].s.e)
                    #print(pix_v)
                    col = Color(pix_v[0],pix_v[1],pix_v[2])
                elif surface[idx].s.__class__.__name__ == "ShaderLambertian":
                    #print('Lambertian')
                    pix_v += (surface[idx].s.d*i.intensity)*max(0,n_l)
                    #print(pix_v)
                    col = Color(pix_v[0],pix_v[1],pix_v[2])
                    
        
    
    col.gammaCorrect(2.2)
    return col.toUINT8()

def main():

    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    # set default values
    viewDir = np.array([0, 0, -1]).astype(np.float)
    viewUp = np.array([0, 1, 0]).astype(np.float)
    # you can safely assume this. (no examples will use shifted perspective camera)
    viewProjNormal = -1*viewDir
    viewWidth = 1.0
    viewHeight = 1.0
    projDistance = 1.0
    # how bright the light is.
    intensity = np.array([1, 1, 1]).astype(np.float)

    imgSize = np.array(root.findtext('image').split()).astype(np.int)

    for c in root.findall('shader'):
        diffuseColor_c = np.array(c.findtext(
            'diffuseColor').split()).astype(np.float)
        print('name', c.get('name'))
        print('diffuseColor', diffuseColor_c)
    #code.interact(local=dict(globals(), **locals()))

    # extract camera info
    for c in root.findall('camera'):
        viewPoint = np.array(c.findtext('viewPoint').split()).astype(np.float)
        print('viewpoint', viewPoint)
        viewDir = np.array(c.findtext('viewDir').split()).astype(np.float)
        print('viewDir', viewDir)
        if (c.findtext('projNormal')):
            viewProjNormal = np.array(c.findtext('projNormal').split()).astype(np.float)
            print('viewProjNormal', viewProjNormal)
        viewUp = np.array(c.findtext('viewUp').split()).astype(np.float)
        print('viewUp', viewUp)
        if (c.findtext('projDistance')):
            projDistance = np.array(c.findtext('projDistance').split()).astype(np.float)
            print('projDistance', projDistance)
        viewWidth = np.array(c.findtext('viewWidth').split()).astype(np.float)
        print('viewWidth', viewWidth)
        viewHeight = np.array(c.findtext('viewHeight').split()).astype(np.float)
        print('viewHeight', viewHeight)
    view = View(viewPoint, viewDir, viewUp, viewProjNormal, viewWidth, viewHeight, projDistance, intensity)

    # extract light info
    light = []
    for c in root.findall('light'):
        light_position=np.array(c.findtext('position').split()).astype(np.float)
        print('light_position', light_position)
        light_intensity=np.array(c.findtext('intensity').split()).astype(np.float)
        print('light_intensity', light_intensity)
        light.append(Light(light_position,light_intensity))

    # extract surface info
    surface = []
    for c in root.findall('surface'):
        type_sur = c.get('type')
        ref = ''
        shader = Shader('')
        type_sh = ''
        for d in c:
                if d.tag == 'shader':
                    ref = d.get('ref')
        for d in root.findall('shader'):
                if d.get('name') == ref:
                    diffuse = np.array(d.findtext('diffuseColor').split()).astype(np.float)
                    type_sh = d.get('type')
                    if type_sh == 'Lambertian':
                        shader = ShaderLambertian(diffuse)
                    elif type_sh == 'Phong':
                        exponent = np.array(d.findtext('exponent').split()).astype(np.float)
                        specular = np.array(d.findtext('specularColor').split()).astype(np.float)
                        shader = ShaderPhong(diffuse, specular, exponent)

        if type_sur == 'Sphere':
            center_c = np.array(c.findtext('center').split()).astype(np.float)
            radius_c = np.array(c.findtext('radius')).astype(np.float)
            surface.append(Sphere(center_c, radius_c, shader))
            print(type_sur,center_c,radius_c,type_sh)
        elif type_sur == 'Box':
            minPt_c = np.array(c.findtext('minPt').split()).astype(np.float)
            maxPt_c = np.array(c.findtext('maxPt').split()).astype(np.float)
            surface.append(Box(minPt_c, maxPt_c, shader))
            print(type_sur,minPt_c,maxPt_c,type_sh)




    # Create an empty image
    channels = 3
    img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
    img[:, :] = 0

    # replace the code block below!

    n_viewDir = view.viewDir/np.linalg.norm(view.viewDir)
    proj_cen = view.viewPoint + (view.projDistance*n_viewDir)
    print('proj_cen',proj_cen)

    Dirprojx = np.cross(n_viewDir,view.viewUp)
    Dirprojx = Dirprojx/np.linalg.norm(Dirprojx)
    Dirprojy = np.cross(n_viewDir,Dirprojx)
    Dirprojy = Dirprojy/np.linalg.norm(Dirprojy)

    print(Dirprojx)
    print(Dirprojy)

    #viewHeight , viewWidth normalization
    n_width = view.viewWidth/imgSize[0]
    n_height = view.viewHeight/imgSize[1]

    # init_proj_point
    init_proj_point = proj_cen - ((view.viewWidth/2)-0.5*(n_width))*Dirprojx - ((view.viewHeight/2)-0.5*(n_height))*Dirprojy
    print(init_proj_point)

    

    for i in np.arange(imgSize[0]) :
        for j in np.arange(imgSize[1]):
            #compute viewing ray
            proj_point = init_proj_point + i*n_width*Dirprojx + j*n_height*Dirprojy
            #n_viewProj = viewProjNormal           #orthographic
            n_viewProj = proj_point - viewPoint    #perspective
            n_viewProj = n_viewProj/np.linalg.norm(n_viewProj)
            intersection_info = raytrace(surface,viewPoint,n_viewProj)
            img[j][i] = shading(intersection_info[0],intersection_info[1],proj_point,n_viewProj,surface,light)




    rawimg = Image.fromarray(img, 'RGB')
    # rawimg.save('out.png')
    rawimg.save(sys.argv[1]+'.png')


if __name__ == "__main__":
    main()
