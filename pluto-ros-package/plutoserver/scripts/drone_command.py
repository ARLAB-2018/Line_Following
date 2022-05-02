#!/usr/bin/env python
# license removed for brevity

import rospy
import roslib
import time
from std_msgs.msg import Char, Int16

#from Test_python.msg import plutomsg

import sys, select, termios, tty




if __name__ == '__main__':
    
    rospy.init_node('simple_drone_teleop_key', anonymous=True)
    pub = rospy.Publisher('/input_key', Int16, queue_size=1)
    settings = termios.tcgetattr(sys.stdin)
   # rate = rospy.Rate(10) # 10hz
   # while not rospy.is_shutdown():
   #     hello_str = "hello world %s" % rospy.get_time()
   #     rospy.loginfo(hello_str)

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

    while not rospy.is_shutdown():
        msg_pub=keyboard_control[' ']         #Arming Key
        pub.publish(msg_pub)
        time.sleep(1)
        msg_pub=keyboard_control['q']         #Take-off Key
        pub.publish(msg_pub)
        time.sleep(1)
        msg_pub=keyboard_control['w']         # Increase Altitude Key
        pub.publish(msg_pub)
        time.sleep(2)
        msg_pub=keyboard_control['d']         # Decrease Altitude Key
        pub.publish(msg_pub)
        time.sleep(3)
        msg_pub=keyboard_control['[A']         # Increase Altitude Key
        pub.publish(msg_pub)
        time.sleep(2)
        msg_pub=keyboard_control['[B']         # Increase Altitude Key
        pub.publish(msg_pub)
        time.sleep(2)
        msg_pub=keyboard_control['e']
        pub.publish(msg_pub)
        time.sleep(5)
    #msg_pub=keyboard_control['q']
    #pub.publish(msg_pub)
    #time.sleep(5)
        #break
    
    
   # print (key)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
   #    rate.sleep()
    
   
"""
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
      """