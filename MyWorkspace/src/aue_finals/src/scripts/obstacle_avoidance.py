#!/usr/bin/env python3

from statistics import mean
import numpy as np
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import sensor_msgs.msg

class Obstacle():

       def __init__(self):
           self.section= {'left':5,'front':1,'right':3 }
           self.Kp_linear= 0.3
           self.Kp_angular= 0.05
           self.threshold= 1
           self.distance=10
           self.error=-9


      
       def callback(self,msg):

              pub = rospy.Publisher('/revised_scan', LaserScan, queue_size = 10)
              scann = LaserScan()

              scann.ranges = msg.ranges
              laser_range = np.array(scann.ranges)
              section = {
              'left': min(laser_range[30:90]),
              'front': min(laser_range[0:30]+laser_range[330:360]),
              'right': min(laser_range[270:330])
              }
              self.section=section
              # print(self.section)
              pub.publish(scann)


       def listener(self):
              rospy.init_node('robot_move', anonymous=True)
              sub = rospy.Subscriber('/scan', LaserScan, self.callback)
              self.move()
              rospy.spin()


       def move(self):
              #starts a new node 
              
              velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
              vel_msg = Twist()

              
              while not rospy.is_shutdown():

                     minval = min(self.section.values())
                     print(minval)
                     obstacle_direction = [keys for keys, values in self.section.items() if values<=minval]  
                     print(obstacle_direction)

                     self.error = self.threshold-minval

                     if (self.error) > 0.2:
                            
                            vel_msg.linear.x = 0.2
                            vel_msg.angular.z=0
                  
                            velocity_publisher.publish(vel_msg) 
                     else:
                            if obstacle_direction == 'left':
                                   vel_msg.linear.x = self.Kp_linear*self.error
                                   vel_msg.angular.z = -self.Kp_angular*self.error
                                   velocity_publisher.publish(vel_msg) 
                            elif obstacle_direction == 'right':
                                   vel_msg.linear.x = self.Kp_linear*self.error
                                   vel_msg.angular.z = self.Kp_angular*self.error
                                   velocity_publisher.publish(vel_msg)
                            else :
                                   
                                   maxval = max(self.section.values())

                                   farthest_obstacle_direction = [keys for keys, values in self.section.items() if values==maxval]
                                   
                                   if farthest_obstacle_direction=='left':
                                         
                                          vel_msg.linear.x = 0
                                          vel_msg.angular.z = self.Kp_angular*self.error
                                          velocity_publisher.publish(vel_msg)
                                   else:
                                          
                                          vel_msg.linear.x = 0
                                          vel_msg.angular.z = -self.Kp_angular*self.error
                                          velocity_publisher.publish(vel_msg)


if __name__ == '__main__':
    
    mynode =Obstacle()
    mynode.listener()
   
  
