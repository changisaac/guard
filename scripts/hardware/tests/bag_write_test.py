import rosbag
from std_msgs.msg import Int32

bag = rosbag.Bag("test.bag", "w")

num_msgs = 100
msgs = []

for i in range(num_msgs):
    i = Int32()
    i.data = 32
    msgs.append(i)

for i in range(num_msgs):
    bag.write("test_topic", msgs[i])

bag.close()
