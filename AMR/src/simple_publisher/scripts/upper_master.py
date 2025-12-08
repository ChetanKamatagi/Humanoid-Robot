#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

def cmd_vel_callback(data):
    # This function will be called whenever a message is received on the cmd_vel topic
    linear_x = data.linear.x
    angular_z = data.angular.z

    # Add your custom logic here based on the received cmd_vel values
    rospy.loginfo(f"Received cmd_vel - Linear X: {linear_x}, Angular Z: {angular_z}")

def cmd_vel_subscriber():
    # Initialize the ROS node
    rospy.init_node('cmd_vel_subscriber', anonymous=True)

    # Subscribe to the cmd_vel topic and specify the callback function
    rospy.Subscriber('cmd_vel_1', Twist, cmd_vel_callback)

    # Keep the node running
    rospy.spin()

if __name__ == '__main__':
    # Run the subscriber node
    cmd_vel_subscriber()
