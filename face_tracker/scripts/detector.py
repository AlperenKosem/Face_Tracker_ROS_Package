#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Int16, Bool
import os
import time



class servo_controller(object) :
	def __init__(self):
		self.error = 0
		self.object_x = 0
		self.reference_x = 0
		self.servo_input = 90
		
		
		rospy.Subscriber("/camera/image", Image, self.imageCallback)
		

		
		
	def imageCallback(self, data):
		print "callback"
		bridge = CvBridge()
		self.cv_image = bridge.imgmsg_to_cv2(data, "8UC3")
		
		#cv2.imshow("image", cv_image)
		#cv2.waitKey(1)
		#return cv_image
		


	def blue_detector(self,img):
		
		rows, cols, _ = img.shape
		x_center = int(cols / 2)

		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		# define range of blue color in HSV

		lower_blue = np.array([110,50,50])
		upper_blue = np.array([130,255,255])
		
		lower_blue = np.array([161, 155, 84])
		upper_blue = np.array([179, 255, 255])

		# Threshold the HSV image to get only blue colors
		mask = cv2.inRange(hsv, lower_blue, upper_blue)
		
		# Bitwise-AND mask and original image
		res = cv2.bitwise_and(img,img, mask= mask)
		x_medium = 0
		_ , contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
		for cnt in contours:
			(x, y, w, h) = cv2.boundingRect(cnt)
			cv2.rectangle(img, (x,y) , (x + w, y + h), (0,255,0), 2 )
			x_medium = int((x + x + w) / 2) #object location.x
			break
		
		
		
		cv2.line(img, (x_medium, 0), (x_medium, 1080), (0, 255, 0), 2)
		cv2.imshow('frame',img)
		cv2.waitKey(1)
		
		
		return x_medium , x_center, img
		

	def face_detector(self, img) :

		rows, cols, _ = img.shape
		x_center = int(cols / 2)
		x_medium = x_center

		dirname = os.path.dirname(__file__)
		filename = os.path.join(dirname, 'haarcascade_frontalface.xml')

		face_cascade = cv2.CascadeClassifier(filename)

		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		
		# Detect faces
		faces = face_cascade.detectMultiScale(gray, 1.1, 8)
	#
		for (x, y, w, h) in faces:
			cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)
			x_medium = int((x + x + w) / 2)

		return x_medium , x_center, img


	def controller(self):
		

		rospy.wait_for_message('/camera/image',Image)
				
		print "servo_controller"
		


		rate = rospy.Rate(10) # 10 hz

		error_publisher = rospy.Publisher("/servo_controller", Int16, queue_size = 10)
		
		while not rospy.is_shutdown():

			self.object_x , self.reference_x, debug_image = self.face_detector(self.cv_image)
			
			#cv2.imshow("image", cv2.resize(debug_image,(640,420)))
			#cv2.waitKey(1)

			if self.object_x < self.reference_x - 150:
				self.servo_input += 2
			elif self.object_x > self.reference_x + 150:
				self.servo_input -= 2

			if self.servo_input >= 180 :
				self.servo_input = 180
			elif self.servo_input <= 0 :
				self.servo_input = 0
			
			error_publisher.publish(servo_controller.servo_input)
		
			
			rate.sleep()
		
	
if __name__ == '__main__':
	rospy.init_node('face_detector', anonymous=True)
	servo_controller = servo_controller()
	servo_controller.controller()

	
