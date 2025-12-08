#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from std_msgs.msg import String
publisher = rospy.Publisher('initialpose', PoseWithCovarianceStamped, queue_size=10)
fly=0
def callback(msg):
    global fly  
    print(msg)
    data=PoseWithCovarianceStamped()
    data.header.frame_id= "map"
    data.pose.pose.position.x=-0.15058287978172302
    data.pose.pose.position.y=-0.03631751611828804
    data.pose.pose.position.z=0.0
    data.pose.pose.orientation.x=0
    data.pose.pose.orientation.y=0
    data.pose.pose.orientation.z= -0.9242665968253131
    data.pose.pose.orientation.w=  0.3817476365256951
    data.pose.covariance=[0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853892326654787]
    rospy.loginfo(data)
    publisher.publish(data)
    fly=1

    
def listener():
    while True:
        # In ROS, nodes are uniquely named. If two nodes with the same
        # name are launched, the previous one is kicked off. The
        # anonymous=True flag means that rospy will choose a unique
        # name for our 'listener' node so that multiple listeners can
        # run simultaneously.
        rospy.init_node('listener', anonymous=True)
        rospy.Subscriber('f_str', String, callback)
        '''
        data=PoseWithCovarianceStamped()
        #data.header.stamp = rospy.Time.now()
        data.header.frame_id= "map"
        #data.header.seq= 1
        data.pose.pose.position.x=-0.8931779861450195
        data.pose.pose.position.y=0.17107726633548737
        data.pose.pose.position.z=0.0
        data.pose.pose.orientation.x=0
        data.pose.pose.orientation.y=0
        data.pose.pose.orientation.z= -0.7019907622269513
        data.pose.pose.orientation.w= 0.7121860499532575
        data.pose.covariance=[0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853892326654787]
        rospy.loginfo(data)
        publisher.publish(data)
        '''
        if fly==1:
            break
          # spin() simply keeps python from exiting until this node is stopped
        # rospy.spin()

if __name__ == '__main__':
    listener()
