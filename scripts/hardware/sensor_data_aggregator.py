#!/usr/bin/env python

# Forest AI
# Maintainer: Isaac Chang i5chang@uwaterloo.ca

from __future__ import print_function

# ROS imports
import rospy
import roslib
import rosbag

# default library imports
import sys
import cv2
from cv_bridge import CvBridge, CvBridgeError

# ROS msg imports
from std_msgs.msg import String
from sensor_msgs.msg import Image
from sensor_msgs.msg import Imu

"""
Class subscribes to each sensor type and data channel and 
stores messages to rosbag.
"""
class SensorDataAggregator:

    def __init__(self):
        self.bridge = CvBridge()

        # sensor data subscribers
        #rospy.Subscriber("/camera/color/image_raw",Image,self.callback)
        rospy.Subscriber('/imu', Imu, self.imu_cb)

    def rgb_image_raw_cb(self, data):
        pass

    def gps_cb(self, data):
        pass
    
    def obd_steering_accel_cb(self, data):
        pass

    def imu_cb(self, data):
        rospy.loginfo(data)

def main():
    agg = SensorDataAggregator()
    rospy.init_node("sensor_data_aggregator", anonymous=True)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.loginfo(rospy.get_caller_id(), "Shutting Down")

if __name__ == '__main__':
	main()
