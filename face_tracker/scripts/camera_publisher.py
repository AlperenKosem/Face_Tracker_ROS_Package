#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError 
#http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython
import os


def undistort(img):

	K   = np.array([[1.2696086139494651e+03, 0., 					9.1109389667924859e+02],
					[0., 					1.3272259861277089e+03, 4.2182521390545230e+02], 
					[0.,					0., 					1. ]])

	D   = np.array([-1.2825674964571737e-01, -1.2608237548114742e-02,
       				1.7289033019328565e-02, -3.5634233489559319e-04])

	h,w             = img.shape[:2]

	NewCameraMatrix, ROI = cv2.getOptimalNewCameraMatrix(K, D, (w,h), 1, (w,h))

	UndistortedImage     = cv2.undistort(img, K,D, None, NewCameraMatrix)

	return UndistortedImage

def cam():
	rospy.init_node('cam_ros', anonymous=True)

	bridge = CvBridge()
	source = 0 # 0 for webcam, 1 for usb camera 

	
	cap = cv2.VideoCapture(source)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
	camPublish = rospy.Publisher("/camera/image",Image, queue_size=10)
	rate=rospy.Rate(10)
	
	while not rospy.is_shutdown():
		ret, frame = cap.read()
		undistorted =undistort(frame)
		image_message = bridge.cv2_to_imgmsg(undistorted, "bgr8")    #64FC1--bgr8
		D          = Image()
		D.data     = image_message
		camPublish.publish(image_message)
		rate.sleep()

if __name__ == '__main__':
	cam()
