#!/usr/bin/env python3

from __future__ import print_function
import sys
import rospy
from turtlesim.srv import *
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import time
import numpy as np

pt=time.time()
    
mu=0.0
std = 1
def gaussian_noise(x,mu,std):
    noise = np.random.normal(mu, std, 1)
    x_noisy = x + noise
    return x_noisy 
    
def callback(msg):
    global pt,pub,pubn,mu,std
    ct=time.time()
    if(ct-pt>5):
        pt=time.time()
        pub.publish(msg)
        nsg = Pose()
        nsg.x = gaussian_noise(msg.x,mu,std)
        nsg.y = gaussian_noise(msg.y,mu,std)
        pubn.publish(nsg)

if __name__ == "__main__":
    try:
        name='rbt'
        rospy.init_node('pose', anonymous=True)
        pub = rospy.Publisher('/rt_real_pose', Pose, queue_size=10)
        pubn = rospy.Publisher('/rt_noisy_pose', Pose, queue_size=10)
        rospy.Subscriber(str(str(name)+'/pose'), Pose, callback)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    
