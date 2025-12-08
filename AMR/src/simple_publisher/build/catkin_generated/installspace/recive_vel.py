#!/usr/bin/env python3
import socket
import rospy
from std_msgs.msg import String
import time
from geometry_msgs.msg import Twist
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('10.4.1.98', 12045) 
client_socket.connect(server_address)
welcome_message = client_socket.recv(1024)
print(f"Server says: {welcome_message.decode('utf-8')}")
rospy.init_node('sui', anonymous=True)
cmd_vel_pub = rospy.Publisher('/cmd_vel_1', Twist, queue_size=1)
def publish_cmd_vel_once(linear_x, angular_z):
    
    cmd_vel_msg = Twist()
    cmd_vel_msg.linear.x = linear_x
    cmd_vel_msg.angular.z = angular_z
    cmd_vel_pub.publish(cmd_vel_msg)
while True:
    # message ="position"
    # client_socket.sendall(message.encode('utf-8'))
    welcome_message = client_socket.recv(1124)
    f=str(welcome_message.decode('utf-8'))
    print(f)
    x=f.split("|")
    print(x)
    print(f"Server says: {x[0],x[1]}")
    if x[0].count('.')>1:
        u=float(x[0].replace('.', '', 1))/100
    if x[1].count('.')>1:
        j=float(x[1].replace('.', '', 1))/100
    if x[0].count('.')==1 and x[1].count('.')==1:
        u=float(x[0])
        j=float(x[1])
    publish_cmd_vel_once(u, j)
    x=[]
client_socket.close()




