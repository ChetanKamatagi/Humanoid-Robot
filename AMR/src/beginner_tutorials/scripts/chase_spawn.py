#!/usr/bin/env python3

from __future__ import print_function
import sys
import rospy
from turtlesim.srv import *
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import os
import random

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
    speed=5
    radius=10
    #radius=radius-speed
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        vel = Twist()
        vel.linear.x = (radius)*speed
        vel.angular.z = (2)*speed
        pub.publish(vel)
        rate.sleep()

if __name__ == "__main__":
    try:
        rospy.init_node('chase_spawn', anonymous=True)
        res_turt()
        x=float(5.5)
        y=float(0.8)
        th=float(0)
        name_n=spawn_random(x, y,th,'rbt')
        kill_turt('turtle1')
        pub = rospy.Publisher('rbt/cmd_vel', Twist, queue_size=10)
        talker()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
