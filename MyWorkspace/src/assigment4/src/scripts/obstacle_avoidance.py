#!/usr/bin/env python3

from cmath import inf
from statistics import mean
import numpy as np
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import sensor_msgs.msg

class Obstacle():

       def __init__(self):
           self.section= {'front': 1,'left':1.5,'right': 1.4}
           self.Kp_linear= 0.5
           self.Kp_angular= 4
           self.threshold= 0.5
           self.error=10-self.threshold
      
       def callback(self,msg):

              pub = rospy.Publisher('/revised_scan', LaserScan, queue_size = 10)
              scann = LaserScan()
              scann.ranges=msg.ranges
              laser_range = np.array(scann.ranges)

              section = {
              'front': mean(laser_range[0:30]+laser_range[330:360]),
              'left': mean(laser_range[270:330]),
              'right': mean(laser_range[30:90])
              }
              self.section=section

              for keys, values in self.section.items():
                     if values>15:
                        section[keys]=10

       
              print(self.section)  

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

                     obstacle_direction = [keys for keys, values in self.section.items() if values==minval]  
                     #print(obstacle_direction)
                     #print(minval)
                     self.error = minval-self.threshold

                     if self.error > 0:
                            
                            #print(self.error)
                            vel_msg.linear.x = self.Kp_linear/(self.error+1)
                            #vel_msg.angular.z = self.Kp_angular*self.error
                            velocity_publisher.publish(vel_msg) 
                     else:
                            #find space opposite direction of obstacle direction and act 

                            if obstacle_direction == 'left':
                                   vel_msg.linear.x = self.Kp_linear/(self.error+1)
                                   vel_msg.angular.z = -self.Kp_angular*self.error#turn right
                                   velocity_publisher.publish(vel_msg) 
                            elif obstacle_direction == 'right':
                                   vel_msg.linear.x = self.Kp_linear/(self.error+1)
                                   vel_msg.angular.z = self.Kp_angular*self.error #turn left
                                   velocity_publisher.publish(vel_msg)
                            else :

                                   vel_msg.linear.x = self.Kp_linear/(self.error+1)
                                   vel_msg.angular.z = self.Kp_angular*self.error#turn right
                                   velocity_publisher.publish(vel_msg)


if __name__ == '__main__':
    
    mynode =Obstacle()
    mynode.listener()
   
  
