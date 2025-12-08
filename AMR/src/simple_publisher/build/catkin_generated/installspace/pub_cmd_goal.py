#!/usr/bin/env python3

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Quaternion
from tf.transformations import quaternion_from_euler
from std_msgs.msg import String
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Path

class MoveBaseController:
    def __init__(self):
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.client.wait_for_server()
        self.cmd_goal_sub = rospy.Subscriber('cmd_goal', String, self.mode_callback)
        self.clear_global_plan_pub = rospy.Publisher('/move_base/NavfnROS/plan', Path, queue_size=1)
        self.current_goal = None  # Variable to store the current goal

    def clear_global_plan(self):
        empty_path = Path()
        self.clear_global_plan_pub.publish(empty_path)
    def mode_callback(self, mode_msg):
        rospy.loginfo(f"Received mode: {mode_msg.data}")
        if mode_msg.data == "Coridar":
            self.move_to_goal(0,-4.1, -9.1)
        elif mode_msg.data == "CASE_lab":
            self.move_to_goal(3,-5.8198927, 0.2123784)
        elif mode_msg.data == "SRP":
            self.move_to_goal(0,-2.6, -2.6)
        elif mode_msg.data == "IRP":
            self.move_to_goal(2,-4.6942,-1.4582)
        elif mode_msg.data == "dock":
            self.move_to_goal(1,-2.0415, -0.7138)
        elif mode_msg.data == 'stoped':
            self.cancel_goal()
            self.clear_global_plan()

    def move_to_goal(self,i, x, y):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"    
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        if i!=1:
            # quaternion = quaternion_from_euler(0, 0, 0) 
            # goal.target_pose.pose.orientation = Quaternion(*quaternion)
            goal.target_pose.pose.orientation.z=-0.9062977852794212
            goal.target_pose.pose.orientation.w=0.42263970991568717
        elif i==1:
            goal.target_pose.pose.orientation.z=0.4237
            goal.target_pose.pose.orientation.w=0.9057
        elif i==2:
            goal.target_pose.pose.orientation.z=0.90758604
            goal.target_pose.pose.orientation.w=0.419866
        elif i==3:
            goal.target_pose.pose.orientation.z=-0.742223935754357
            goal.target_pose.pose.orientation.w=0.6701519448552784

        self.current_goal = goal
        self.client.send_goal(goal)
        rospy.loginfo("Goal execution done!")
        if goal.target_pose.pose.position.x==-1.5:
            rospy.loginfo("oooooooooooooooooooooo")
        
    def cancel_goal(self):
        if self.current_goal and self.client.get_state() == actionlib.GoalStatus.ACTIVE:
            rospy.loginfo("Cancelling the current goal.")
            self.client.cancel_all_goals()
        else:
            rospy.loginfo("No active goal to cancel.")

if __name__ == '__main__':
    try:
        rospy.init_node('movebase_controller_py')
        movebase_controller = MoveBaseController()
        rospy.spin()

    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
