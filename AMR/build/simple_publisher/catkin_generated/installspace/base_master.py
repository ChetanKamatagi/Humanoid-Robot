
#!/usr/bin/env python

import subprocess
import rospy
from std_srvs.srv import Trigger, TriggerResponse

launch_process = None
launch_files = {
    'start_roslaunch5': ('simple_publisher', 'person_follower.launch'),
    'start_roslaunch6': ('simple_publisher', 'local+_nav.launch'),
    'start_roslaunch7': ('simple_publisher', 'dock.launch'),
    'start_roslaunch8': ('simple_publisher', 'local+_nav.launch'),
    'start_roslaunch9': ('simple_publisher', 'dock.launch'),
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
    # person follower
    start_service5 = rospy.Service('start_roslaunch5', Trigger, lambda req: start_roslaunch(req, 'start_roslaunch5'))
    # charging mode
    start_service6 = rospy.Service('start_roslaunch6', Trigger, lambda req: start_roslaunch(req, 'start_roslaunch6'))
    # CASE tour
    start_service7 = rospy.Service('start_roslaunch7', Trigger, lambda req: start_roslaunch(req, 'start_roslaunch7'))
    # Goal publisher
    start_service8 = rospy.Service('start_roslaunch8', Trigger, lambda req: start_roslaunch(req, 'start_roslaunch8'))
    
    start_service9 = rospy.Service('start_roslaunch9', Trigger, lambda req: start_roslaunch(req, 'start_roslaunch9'))

    stop_service = rospy.Service('stop_roslaunch2', Trigger, stop_roslaunch)
    rospy.loginfo("Ready to start/stop ROS launch process.")
    rospy.spin()

if __name__ == '__main__':
    run_services()
