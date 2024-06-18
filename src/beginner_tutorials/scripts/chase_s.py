#!/usr/bin/env python3

from __future__ import print_function
import sys
import rospy
from turtlesim.srv import *
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import random
import math
import os
from math import atan
import numpy as np
import time

pt=time.time()
lin_error_p=0
ang_error_p=0
I_l=0
I_a=0

PI = 3.14159265
kf=0
    
def get_intersections(x0, y0, r0, x1, y1, r1):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    d=math.sqrt((x1-x0)**2 + (y1-y0)**2)
    
    # non intersecting
    if d > r0 + r1 :
        return None
    # One circle within other
    if d < abs(r0-r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
    else:
        a=(r0**2-r1**2+d**2)/(2*d)
        h=math.sqrt(r0**2-a**2)
        x2=x0+a*(x1-x0)/d   
        y2=y0+a*(y1-y0)/d   
        x3=x2+h*(y1-y0)/d     
        y3=y2-h*(x1-x0)/d 

        x4=x2-h*(y1-y0)/d
        y4=y2+h*(x1-x0)/d
        
        return (x3, y3, x4, y4)
        
def define_circle(p1, p2, p3):
    temp = p2[0] * p2[0] + p2[1] * p2[1]
    bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
    cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
    det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])
    if abs(det) < 1.0e-6:
        return (None, np.inf)
    cx = (bc*(p2[1] - p3[1]) - cd*(p1[1] - p2[1])) / det
    cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det
    radius = np.sqrt((cx - p1[0])**2 + (cy - p1[1])**2)
    return ((cx, cy), radius)
    
def findAngle(x1, y1, x2, y2):
    vector_1 = [(x2-x1),(y2-y1)]
    vector_2 = [1, 0]

    unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
    unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle = np.arccos(dot_product)

    return angle
    
def kill_turt(name):
    rospy.wait_for_service('kill')
    try:
        kill_r = rospy.ServiceProxy('kill', Kill)
        resp = kill_r(name)
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
        
def res_turt():
    os.system('rosservice call /reset')
    

def spawn_random(x, y,theta,name=''):
    rospy.wait_for_service('spawn')
    try:
        spawn_r = rospy.ServiceProxy('spawn', Spawn)
        resp1 = spawn_r(float(x),float(y),float(theta),'turtle1')
        #nav_turt(float(x),float(y),float(theta),resp1.name)
        #kill_turt(resp1.name)
        return resp1.name
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
        
        
def robber(msg):
    global x1,y1,x2,y2,x3,y3
    if x1==-2143 and y1==-2143:
        x1=msg.x
        y1=msg.y
    elif x2==-2143 and y2==-2143:
        x2=msg.x
        y2=msg.y
    elif x3==-2143 and y3==-2143:
        x3=msg.x
        y3=msg.y
    else:
        x3=x2
        x2=x1
        x1=msg.x
        y3=y2
        y2=y1
        y1=msg.y
    
def a_robber(msg):
    global ax,ay
    ax=msg.x
    ay=msg.y

def police(msg):
    global pub,x1,y1,x2,y2,x3,y3,th,lin_error_p,ang_error_p,I_l,I_a,kf,name_p,pt
    if x1!=-2143 and y1!=-2143 and x2!=-2143 and y2!=-2143 and x3!=-2143 and y3!=-2143:
        PI = 3.14159265
        px=msg.x
        py=msg.y
        pth=msg.theta
        
        cntr,r0=define_circle([x1,y1],[x2,y2],[x3,y3])
        x0,y0=cntr
        r1=math.dist([x1,y1],[x2,y2])
        d1x,d1y,d2x,d2y=get_intersections(x0, y0, r0, x1, y1, r1)
        #print([x1,y1],[x2,y2],[x3,y3])
        #print(d1x,d1y,d2x,d2y)
        if abs(d2x-x2)<0.01 and abs(d2y-y2)<0.01:
            x=d1x
            y=d1y
            #print('up')
        elif abs(d1x-x2)<0.01 and abs(d1y-y2)<0.01:
            x=d2x
            y=d2y
            #print('dn')
        else:
            x=x1
            y=y1
            #print('--')
        
        th=findAngle(px,py,x,y)
        if (y<py):
            th=-th
        '''
        elif (y>=py and x<px):
            th+=3.14159265/2
        elif (y>=py and x>=px):
            th-=3.14159265/2
        th=th*180/3.142857
        pth=pth*180/3.142857
        '''
        lin_error=math.dist([x,y],[px,py])
        if(pth<-PI/2 or pth>PI/2):
            if((th<0 and pth<0) or (th>0 and pth>0)):
                pass
            elif(th<0 and pth>0):
                th+=3.14159265*2
            elif(th>0 and pth<0):
                pth+=3.14159265*2
        ang_error=th-pth

        kp_l=2
        ki_l=0
        kd_l=0.01

        kp_a=3
        ki_a=0
        kd_a=0

        P_a=ang_error*kp_a
        I_a+=ang_error*ki_a
        D_a=(ang_error-ang_error_p)*kd_a
        ang_error_p=ang_error
        PID_a=P_a+I_a+D_a
        
        if(abs(ang_error)<3.14159265/4):
            if(lin_error<2):
                P_l=lin_error*kp_l
                I_l+=lin_error*ki_l
                D_l=(lin_error-lin_error_p)*kd_l
                lin_error_p=lin_error
                PID_l=P_l+I_l+D_l
            else:
                PID_l=3
        else:
            PID_l=0
        
        #print(lin_error,PID_l)
        #print(th*180/3.14159265,pth*180/3.14159265,PID_a)
        
        if ax!=-2143 and ay!=-2143:
            a_lin_error=math.dist([ax,ay], [px,py])
        else:
            a_lin_error=lin_error
        if (abs(a_lin_error)<1):
            kill_turt('turtle1')
            tx=float(random.uniform(0, 11.08))
            ty=float(random.uniform(0, 11.08))
            tth=float(random.uniform(0, 6.28318531))
            name_p=spawn_random(tx, ty,tth,'turtle1')
            print('Reached')
            PID_l=0
            PID_a=0
            
        vel = Twist()
        vel.linear.x = PID_l
        vel.angular.z = PID_a
        
        pub.publish(vel)
    
if __name__ == "__main__":
    try:
        rospy.init_node('chase_fast', anonymous=True)
        pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        name_r='rbt'
        name_p='turtle1'
        x1=-2143
        y1=-2143
        x2=-2143
        y2=-2143
        x3=-2143
        y3=-2143
        ax=-2143
        ay=-2143
        rospy.Subscriber('/rt_real_pose', Pose, robber)
        rospy.Subscriber(str(str(name_r)+'/pose'), Pose, a_robber)
        rospy.Subscriber(str(str(name_p)+'/pose'), Pose, police)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    
