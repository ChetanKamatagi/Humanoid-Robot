#!/usr/bin/env python3
import time
import rospy
from std_msgs.msg import String
from std_srvs.srv import Trigger
from geometry_msgs.msg import Twist
flag=0
go=None
go1=None
def publish_cmd_vel_once(linear_x, angular_z):
    # rospy.init_node('cmd_vel_publisher_once', anonymous=True)
    cmd_vel_pub = rospy.Publisher('/cmd_vel_1', Twist, queue_size=1)

    cmd_vel_msg = Twist()
    cmd_vel_msg.linear.x = linear_x
    cmd_vel_msg.angular.z = angular_z

    cmd_vel_pub.publish(cmd_vel_msg)
    rospy.loginfo("********************************************")
def send_service_request1():
    rospy.wait_for_service('/start_roslaunch1')  # Replace with your actual service name
    try:
        # Create a service proxy
        start_roslaunch1 = rospy.ServiceProxy('/start_roslaunch1', Trigger)

        # Send a service request
        response = start_roslaunch1()

        # Check the service response
        if response.success:
            rospy.loginfo(f"Service call successful: {response.message}")
        else:
            rospy.loginfo(f"Service call failed: {response.message}")

    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")
def send_service_request2():
    rospy.wait_for_service('/start_roslaunch2')  # Replace with your actual service name
    try:
        # Create a service proxy
        start_roslaunch1 = rospy.ServiceProxy('/start_roslaunch2', Trigger)

        # Send a service request
        response = start_roslaunch1()

        # Check the service response
        if response.success:
            rospy.loginfo(f"Service call successful: {response.message}")
        else:
            rospy.loginfo(f"Service call failed: {response.message}")

    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")

def send_service_request3():
    rospy.wait_for_service('/start_roslaunch3')  # Replace with your actual service name
    try:
        # Create a service proxy
        start_roslaunch1 = rospy.ServiceProxy('/start_roslaunch3', Trigger)

        # Send a service request
        response = start_roslaunch1()

        # Check the service response
        if response.success:
            rospy.loginfo(f"Service call successful: {response.message}")
        else:
            rospy.loginfo(f"Service call failed: {response.message}")

    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")
def send_service_request4():
    rospy.wait_for_service('/start_roslaunch4')  # Replace with your actual service name
    try:
        # Create a service proxy
        start_roslaunch1 = rospy.ServiceProxy('/start_roslaunch4', Trigger)

        # Send a service request
        response = start_roslaunch1()

        # Check the service response
        if response.success:
            rospy.loginfo(f"Service call successful: {response.message}")
        else:
            rospy.loginfo(f"Service call failed: {response.message}")

    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")

def send_service_request5():
    rospy.wait_for_service('/start_roslaunch5')  # Replace with your actual service name
    try:
        # Create a service proxy
        start_roslaunch1 = rospy.ServiceProxy('/start_roslaunch5', Trigger)

        # Send a service request
        response = start_roslaunch1()

        # Check the service response
        if response.success:
            rospy.loginfo(f"Service call successful: {response.message}")
        else:
            rospy.loginfo(f"Service call failed: {response.message}")

    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")


def send_service_request6():
    rospy.wait_for_service('/start_roslaunch6')  # Replace with your actual service name
    try:
        # Create a service proxy
        start_roslaunch1 = rospy.ServiceProxy('/start_roslaunch6', Trigger)

        # Send a service request
        response = start_roslaunch1()

        # Check the service response
        if response.success:
            rospy.loginfo(f"Service call successful: {response.message}")
        else:
            rospy.loginfo(f"Service call failed: {response.message}")

    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")



def send_service_request7():
    rospy.wait_for_service('/start_roslaunch7')  # Replace with your actual service name
    try:
        # Create a service proxy
        start_roslaunch1 = rospy.ServiceProxy('/start_roslaunch7', Trigger)

        # Send a service request
        response = start_roslaunch1()

        # Check the service response
        if response.success:
            rospy.loginfo(f"Service call successful: {response.message}")
        else:
            rospy.loginfo(f"Service call failed: {response.message}")

    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")
