#!/usr/bin/env python

import rospy
import cv2
import roslib
import time
import numpy as np
from std_msgs.msg import String, Char, Int16
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import sys, select, termios, tty

bridge = CvBridge()

width, height = 480, 360

sensors = 5  #Number of senors(Hypothetical)
threshold = 0.1 #Sensitivity of Color detection
Kernel_size=15


"""
msg_pub=0
keyboard_control={  #dictionary containing the key pressed abd value associated with it
                      '[A': 10,
                      '[D': 30,
                      '[C': 40,
                      'w':50,
                      's':60,
                      ' ': 70,
                      'r':80,
                      't':90,
                      'p':100,
                      '[B':110,
                      'n':120,
                      'q':130,
                      'e':140,
                      'a':150,
                      'd':160,
                      '+' : 15,
                      '1' : 25,
                      '2' : 30,
                      '3' : 35,
                      '4' : 45}
"""




def image_callback(ros_image):
  global bridge
  #convert ros_image into an opencv-compatible image
  try:
    img = bridge.imgmsg_to_cv2(ros_image, "bgr8")
  except CvBridgeError as e:
      print(e)

  def thresholding( img ):                                       #Creates an HSV mask over the live feed
	  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	  blurred = cv2.GaussianBlur(img, (Kernel_size, Kernel_size), 0)
	  hsv = cv2.cvtColor( blurred, cv2.COLOR_BGR2GRAY )
	  ret, thresh1 = cv2.threshold(hsv, 120, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)   
	  return thresh1

  def getContours( imgThres, img ):                             #Forms a contour around the largest visible(White) patch
	  contours, heirarchy = cv2.findContours( imgThres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE )
	  biggest = max( contours, key=cv2.contourArea )
	  x, y, w, h = cv2.boundingRect( biggest )
	  cx = x + w // 2
	  cy = y + h // 2
	  cv2.drawContours( img, biggest, -1, (255, 255, 0), 5 )
	  cv2.circle( img, (cx, cy), 5, (0, 128, 255), cv2.FILLED )

  
  def droneOutput(senOut):                                      #Gives Commands to drone
	  #global msg_pub, keyboard_control
	  if senOut==[0,1,1,1,0] or senOut==[0,0,1,0,0]:
		  
		  #msg_pub=keyboard_control['w']         # Increase Altitude Key
		  #pub.publish(msg_pub)

		  return 'Move Upward'
	  if senOut==[0,1,1,1,1] :
	  	  return  'Move Slight Right'
	  if senOut==[1,1,1,1,0] :
		  return  'Move Sligth Left'
	  if senOut==[1,1,1,0,0] :
		  return  'Move Left'
	  if senOut==[0,0,1,1,1] :
		  return  'Move Right'
	  if senOut==[0,0,0,1,1] :
		  return  'Rotate Right'
	  if senOut==[1,1,0,0,0] :
		  return  'Rotate Left'
	  else :
		 # msg_pub=keyboard_control['e']         # Increase Altitude Key
		#  pub.publish(msg_pub)
		  return 'Stop'
	  ## Translation Error
	  ## lr = (cx - width // 2) // sensitivity   ## lr is left-right error from center
	  ## lr = int(np.clip(lr, -10, 10))    ## cliping the value of lr between -10 and 10
	  ## if 2 > lr and lr > -2 : lr = 0

  def getSensorOutput( imgThres, sensor ):                      #Senses the position of the drone along the path
	  imgs = np.hsplit( imgThres, sensor )
	  totalPixels = (img.shape[1] // sensor) * img.shape[0]
	  senOut = []
	  for x, im in enumerate( imgs ):
		  pixelCount = cv2.countNonZero( im )
		  if pixelCount > threshold * totalPixels:
			  senOut.append( 1 )
		  else:
			  senOut.append( 0 )
		  cv2.imshow( str( x ), im )
	  print( senOut )
	  return senOut

  img = cv2.resize( img, (width, height) )
  #img = cv2.flip( img, 1 )
  imgThres = thresholding( img )
  cx = getContours( imgThres, img )  # Translation
  senOut = getSensorOutput( imgThres, sensors )
  cv2.imshow( "Output", img )
  cv2.imshow( "Path", imgThres )
  print(droneOutput(senOut))
  cv2.waitKey( 10 )


def main(args):
  rospy.init_node('image_converter', anonymous=True) 
  image_sub = rospy.Subscriber("/plutocamera/image_raw",Image, image_callback)
  
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
	
	main(sys.argv)

	#rospy.init_node('simple_drone_teleop_key', anonymous=True)
"""	pub = rospy.Publisher('/input_key', Int16, queue_size=1)
	settings = termios.tcgetattr(sys.stdin)

	msg_pub=keyboard_control[' ']         #Arming Key
	pub.publish(msg_pub)
	time.sleep(1)
	msg_pub=keyboard_control['q']         #Take-off Key
	pub.publish(msg_pub)
	time.sleep(1)
	msg_pub=keyboard_control['w']         # Increase Altitude Key
	pub.publish(msg_pub)
	time.sleep(3)
	main(sys.argv)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	"""