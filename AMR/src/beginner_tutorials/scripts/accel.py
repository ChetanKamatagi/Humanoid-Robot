#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import time
pub_cmd = rospy.Publisher('/cmd_vel_2', Twist, queue_size=1)
dx=-1234
dz=-1234
z=0
prev_time=time.time()

def cmd_callback(msg):
    global dx,dz
    dx=msg.linear.x
    dz=msg.angular.z
    
def odom_callback(msg):
    global dx,dz,pub_cmd,prev_time,z
    if dx!=-1234 and dz!=-1234:
        x=msg.twist.twist.linear.x
        #z=msg.twist.twist.angular.z
        ox=x
        oz=z
        accel_x_lim=0.05
        accel_z_lim=0.3
        decel_x_lim=0.05
        decel_z_lim=0.3
        crnt_time=time.time()
        td=1#crnt_time-prev_time
        prev_time=time.time()
        if(x==0):
            if ((abs(dx-x)/td)<accel_x_lim):
                x=dx
            else:
                if dx>0:
                    x+=(accel_x_lim*td)
                else:
                    x-=(accel_x_lim*td)
        elif(x>0):
            if (dx>=x):
                if ((abs(dx-x)/td)<accel_x_lim):
                    x=dx
                else:
                    x+=(accel_x_lim*td)
            else:
                if(dx<0):
                    if ((abs(0-x)/td)<decel_x_lim):
                        x=0
                    else:
                        x-=(decel_x_lim*td)
                if ((abs(dx-x)/td)<decel_x_lim):
                    x=dx
                else:
                    x-=(decel_x_lim*td)
        elif(x<0):
            if (x>=dx):
                if ((abs(dx-x)/td)<accel_x_lim):
                    x=dx
                else:
                    x-=(accel_x_lim*td)
            else:
                if(dx>0):
                    if ((abs(0-x)/td)<decel_x_lim):
                        x=0
                    else:
                        x+=(decel_x_lim*td)
                if ((abs(dx-x)/td)<decel_x_lim):
                    x=dx
                else:
                    x+=(decel_x_lim*td)
#------------------------------------------------------------------------
        if(z==0):
            if ((abs(dz-z)/td)<accel_z_lim):
                z=dz
            else:
                if dz>0:
                    z+=(accel_z_lim*td)
                else:
                    z-=(accel_z_lim*td)
        elif(z>0):
            if (dz>=z):
                if ((abs(dz-z)/td)<accel_z_lim):
                    z=dz
                else:
                    z+=(accel_z_lim*td)
            else:
                if(dz<0):
                    if ((abs(0-z)/td)<decel_z_lim):
                        z=0
                    else:
                        z-=(decel_z_lim*td)
                if ((abs(dz-z)/td)<decel_z_lim):
                    z=dz
                else:
                    z-=(decel_z_lim*td)
        elif(z<0):
            if (z>=dz):
                if ((abs(dz-z)/td)<accel_z_lim):
                    z=dz
                else:
                    z-=(accel_z_lim*td)
            else:
                if(dz>0):
                    if ((abs(0-z)/td)<decel_z_lim):
                        z=0
                    else:
                        z+=(decel_z_lim*td)
                if ((abs(dz-z)/td)<decel_z_lim):
                    z=dz
                else:
                    z+=(decel_z_lim*td)
        #print(ox,oz,'|',x,z,'|',dx,dz)
        vel = Twist()
        vel.linear.x = x
        vel.angular.z = z
        pub_cmd.publish(vel)

if __name__ == '__main__':
    rospy.init_node('local_planner', anonymous=True)
    rospy.Subscriber("/odom", Odometry, odom_callback)
    rospy.Subscriber('/cmd_vel_1', Twist, cmd_callback)
    rospy.spin()
