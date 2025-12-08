
#!/usr/bin/env python

import subprocess
import rospy
from std_srvs.srv import Trigger, TriggerResponse

launch_process = None
launch_files = {
    'start_roslaunch1': ('rplidar_ros', 'rplidar_a2m12.launch'),
    'start_roslaunch2': ('simple_publisher', 'nav.launch'),
    'start_roslaunch3': ('rplidar_ros', 'rplidar_a2m12.launch'),
    'start_roslaunch4': ('simple_publisher', 'odom_pub_all.launch'),
    # Add more services and launch files as needed
}

def start_roslaunch(request, service_name):
    global launch_process

    if launch_process is not None and launch_process.poll() is None:
        # Stop the current ROS launch process
        rospy.loginfo("Stopping the current ROS launch process.")
        launch_process.terminate()
        launch_process.wait()

    if service_name in launch_files:
        package, launch_file = launch_files[service_name]
        roslaunch_cmd = ['roslaunch', package, launch_file]
        launch_process = subprocess.Popen(roslaunch_cmd)
        rospy.loginfo(f"ROS launch process for {launch_file} started.")
        return TriggerResponse(success=True, message=f"ROS launch process for {launch_file} started.")
    else:
        rospy.loginfo("Invalid service name.")
        return TriggerResponse(success=False, message="Invalid service name.")

def stop_roslaunch(request):
    global launch_process
    if launch_process is not None and launch_process.poll() is None:
        # Stop the current ROS launch process
        launch_process.terminate()
        launch_process.wait()
        rospy.loginfo("ROS launch process stopped.")
        return TriggerResponse(success=True, message="ROS launch process stopped.")
    else:
        rospy.loginfo("No ROS launch process running.")
        return TriggerResponse(success=False, message="No ROS launch process running.")

def run_services():
    rospy.init_node('ros_launch_controller', anonymous=True)
    start_service1 = rospy.Service('start_roslaunch1', Trigger, lambda req: start_roslaunch(req, 'start_roslaunch1'))
    start_service2 = rospy.Service('start_roslaunch2', Trigger, lambda req: start_roslaunch(req, 'start_roslaunch2'))
    start_service3 = rospy.Service('start_roslaunch3', Trigger, lambda req: start_roslaunch(req, 'start_roslaunch3'))
    start_service4 = rospy.Service('start_roslaunch4', Trigger, lambda req: start_roslaunch(req, 'start_roslaunch4')) 
    # Add more services as needed
    stop_service = rospy.Service('stop_roslaunch', Trigger, stop_roslaunch)
    rospy.loginfo("Ready to start/stop ROS launch process.")
    rospy.spin()

if __name__ == '__main__':
    run_services()
