#!/usr/bin/env python2	
import rospy
import time
from guard.msg import obd_msg
from guard.msg import gps_msg

def obdCb(data):
	print 'OBD DATA: ', data.vEgo
	rospy.loginfo("%s Test %d" % (data.vEgo, data.aEgo))

def gpsCb(data):
	print 'GPS DATA: ', data.flags
	rospy.loginfo("%s Test %d" % (data.flags, data.timestamp))

def listener():
	# anonymous=True allows rospy to randomly select a name
	# for our Subscriber so that multiple Subscribers can run
	# at the same time. If we end up using only one, we probably
	# don't need to enable this option
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber('/obd_driver', obd_msg, obdCb)
	rospy.Subscriber('/gps_driver', gps_msg, gpsCb)

	rospy.spin()

if __name__ == '__main__':
	listener()