import rosbag
from cv_bridge import CvBridge 
import cv2

bag = rosbag.Bag("../guard_cam_1_rgb_image_1583219388214226007.bag")
bridge = CvBridge()

for topic, msg, t in bag.read_messages(topics=["/cam_1/color/image_raw"]):
    image = bridge.imgmsg_to_cv2(msg, "bgr8")
    cv2.imshow("Image Window", image)
    cv2.waitKey(50)

bag.close()
