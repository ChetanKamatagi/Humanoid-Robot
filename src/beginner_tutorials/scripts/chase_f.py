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
    global x,y
    x=msg.x
    y=msg.y
    
def a_robber(msg):
    global ax,ay
    ax=msg.x
    ay=msg.y

def police(msg):
    global pub,x,y,th,lin_error_p,ang_error_p,I_l,I_a,kf,name_p,pt
    if x!=-2143 and y!=-2143:
        PI = 3.14159265
        px=msg.x
        py=msg.y
        pth=msg.theta
        
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
        lin_error=math.dist([x,y], [px,py])
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
                PID_l=4
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
        x=-2143
        y=-2143
        ax=-2143
        ay=-2143
        rospy.Subscriber('/rt_real_pose', Pose, robber)
        rospy.Subscriber(str(str(name_r)+'/pose'), Pose, a_robber)
        rospy.Subscriber(str(str(name_p)+'/pose'), Pose, police)
        
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    
