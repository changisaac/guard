#!/usr/bin/env python

# Maintainer: Isaac Chang

"""
Interfaces with IMU connected serially to PI and publishes
IMU msgs to "imu" channel.
"""

import rospy
from guard.msg import IMU

def pub_data():
    pub = rospy.Publisher('imu', IMU, queue_size=10)
    rospy.init_node('imu_hardware', anonymous=True)
    rate = rospy.Rate(10)

    # interface with serial connection to arduino

    while not rospy.is_shutdown():
        # fill msg with imu data

if __name__ == '__main__':
    try:
        
