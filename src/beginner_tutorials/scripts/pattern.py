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
        resp1 = spawn_r(float(x),float(y),float(theta),name)
        #nav_turt(float(x),float(y),float(theta),resp1.name)
        #kill_turt(resp1.name)
        return resp1.name
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
        
def talker():
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        vel = Twist()
        vel.linear.x = 5
        vel.angular.z = 5
        pub.publish(vel)
        rate.sleep()
        
def callback(msg):
    global pub,x,y,th,lin_error_p,ang_error_p,I_l,I_a,name_n,name,kf,i,j
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
    
    if(abs(ang_error)<3.14159265/16):
        if(lin_error<3):
            P_l=lin_error*kp_l
            I_l+=lin_error*ki_l
            D_l=(lin_error-lin_error_p)*kd_l
            lin_error_p=lin_error
            PID_l=P_l+I_l+D_l
        else:
            PID_l=5
    else:
        PID_l=0
    '''
    print(lin_error,PID_l)
    print(th*180/3.14159265,pth*180/3.14159265,PID_a)
    '''
    if (abs(lin_error)<0.01):
        if j<19:
            kill_turt(name_n)
            j+=1
            if j%4==0:
                x=float(1)
                y=float(i)
                print(1,i)
            elif j%4==1:
                x=float(9)
                y=float(i)
                print(9,i)
                i+=1
            elif j%4==2:
                x=float(9)
                y=float(i)
                print(9,i)
            elif j%4==3:
                x=float(1)
                y=float(i)
                print(1,i)
                i+=1
            th=float(PI/2)
            name_n=spawn_random(x, y,th)
        elif j==19:
            kill_turt(name_n)
            print('Pattern finished')
            j+=1
        PID_l=0
        PID_a=0
        
    vel = Twist()
    vel.linear.x = PID_l
    vel.angular.z = PID_a
    
    pub.publish(vel)

if __name__ == "__main__":
    try:
        i=1
        j=0
        res_turt()
        kill_turt('turtle1')
        x=float(1)
        y=float(i)
        th=float(0)
        name=spawn_random(x, y,th,'turtle1')
        #-------        
        j=1
        x=float(9)
        y=float(i)
        th=float(PI/2)
        #print(x, y,th)
        name_n=spawn_random(x, y,th)
        i+=1
        #--------                  Spawn a new turtle bot as the goal
        
        rospy.init_node('pattern', anonymous=True)
        pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber(str(str(name)+'/pose'), Pose, callback)
        
        rospy.spin()
    except rospy.ROSInterruptException:
        kill_turt(name_n)
    finally:
        kill_turt(name_n)
