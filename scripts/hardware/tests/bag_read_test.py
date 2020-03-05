import rosbag
from cv_bridge import CvBridge 
import cv2

bag_1 = rosbag.Bag("../guard_log_1583370581677942037/cam_2_rgb_image_1583370941403935909.bag")
#bag_2 = rosbag.Bag("../guard_cam_2_rgb_image_1583219388231663942.bag")

bridge = CvBridge()
i = 0

for topic, msg, t in bag_1.read_messages(topics=["/cam_2/color/image_raw"]):
    image = bridge.imgmsg_to_cv2(msg, "bgr8")
    cv2.imwrite("out/"+str(i)+".jpg", image)
    i+=1
    #cv2.imshow("Image Window 1", image)
    #cv2.waitKey(70)

#for topic, msg, t in bag_2.read_messages(topics=["/cam_2/color/image_raw"]):
#    image = bridge.imgmsg_to_cv2(msg, "bgr8")
#    cv2.imshow("Image Window 2", image)
#    cv2.waitKey(50)

bag_1.close()
#bag_2.close()
