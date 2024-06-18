#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3Stamped
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import sensor_msgs.msg
import numpy as np
import time
pub = rospy.Publisher('/rev_scan', LaserScan, queue_size = 10)
pub_cmd = rospy.Publisher('/cmd_vel_1', Twist, queue_size = 10)

lin_error_p=0
ang_error_p=0
I_l=0
I_a=0

PI = 3.14159265
kf=0

th=480
pos_x=-123
pos_y=-123
c_pos_y=-123
g_i=0
prc_flg=[[-1,-1,-1,-1]]*2
prc_flg=[]

def polar_to_cartesian(angle, distance):
    radians = np.radians(angle+45)
    x = (distance * np.cos(radians))
    y = (distance * np.sin(radians))
    return x, abs(y)

def odom_callback(msg):
    global th
    th=msg.vector.z

def angl_callback(msg):
    global pos_x,pos_y
    #print(msg.pose.pose.position.x,msg.pose.pose.position.y)
    #print(msg)
    pos_x=msg.pose.pose.position.x
    pos_y=msg.pose.pose.position.y

def callback(msg):
    global th,pos_x,pos_y,prc_flg,c_pos_y,g_i
    print('+++++++++++++++++++++++++++++++++++++++++')
    use_th=1
    of_ang=45+4.18
    dst=0.361
    if th!=480 and pos_x!=-123 and pos_y!=-123:
        print(len(prc_flg),end=' | ')
        ang=len(msg.ranges)
        if th > 180:
            th-=360
        #print(th,end=' | ')
        if len(prc_flg)==0:
            cmd_vel=Twist()
            if th > 180:
                th-=360
            if use_th:
                fang=of_ang
            else:
                fang=of_ang-th
            ang_o=10
            tl=[]
            mxd=[]
            i_min=1000
            mn_ang=-1
            for i in range(len(msg.ranges)):
                if (i>(fang-ang_o)/360*ang and i<(fang+ang_o)/360*ang):
                    if (0.3<msg.ranges[i] and msg.ranges[i]<1000):
                        i_tmp=msg.ranges[i]
                        if(i_min>i_tmp):
                            i_min=msg.ranges[i]
                            mn_ang=i
                            mxd.append(dst)
                        else:
                            mxd.append(dst)
                    else:
                        mxd.append(dst)
                    tl.append(msg.ranges[i])
                else:
                    mxd.append(dst)
                    tl.append(dst)
            
            ang_error=((mn_ang/ang*360)-fang)
            print(ang_error,i_min)
            mxd[mn_ang]=i_min
            #mxd[int(fang/360*ang)]=i_min#0.555
            if 1:
                msg.ranges=tuple(mxd)
            else:
                msg.ranges=tuple(tl)
            pub.publish(msg)
            if th > 180:
                th-=360
                #'''
            i_dis=0.88
            if(i_min>i_dis):
                if(i_min-i_dis)>0.5:
                    cmd_vel.linear.x=0.5
                    cmd_vel.angular.z=-ang_error/10 
                else:
                    if((i_min-i_dis)<0.03):
                        cmd_vel.linear.x=0.03
                        cmd_vel.angular.z=-ang_error/100
                    else:
                        cmd_vel.linear.x=i_min-i_dis
                        cmd_vel.angular.z=-ang_error/50 
                pub_cmd.publish(cmd_vel)
            else:
                cmd_vel.linear.x=0
                cmd_vel.angular.z=0
                pub_cmd.publish(cmd_vel)
                prc_flg.append(90)
                #'''
        elif len(prc_flg)==1:
            if th > 180:
                th-=360
            if use_th:
                fang=of_ang
            else:
                fang=of_ang-th
            ang_o=20
            tl=[]
            mxd=[]
            i_min=1000
            mn_ang=-1
            for i in range(len(msg.ranges)):
                if (i>(fang-ang_o)/360*ang and i<(fang+ang_o)/360*ang):
                    if (0.3<msg.ranges[i] and msg.ranges[i]<1000):
                        i_tmp=msg.ranges[i]
                        if(i_min>i_tmp):
                            i_min=msg.ranges[i]
                            mn_ang=i
                            mxd.append(dst)
                        else:
                            mxd.append(dst)
                    else:
                        mxd.append(dst)
                    tl.append(msg.ranges[i])
                else:
                    mxd.append(dst)
                    tl.append(dst)
            ang_error=((mn_ang/ang*360)-fang)
            print(ang_error,i_min)
            mxd[mn_ang]=i_min
            #mxd[int(fang/360*ang)]=i_min#0.555
            if 1:
                msg.ranges=tuple(mxd)
            else:
                msg.ranges=tuple(tl)
            pub.publish(msg)
            #'''
            cmd_vel=Twist()
            if abs(ang_error)>1.5:
                cmd_vel.angular.z=-ang_error/100
            else:
                cmd_vel.angular.z=0
            pub_cmd.publish(cmd_vel)
            cmd_vel=Twist()
            cmd_vel.angular.z=0.3
            pub_cmd.publish(cmd_vel)
            time.sleep(6)
            cmd_vel.angular.z=0
            pub_cmd.publish(cmd_vel)
            prc_flg.append(90)
        elif len(prc_flg)==2:
            cmd_vel=Twist()
            if th > 180:
                th-=360
            if use_th:
                fang=of_ang
            else:
                fang=of_ang-th
            ang_o=5
            tl=[]
            mxd=[]
            i_min=1000
            mn_ang=-1
            for i in range(len(msg.ranges)):
                if (i>(fang-ang_o)/360*ang and i<(fang+ang_o)/360*ang):
                    if (0.3<msg.ranges[i] and msg.ranges[i]<1000):
                        i_tmp=msg.ranges[i]
                        if(i_min>i_tmp):
                            i_min=msg.ranges[i]
                            mn_ang=i
                            mxd.append(dst)
                        else:
                            mxd.append(dst)
                    else:
                        mxd.append(dst)
                    tl.append(msg.ranges[i])
                else:
                    mxd.append(dst)
                    tl.append(dst)
            ang_error=((mn_ang/ang*360)-fang)
            print(ang_error,i_min)
            mxd[mn_ang]=i_min
            #mxd[int(fang/360*ang)]=i_min#0.555
            if 1:
                msg.ranges=tuple(mxd)
            else:
                msg.ranges=tuple(tl)
            pub.publish(msg)
            if th > 180:
                th-=360
                #'''
            i_dis=1.632
            g_i+=1
            if(g_i>100):
                if(i_min>i_dis):
                    if(i_min-i_dis)>0.5:
                        cmd_vel.linear.x=0.5
                        cmd_vel.angular.z=-ang_error/10
                    else:
                        if((i_min-i_dis)<0.03):
                            cmd_vel.linear.x=0.03
                            cmd_vel.angular.z=-ang_error/50
                        else:
                            cmd_vel.linear.x=i_min-i_dis
                            cmd_vel.angular.z=-ang_error/10 
                    pub_cmd.publish(cmd_vel)
                else:
                    cmd_vel.linear.x=0
                    cmd_vel.angular.z=0
                    pub_cmd.publish(cmd_vel)
                    prc_flg.append(90)
                    #'''
        elif len(prc_flg)==3:
            if th > 180:
                th-=360
            if use_th:
                fang=of_ang
            else:
                fang=of_ang-th
            ang_o=20
            tl=[]
            mxd=[]
            i_min=1000
            mn_ang=-1
            for i in range(len(msg.ranges)):
                if (i>(fang-ang_o)/360*ang and i<(fang+ang_o)/360*ang):
                    if (0.3<msg.ranges[i] and msg.ranges[i]<1000):
                        i_tmp=msg.ranges[i]
                        if(i_min>i_tmp):
                            i_min=msg.ranges[i]
                            mn_ang=i
                            mxd.append(dst)
                        else:
                            mxd.append(dst)
                    else:
                        mxd.append(dst)
                    tl.append(msg.ranges[i])
                else:
                    mxd.append(dst)
                    tl.append(dst)
            
            ang_error=((mn_ang/ang*360)-fang)
            print(ang_error,i_min)
            mxd[mn_ang]=i_min
            #mxd[int(fang/360*ang)]=i_min#0.555
            if 1:
                msg.ranges=tuple(mxd)
            else:
                msg.ranges=tuple(tl)
            pub.publish(msg)
            #'''
            cmd_vel=Twist()
            if abs(ang_error)>1.5:
                cmd_vel.angular.z=-ang_error/100
            else:
                cmd_vel.angular.z=0
            pub_cmd.publish(cmd_vel)
            cmd_vel=Twist()
            cmd_vel.angular.z=0.3
            pub_cmd.publish(cmd_vel)
            time.sleep(6.3)
            cmd_vel.angular.z=0
            pub_cmd.publish(cmd_vel)
            prc_flg.append(90)
            #'''
        elif len(prc_flg)==4:
            if th > 180:
                th-=360
            if use_th:
                fang=of_ang+180
            else:
                fang=of_ang+180-th
            ang_o=20
            tl=[]
            mxd=[]
            i_min=1000
            mn_ang=-1
            for i in range(len(msg.ranges)):
                if (i>(fang-ang_o)/360*ang and i<(fang+ang_o)/360*ang):
                    if (0.3<msg.ranges[i] and msg.ranges[i]<1000):
                        i_tmp=msg.ranges[i]
                        if(i_min>i_tmp):
                            i_min=msg.ranges[i]
                            mn_ang=i
                            mxd.append(dst)
                        else:
                            mxd.append(dst)
                    else:
                        mxd.append(dst)
                    tl.append(msg.ranges[i])
                else:
                    mxd.append(dst)
                    tl.append(dst)
            
            ang_error=((mn_ang/ang*360)-fang)
            print(ang_error,i_min)
            mxd[mn_ang]=i_min
            #mxd[int(fang/360*ang)]=i_min#0.555
            if 1:
                msg.ranges=tuple(mxd)
            else:
                msg.ranges=tuple(tl)
            pub.publish(msg)
            #'''
            cmd_vel=Twist()
            if abs(ang_error)>1.5:
                cmd_vel.angular.z=-ang_error/100
            else:
                cmd_vel.angular.z=0
                prc_flg.append(0)
            pub_cmd.publish(cmd_vel)
        elif len(prc_flg)==5:
            if th > 180:
                th-=360
            if use_th:
                fang=of_ang+180
            else:
                fang=of_ang+180-th
            ang_o=20
            tl=[]
            mxd=[]
            i_min=1000
            mn_ang=-1
            for i in range(len(msg.ranges)):
                if (i>(fang-ang_o)/360*ang and i<(fang+ang_o)/360*ang):
                    if (0.3<msg.ranges[i] and msg.ranges[i]<1000):
                        i_tmp=msg.ranges[i]
                        if(i_min>i_tmp):
                            i_min=msg.ranges[i]
                            mn_ang=i
                            mxd.append(dst)
                        else:
                            mxd.append(dst)
                    else:
                        mxd.append(dst)
                    tl.append(msg.ranges[i])
                else:
                    mxd.append(dst)
                    tl.append(dst)
            
            ang_error=((mn_ang/ang*360)-fang)
            print(ang_error,i_min)
            mxd[mn_ang]=i_min
            #mxd[int(fang/360*ang)]=i_min#0.555
            if 1:
                msg.ranges=tuple(mxd)
            else:
                msg.ranges=tuple(tl)
            pub.publish(msg)
            #'''
            cmd_vel=Twist()
            i_dis=0.38
            if(i_min>i_dis):
                if(i_min-i_dis)>1:
                    cmd_vel.linear.x=-0.5
                    cmd_vel.angular.z=-ang_error/10 
                else:
                    if((i_min-i_dis)<0.1):
                        cmd_vel.linear.x=-0.03
                        cmd_vel.angular.z=-ang_error/100
                    else:
                        cmd_vel.linear.x=-(i_min-i_dis)/2
                        cmd_vel.angular.z=-ang_error/60 
                pub_cmd.publish(cmd_vel)
            else:
                cmd_vel.linear.x=0
                cmd_vel.angular.z=0
                pub_cmd.publish(cmd_vel)
                prc_flg.append(90)
                #'''
        else:
            if th > 180:
                th-=360
            if use_th:
                fang=of_ang+180
            else:
                fang=of_ang+180-th
            ang_o=20
            tl=[]
            mxd=[]
            i_min=1000
            mn_ang=-1
            for i in range(len(msg.ranges)):
                if (i>(fang-ang_o)/360*ang and i<(fang+ang_o)/360*ang):
                    if (0.3<msg.ranges[i] and msg.ranges[i]<1000):
                        i_tmp=msg.ranges[i]
                        if(i_min>i_tmp):
                            i_min=msg.ranges[i]
                            mn_ang=i
                            mxd.append(dst)
                        else:
                            mxd.append(dst)
                    else:
                        mxd.append(dst)
                    tl.append(msg.ranges[i])
                else:
                    mxd.append(dst)
                    tl.append(dst)
            
            ang_error=((mn_ang/ang*360)-fang)
            print(ang_error,i_min)
            mxd[mn_ang]=i_min
            #mxd[int(fang/360*ang)]=i_min#0.555
            if 1:
                msg.ranges=tuple(mxd)
            else:
                msg.ranges=tuple(tl)
            pub.publish(msg)
    print('------------------------------------------')

def listener():
    rospy.init_node('revised_scan', anonymous=True)
    sub = rospy.Subscriber('/scan', LaserScan, callback)
    sub_angl = rospy.Subscriber('/odom', Odometry, angl_callback)
    sub_odom = rospy.Subscriber('/motors_ticks', Vector3Stamped, odom_callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
