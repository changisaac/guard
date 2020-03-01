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
        self.max_bag_size_bytes = 500000000
        self.bag = self.init_bag()
        self.bridge = CvBridge()

        # sensor data topics
        self.rgb_image_topic = "/camera/color/image_raw"
        #self.imu_topic = "/imu"

        # sensor data subscribers
        rospy.Subscriber(self.rgb_image_topic, Image, self.rgb_image_cb)
        #rospy.Subscriber(self.imu_topic, Imu, self.imu_cb)

    def rgb_image_cb(self, data):
        self.write_bag(self.rgb_image_topic, data)        

    def gps_cb(self, data):
        pass
    
    def obd_steering_accel_cb(self, data):
        pass

    def imu_cb(self, data):
        self.write_bag(self.imu_topic, data)

    # writes to rosbag but keeps track of max file size, if passed, make new bag 
    def write_bag(self, topic, msg):
        try:
            size = self.bag.size
        except ValueError:
            rospy.logerr("Bag file is closed")

        if (size + sys.getsizeof(msg)*1.5) > self.max_bag_size_bytes:
            self.bag.close()
            self.bag = self.init_bag()

        self.bag.write(topic, msg)
        self.bag.flush()
            
    # inits a bag file with unix time stamp in name and returns it
    def init_bag(self):
        file_name = "guard_" + str(rospy.Time.now()) + ".bag"
        bag = rosbag.Bag(file_name, "w")
        bag._set_chunk_threshold(self.max_bag_size_bytes)
        return bag

    def __del__(self):
        self.bag.close()

def main():
    rospy.init_node("sensor_data_aggregator", anonymous=True)
    #rospy.on_shutdown()
    
    # SensorDataAggregator relies on rospy.get_rostime()
    # this needs the node to be initialized
    agg = SensorDataAggregator()
    rospy.spin()

if __name__ == '__main__':
    main()

