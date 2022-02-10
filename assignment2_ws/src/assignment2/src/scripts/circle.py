#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

def circle():

     # Starts a new node
     rospy.init_node('circle', anonymous=True)
     velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
     vel_msg = Twist()
     
     #Receiveing the user's input
     print("Let's move your robot")
     vel_msg.linear.x = 2    
     vel_msg.linear.y = 0
     vel_msg.linear.z = 0
     vel_msg.angular.x = 0
     vel_msg.angular.y = 0
     vel_msg.angular.z = -1.8
     while not rospy.is_shutdown():
       velocity_publisher.publish(vel_msg)
   
if __name__ == '__main__':
      try:
           #Testing our function
           circle()
      except rospy.ROSInterruptException: pass

