#!/usr/bin/env python
   # license removed for brevity
import rospy
from std_msgs.msg import String
        
def talker():
    pub = rospy.Publisher('plutonode', String, queue_size=50)
    rospy.init_node('drone_command', anonymous=True)
   # rate = rospy.Rate(10) # 10hz
   # while not rospy.is_shutdown():
   #     hello_str = "hello world %s" % rospy.get_time()
   #     rospy.loginfo(hello_str)
    pub.publish("{rcRoll: 1500, rcPitch: 1500, rcYaw: 1500, rcThrottle: 1000, rcAUX1: 0, rcAUX2: 0, rcAUX3: 0, rcAUX4: 1500}")
   #    rate.sleep()
   
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass