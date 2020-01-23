import rospy
from sensor_msgs.msg import Imu

def callback(data):
	rospy.loginfo(rospy.get_caller_id(), data.data)

def listener():

	# anonymous=True allows rospy to randomly select a name
	# for our Subscriber so that multiple Subscribers can run
	# at the same time. If we end up using only one, we probably
	# don't need to enable this option
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber('imu_driver', Imu, callback)

	rospy.spin()

if __name__ == '__main__':
	listener()