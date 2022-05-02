#!/usr/bin/env python
# license removed for brevity

import rospy
from std_msgs.msg import Char, Int64

from Test_python.msg import plutomsg

import sys, select, termios, tty



if __name__ == '__main__':
    
    rospy.init_node('drone_command_145507_1650217054908', anonymous=True)
    rospy.topics
    pub = rospy.Publisher('pluto_msg', plutomsg, queue_size=10)
   # rate = rospy.Rate(10) # 10hz
   # while not rospy.is_shutdown():
   #     hello_str = "hello world %s" % rospy.get_time()
   #     rospy.loginfo(hello_str)

 
    msg=plutomsg()

    msg.rcRoll=1500
    msg.rcPitch=1500
    msg.rcYaw=1500
    msg.rcThrottle=1000
    msg.rcAUX1=0
    msg.rcAUX2=0
    msg.rcAUX3=0
    msg.rcAUX4=1500

    rospy.loginfo(msg)
    pub.publish(msg)
   #    rate.sleep()
   
"""
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
      """