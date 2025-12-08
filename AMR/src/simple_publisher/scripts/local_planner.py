import rospy
import math
from geometry_msgs.msg import Twist, PoseWithCovarianceStamped
from nav_msgs.msg import Path
from tf.transformations import euler_from_quaternion
from move_base_msgs.msg import MoveBaseActionResult
from move_base_msgs.msg import MoveBaseActionGoal
from std_msgs.msg import String

class KeyboardControl:
    def __init__(self):
        rospy.init_node('local_plammer', anonymous=False)
        self.pub = rospy.Publisher('/cmd_vel_1', Twist, queue_size=1)
        self.rate = rospy.Rate(10)  # 10Hz
        self.path_sub = rospy.Subscriber('/move_base/NavfnROS/plan', Path, self.callback)
        self.goal_subscriber = rospy.Subscriber('/move_base/goal', MoveBaseActionGoal, self.goal_callback)
        self.pose_robot_sub = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.amcl_pose_callback)
    
    def goal_callback(msg,message_info):
        pass
    def callback(self, msg):
        print("++++++++++++++++++++++++++++++++++++++")
        for i in msg.poses:
                print(i.pose.position.x)
        print("--------------------------------------")

    def amcl_pose_callback(self, msg):
        pass

    def run(self):
        while not rospy.is_shutdown():
            print('running')
def main():
    try:
        kc = KeyboardControl()
        kc.run()
    except KeyboardInterrupt:
        rospy.loginfo("Shutting down")

if __name__ == '__main__':
    main()
