#!/usr/bin/env python3

from __future__ import print_function
import sys
import rospy
from turtlesim.srv import *
import random

def kill_turt(resp1_name):
    rospy.wait_for_service('kill')
    try:
        kill_r = rospy.ServiceProxy('kill', Kill)
        name=''
        for i in range(len(resp1_name)-1):
            name+=resp1_name[i]
        name+=str(int(resp1_name[-1])-1)
        resp = kill_r(name)
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def spawn_random(x, y,theta):
    rospy.wait_for_service('spawn')
    try:
        spawn_r = rospy.ServiceProxy('spawn', Spawn)
        resp1 = spawn_r(float(x),float(y),float(theta),'')
        kill_turt(resp1.name)
        return resp1.name
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def usage():
    return "%s [x y]"%sys.argv[0]

if __name__ == "__main__":
    x=float(random.uniform(0, 11))
    y=float(random.uniform(0, 11))
    theta=float(random.uniform(0, 6.28318531))
    print(x, y,theta)
    print(spawn_random(x, y,theta))
