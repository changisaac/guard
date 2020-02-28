#!/usr/bin/env python

# Maintainer: Isaac Chang

"""
Interfaces with IMU connected serially to PI and publishes
IMU msgs to "imu" channel.
"""

import rospy
from sensor_msgs.msg import Imu

def pub_data():
    pub_imu = rospy.Publisher('imu', Imu, queue_size=10)
    rospy.init_node('imu_hardware', anonymous=True)
    rate = rospy.Rate(10)
    
    imu_msg = Imu()
    imu_msg.header.stamp = rospy.Time.now()

    # interface with serial connection ...

    # rospy.loginfo("Ready for publishing imu:" + serial_port)

    while not rospy.is_shutdown():
        # fill msg with imu data
        rospy.loginfo(imu_msg)
        pub_imu.publish(imu_msg)
        rate.sleep()

if __name__ == '__main__':
    try:
    	pub_data()
    except rospy.ROSInterruptException:
    	pass
        
