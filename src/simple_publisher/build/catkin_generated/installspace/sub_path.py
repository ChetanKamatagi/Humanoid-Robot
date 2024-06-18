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
            self.move_to_goal(-4.1, -9.1)  # Set your desired x and y coordinates
        elif mode_msg.data == "CASE_lab":
            self.move_to_goal(2.3, -6.3)
        elif mode_msg.data == "SRP":
            self.move_to_goal(-2.6, -2.6)
        elif mode_msg.data == "IRP":
            self.move_to_goal(0.5, 0.5)
        elif mode_msg.data == 'stoped':
            self.cancel_goal()
            self.clear_global_plan()

    def move_to_goal(self, x, y):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"    
        goal.target_pose.header.stamp = rospy.Time.now()

        # Set the target position
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        quaternion = quaternion_from_euler(0, 0, 0) 
        goal.target_pose.pose.orientation = Quaternion(*quaternion)

        # Store the current goal
        self.current_goal = goal

        self.client.send_goal(goal)
        rospy.loginfo("Goal execution done!")

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
