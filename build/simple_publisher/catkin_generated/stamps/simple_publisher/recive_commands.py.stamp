import socket
import rospy
from std_msgs.msg import String
import time
truth=None
weired=None
def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('10.4.1.247', 12345)
    client_socket.connect(server_address)
    return client_socket
def d_mode_callback(data):
    global weired
    weired=str(data.data)
def d_mode_callback1(data):
    global truth
    truth=str(data.data)
if __name__ == '__main__':
    rospy.init_node('recive_commands', anonymous=True)
    pub = rospy.Publisher('mode', String, queue_size=10)
    pub1 = rospy.Publisher('cmd_goal', String, queue_size=10)
 
    client_socket = connect_to_server()
    while True:
        cmd_goal_sub = rospy.Subscriber('cmd_goal', String, d_mode_callback)
        dock = rospy.Subscriber('dock_i', String, d_mode_callback1)
        try:
            if weired=="CASE_lab" and truth=="yes":
                message = "case"
            elif weired=="IRP" and truth=="yes":
                message = "intro"
            else:
                message = "nothing"
            client_socket.sendall(message.encode('utf-8'))
            time.sleep(0.3)

            try:
                welcome_message = client_socket.recv(1024)
                received_data = welcome_message.decode('utf-8')
                print(received_data)

                data_parts = received_data.split("|")
                if len(data_parts) >= 2:
                    message1 = data_parts[1]
                    message2 = data_parts[0]
                    pub.publish(message1)
                    pub1.publish(message2)

                if message.lower() == 'exit':
                    break

            except BrokenPipeError:
                print("BrokenPipeError: Connection reset by peer. Reconnecting...")
                client_socket.close()
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_address = ('10.1.6.248', 12345)
                client_socket.connect(server_address)

        except ConnectionResetError as e:
            print(f"ConnectionResetError: {e}")
            print("Attempting to reconnect...")
            time.sleep(2)
            client_socket = connect_to_server()

    client_socket.close()
