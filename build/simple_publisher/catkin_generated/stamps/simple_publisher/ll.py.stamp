import rospy
import math
from geometry_msgs.msg import Twist, PoseWithCovarianceStamped
from nav_msgs.msg import Path
from tf.transformations import euler_from_quaternion
from move_base_msgs.msg import MoveBaseActionResult
from move_base_msgs.msg import MoveBaseActionGoal
from std_msgs.msg import String
import time
robot_x=0.1
robot_y=0.1
robot_a=0.0
temp_x=0.0
temp_y=0.0
temp_a=0.0
goal_x=0.0
goal_y=0.0
goal_a=0.0
len=0
goal_published = False
gp=0.0
weired=None
pub_d = rospy.Publisher('dock_i', String, queue_size=10)
def compute(Kp, Ki, Kd, setpoint, current_value, prev_error, integral):
    min_output = -180.0  # Minimum allowable control output
    max_output = 180.0 
    # Calculate the error
    error = setpoint - current_value

    # Calculate the integral term
    integral += error

    # Calculate the derivative term
    derivative = error - prev_error

    # Calculate the control output
    control_output = (Kp * error) + (Ki * integral) + (Kd * derivative)
    control_output = max(min_output, min(max_output, control_output))
    return control_output, integral
def calculate_angle(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    if x2==0 and y2==0:
        return 0
    if x2 - x1 == 0:
        if y1>y2:
            return 270.0
        else:
            return 90.0
    else:
        angle_rad = math.atan2(y2 - y1, x2 - x1)
        angle_deg = math.degrees(angle_rad)
        if angle_deg<=0:
            angle_deg=360+angle_deg
        return angle_deg
def map_value(value, source_min, source_max, target_min, target_max):
    # Calculate the percentage of value within the source range
    percentage = (value - source_min) / (source_max - source_min)
    
    # Map the percentage to the target range
    target_value = target_min + percentage * (target_max - target_min)
    
    return target_value
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
def d_mode_callback(data):
    global weired
    weired=str(data.data)

class KeyboardControl:
    def __init__(self):
        
        rospy.init_node('Script_controlling_ARDrone', anonymous=False)
        self.pub = rospy.Publisher('/cmd_vel_1', Twist, queue_size=1)
        self.rate = rospy.Rate(10)  # 10Hz
        # self.twist = Twist()
        

        # Create subscribers
        self.path_sub = rospy.Subscriber('/move_base/NavfnROS/plan', Path, self.callback)
        self.goal_subscriber = rospy.Subscriber('/move_base/goal', MoveBaseActionGoal, self.goal_callback)
        self.pose_robot_sub = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.amcl_pose_callback)
    # def status_callback(msg):
    #     # Handle the status message here
    #     status = msg.status.status
    #     goal_id = msg.status.goal_id.id
    #     print(f"Received status message: Status = {status}, Goal ID = {goal_id}")
    
    def goal_callback(msg,message_info):
        global goal_published
        goal_published = True
        # print(goal_published)
        rospy.loginfo("Goal has been published!")
    def callback(self, msg):
        global temp_x
        global temp_y 
        global temp_a
        global goal_a
        global goal_x
        global goal_y  
        global path_stack_nos
        global last_goal
        global last_goalw
        global gp
        global len
        last_goal=None
        last_goalw=None
        # print("--------------------------------------")
        path_stack_nos = 0
        for i in msg.poses:
            path_stack_nos += 1
            last_goal=i.pose.orientation.z
            last_goalw=i.pose.orientation.w
            if path_stack_nos == 8:
                temp_x = i.pose.position.x
                temp_y = i.pose.position.y
                # orientation_list1 = [i.pose.orientation.x, i.pose.orientation.y, i.pose.orientation.z, i.pose.orientation.w]
                # roll1,pitch1,yaw1= euler_from_quaternion(orientation_list1)
                # theta1 = (yaw1) * 180 / 3.141592653589793 
                # rospy.loginfo(f"***************({temp_x},{temp_y})***************************")

                # You can use temp_x and temp_y here
            
        orientation_list1 = [0, 0, last_goal, last_goalw]
        roll1,pitch1,yaw1= euler_from_quaternion(orientation_list1)
        gp = (yaw1) * 180 / 3.141592653589793 
        len=path_stack_nos          

    def amcl_pose_callback(self, msg):
        global robot_x
        global robot_y
        global robot_a
        
        pose = msg.pose.pose
        position = pose.position
        orientation_q = pose.orientation

        robot_x = position.x
        robot_y = position.y
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        
        roll,pitch,yaw= euler_from_quaternion(orientation_list)
        robot_a = (yaw) * 180 / 3.141592653589793  # Assuming orientation is represented as a quaternion
        if robot_a<=0:
            robot_a=360+robot_a
        # Your code to use the pose information goes here
        # rospy.loginfo(f"-----------------({robot_x},{robot_a})-----------------")
        # Modify self.twist based on pose information
        # For example, to move forward at a certain speed:
        # self.twist.linear.x = 0.1

    def run(self):
        Kp = 7.0  # Proportional gain
        Ki = 0.01  # Integral gain
        Kd = 0.01  # Derivative gain

        # Setpoint and initial values
        setpoint = 0                                                                                  
        current_value = 0.0
        prev_error = 0.0
        integral = 0.0
        time.sleep(4) 
        start=0
        
        while not rospy.is_shutdown():
            cmd_goal_sub = rospy.Subscriber('cmd_goal', String, d_mode_callback)
            if(start==0):
                print('START')
                tmp_twist = Twist()
                tmp_twist.angular.z = 0
                tmp_twist.linear.x = 0.03
                self.pub.publish(tmp_twist)
                time.sleep(15)
                tmp_twist.angular.z = 0
                tmp_twist.linear.x = 0
                self.pub.publish(tmp_twist)
                print('STOP')
                start=1
                
            twist = Twist()
            # Publish the modified twist command
            angle_r_p = calculate_angle((robot_x,robot_y),(temp_x,temp_y)) 
            distance = calculate_distance(robot_x, robot_y, temp_x, temp_y)
            # rospy.loginfo(f"-----------------({angle_r_p},{robot_a})-----------------") 
            if angle_r_p==0:
                t=0
            elif angle_r_p!=0:
                t=robot_a-angle_r_p
            if t>0:
                if t>180:
                    #left
                    val=t-360
                    if t-360>=30:
                        integral=0
                        above=1
                    else:    
                        above=0
                    control_output, integral = compute(Kp, Ki, Kd, setpoint, val, prev_error, integral)
                    prev_error = setpoint - val
                    
                    mapped_value = map_value(-control_output, -90, 90, -0.3, 0.3)
                    twist.angular.z = mapped_value
                    # rospy.loginfo(f"-----------------({mapped_value})-----------------")
                else:
                    val=t
                    if t>=30:
                        integral=0
                        above=1
                    else:    
                        above=0
                    #right
                    control_output, integral = compute(Kp, Ki, Kd, setpoint, val, prev_error, integral)
                    prev_error = setpoint - val
                    mapped_value = map_value(-control_output, -90, 90, -0.3, 0.3)
                    twist.angular.z = mapped_value
                    # rospy.loginfo(f"-----------------({mapped_value})-----------------")
                
            elif t<0: 
                if t<-180:
                    val=360+t
                    if 360+t>=30:
                        integral=0
                        above=1
                    else:    
                        above=0
                    #right
                    control_output, integral = compute(Kp, Ki, Kd, setpoint, val, prev_error, integral)
                    prev_error = setpoint - val
                    mapped_value = map_value(-control_output, -90, 90, -0.3, 0.3)
                    twist.angular.z = mapped_value
                    # rospy.loginfo(f"-----------------({mapped_value})-----------------")
                else:
                    val=t
                    if t<=-20:
                        integral=0
                        above=1
                    else:    
                        above=0
                    #left
                    control_output, integral = compute(Kp, Ki, Kd, setpoint, val, prev_error, integral)
                    prev_error = setpoint - val
                    mapped_value = map_value(-control_output, -90, 90, -0.3, 0.3)
                    twist.angular.z = mapped_value
                    # rospy.loginfo(f"-----------------({mapped_value})-----------------")
            else:
                twist.angular.z=0
                mapped_value=0
                control_output=0
                val=0
            if len<=8 :
                twist.angular.z=0
                twist.linear.x = 0
                # here orientation of goal
                fo=robot_a
                if robot_a>180:
                    fo=robot_a-360
                if abs(gp-fo)>180:
                    if gp-fo>0:
                        opt=gp-fo-360
                    elif gp-fo<0:
                        opt=gp-fo+360
                else:
                    opt=gp-fo
                    
                if opt >10:
                    rospy.loginfo("left")
                    twist.angular.z=-0.15
                elif opt <-10:
                    rospy.loginfo("right")
                    twist.angular.z=0.15
                    
                # if abs(opt)>3:
                #     twist.angular.z=-opt/500
                else:
                    twist.angular.z=0
                    twist.linear.x = 0
                    rospy.loginfo("right")
                    if weired=="dock" :
                        if -2.3<robot_x<-1.8 and -0.99<robot_y<-0.5:
                            pub_d.publish(str("yes"))
                        else:
                            pub_d.publish(str("no"))
                    elif weired=="CASE_lab" :
                        if -5.9<robot_x<-5.3 and -0.096403<robot_y<1.0:
                            pub_d.publish(str("yes"))
                        else:
                            pub_d.publish(str("no"))
                    elif weired=="IRP" :
                        if -4.9<robot_x<-4.3 and -1.7<robot_y<-1.1:
                            pub_d.publish(str("yes"))
                        else:
                            pub_d.publish(str("no"))
                    elif weired=="SRP" :
                        if -4.9<robot_x<-4.3 and -1.7<robot_y<-1.1:
                            pub_d.publish(str("yes"))
                        else:
                            pub_d.publish(str("no"))
                    
                print(gp,fo,opt )
            elif above==1:
                twist.linear.x = 0

            elif len>=8 and above==0:
                twist.linear.x = 0.3-abs(twist.angular.z)
            if goal_published==False:
                twist.linear.x = 0
                twist.angular.z=0
                self.pub.publish(twist)
            elif goal_published==True:
                self.pub.publish(twist)
            
            prev=weired

            self.rate.sleep()



def main():
    try:
        kc = KeyboardControl()
        kc.run()
    except KeyboardInterrupt:
        rospy.loginfo("Shutting down")

if __name__ == '__main__':
    main()