def send_service_request8():
    rospy.wait_for_service('/start_roslaunch8')  # Replace with your actual service name
    try:
        # Create a service proxy
        start_roslaunch1 = rospy.ServiceProxy('/start_roslaunch8', Trigger)

        # Send a service request
        response = start_roslaunch1()

        # Check the service response
        if response.success:
            rospy.loginfo(f"Service call successful: {response.message}")
        else:
            rospy.loginfo(f"Service call failed: {response.message}")

    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")
def send_service_request9():
    rospy.wait_for_service('/start_roslaunch9')  # Replace with your actual service name
    try:
        # Create a service proxy
        start_roslaunch1 = rospy.ServiceProxy('/start_roslaunch9', Trigger)

        # Send a service request
        response = start_roslaunch1()

        # Check the service response
        if response.success:
            rospy.loginfo(f"Service call successful: {response.message}")
        else:
            rospy.loginfo(f"Service call failed: {response.message}")

    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")

def send_stop_request1():
    rospy.wait_for_service('/stop_roslaunch1')  # Replace with your actual service name
    try:
        publish_cmd_vel_once(0, 0)

        # Create a service proxy
        start_roslaunch1 = rospy.ServiceProxy('/stop_roslaunch1', Trigger)

        # Send a service request
        response = start_roslaunch1()

        # Check the service response
        if response.success:
            rospy.loginfo(f"Service call successful: {response.message}")
        else:
            rospy.loginfo(f"Service call failed: {response.message}")

    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")
def send_stop_request2():
    rospy.wait_for_service('/stop_roslaunch2')  # Replace with your actual service name
    try:
        publish_cmd_vel_once(0, 0)

        # Create a service proxy
        start_roslaunch1 = rospy.ServiceProxy('/stop_roslaunch2', Trigger)

        # Send a service request
        response = start_roslaunch1()

        # Check the service response
        if response.success:
            rospy.loginfo(f"Service call successful: {response.message}")
        else:
            rospy.loginfo(f"Service call failed: {response.message}")

    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")


def mode_callback(data):
    global flag
    rospy.loginfo(f"Received mode: {data.data}")
    rospy.loginfo(f">>>>>>>>>>>>>>>>>>>>>>>> {go1}")
    rospy.loginfo(flag)
    if data.data=="Interactive" and flag!=1:
        flag=1
        # send_service_request1()
        publish_cmd_vel_once(0, 0)
    elif data.data=="Charging_mode" and flag!=2:
        flag=2
        # send_service_request2()
        send_service_request6()
    elif data.data=="Person_follower" and flag!=3:
        flag=3
        send_service_request5()
        # send_service_request3()
    elif data.data=="CASE_tour" and flag!=4:
        flag=4
        # send_service_request4()
        send_service_request7()
    elif data.data=="goal_pub" and flag!= 7 and flag!=5:
        flag=5
        # flag=7
        send_service_request8()
    elif go=="dock" and go1=="yes" and flag==5:
        flag=7
        rospy.loginfo("*******************************************************")
        publish_cmd_vel_once(0, 0)
        send_service_request7()        

    elif data.data=="stoped" and flag!=6:
        flag=6
        send_stop_request2()
        # send_stop_request1()
        publish_cmd_vel_once(0, 0)
def d_mode_callback(data):
    global go
    go=str(data.data)

def d_mode_callback1(data):
    global go1
    go1=str(data.data)

def mode_subscriber():
    rospy.init_node('mode_subscriber', anonymous=True)
    cmd_goal_sub = rospy.Subscriber('cmd_goal', String, d_mode_callback)
    dock = rospy.Subscriber('dock_i', String, d_mode_callback1)

    rospy.Subscriber('mode', String, mode_callback)
    rospy.loginfo("Mode subscriber node ready.")
    rospy.spin()

if __name__ == '__main__':
    mode_subscriber()






