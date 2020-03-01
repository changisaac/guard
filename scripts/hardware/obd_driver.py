#!/usr/bin/env python2	
import rospy
import time
from guard.msg import obd_msg
from guard.msg import gps_msg

obd_msg_attr = ['vEgo', 'gas', 'gasPressed', 'brake', 'brakePressed', 'steeringAngle', 
				'steeringTorque', 'steeringPressed', 'gearShifter', 'steeringRate', 'aEgo', 
				'vEgoRaw', 'standstill', 'brakeLights',	'leftBlinker', 'rightBlinker', 
				'yawRate', 'genericToggle', 'doorOpen', 'seatbeltUnlatched', 'canValid',
				'steeringTorqueEps', 'clutchPressed']

gps_msg_attr = ['flags', 'latitude', 'longitude', 'altitude', 'speed', 'bearing', 'accuracy',
				'timestamp', 'verticalAccuracy', 'bearingAccuracy', 'speedAccuracy']


def package_data(data, msg_type, attr_list):
	dataIdx = 0

	for attr in attr_list:
		msg_attr = getattr(msg_type, attr)
		# print "ATTR: ", msg_attr
		# print "TYPE: ", type(msg_attr)
		# print "DATA: ", data[dataIdx]

		if isinstance(msg_attr, float):
			setattr(msg_type, attr, float(data[dataIdx]))
		elif isinstance(msg_attr, bool):
			setattr(msg_type, attr, bool(data[dataIdx]))
		elif isinstance(msg_attr, int):
			setattr(msg_type, attr, int(data[dataIdx]))
		dataIdx = dataIdx + 1

	return msg_type

def pub_data():
	obd_data_path = "/home/shared/catkin_ws/src/guard/scripts/hardware/test"
	rospy.init_node('imu_subscriber', anonymous=True)
	
	pub_obd = rospy.Publisher('/obd_driver', obd_msg)
	pub_gps = rospy.Publisher('/gps_driver', gps_msg, queue_size=10)

	i = 0
	rate = rospy.Rate(10) # 10hz
	while not rospy.is_shutdown():
		try:
			print "Data file is: " + obd_data_path
			with open(obd_data_path, 'r') as data_stream:
				for line in data_stream:
					# split data into a list
					obd_index = line.split(' ')[0:23]
					gps_index = line.split(' ')[23:34]

					obd_data = package_data(obd_index, obd_msg(), obd_msg_attr)
					gps_data = package_data(gps_index, gps_msg(), gps_msg_attr)

					print("LOGGING OBD INFO: ", i)
					rospy.loginfo(obd_data)

					print("LOGGING GPS INFO: ", i )					
					rospy.loginfo(gps_data)

					pub_obd.publish(obd_data)
					pub_gps.publish(gps_data) 
					i = i + 1

					rate.sleep()

		except IOError:
			print("File not accessible")

if __name__ == '__main__':
    try:
    	pub_data()
    except rospy.ROSInterruptException:
    	pass
        