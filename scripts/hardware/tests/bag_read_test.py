import rosbag
import pdb

bag = rosbag.Bag("test.bag")
bag.reindex()

for topic, msg, t in bag.read_messages(topics=["/test_topic"]):
    print(topic, msg, t)

    bag.close()
