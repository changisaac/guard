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
# all possible msg types need to be imported and then placed into
# the MSG_TYPE dictionary in thein init of the SensorDataAggregator
from std_msgs.msg import String
from sensor_msgs.msg import Image
from sensor_msgs.msg import Imu
from realsense2_camera.msg import IMUInfo

"""
Class subscribes to specified data topics and 
stores all messages from those topics  to a single rosbag.
"""
class SensorDataAggregator:

    MSG_TYPE = {"Image": Image, "ImuInfo": IMUInfo, "Imu": Imu} 

    def __init__(self, bag_name, topic_msg_list, max_bag_size_bytes):
        self.bag_name = bag_name
        self.topic_msg_list = topic_msg_list
        self.max_bag_size_bytes = max_bag_size_bytes
       
        # init first bag
        self.bag = self.init_bag()
        
        # init all data topics subscribers
        for topic, msg in self.topic_msg_list:
            rospy.Subscriber(topic, self.MSG_TYPE[msg], self.callback, topic)

    def callback(self, data, args):
        self.write_bag(args, data)        

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
        file_name = "guard_" + self.bag_name + "_" + str(rospy.Time.now()) + ".bag"
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
    agg = SensorDataAggregator(
        "cam_2_rgb_image",
        [("/cam_2/color/image_raw", "Image")],
        50000000)

    imu_agg = SensorDataAggregator(
        "cam_2_imu",
        [("/cam_2/gyro/sample", "Imu")],
        50000000) 
    
    rospy.spin()

if __name__ == '__main__':
    main()

