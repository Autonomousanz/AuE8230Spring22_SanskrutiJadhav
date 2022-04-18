#!/usr/bin/env python3

from statistics import mean
import math
import numpy as np
import rospy
from geometry_msgs.msg import Twist
import sensor_msgs.msg
from sensor_msgs.msg import LaserScan

class Obstacle():

        def __init__(self):
           self.section= {'left':3,'front':7,'right':6 }
           self.Kp_linear=0.1
           self.Kp_angular=1
           self.threshold=1
           self.error=3

        def callback(self,msg):

                    pub = rospy.Publisher('/revised_scan', LaserScan, queue_size = 10)
                    scann = LaserScan()

                    scann.ranges = msg.ranges
                    laser_range = np.array(scann.ranges)
                    # print(laser_range)
                    section = {
                    'left': min(laser_range[30:90]),
                    'front': min(laser_range[0:30]+laser_range[330:360]),
                    'right': min(laser_range[270:330])
                    }

                    for keys, values in section.items() :
                        if values==math.inf:
                            section[keys]=1
  
                    self.section=section
                    # print(self.section.values())
                    pub.publish(scann)

        def listener(self):
            #starts a new node 
            rospy.init_node('turtlebot3', anonymous=True)
            scan=rospy.Subscriber('/scan',LaserScan,self.callback)
            self.move()
            rospy.spin()

        def move(self):
                #starts a new node 
                
                velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
                vel_msg = Twist()

                
                while not rospy.is_shutdown():

                        print(vel_msg)

                        if self.section['left'] > self.section['right'] :
                            farthest_obstacle_direction='left'

                        else:
                            farthest_obstacle_direction='right'

                        self.error = self.section['front']-self.threshold
                        print(self.error)
                        if abs(self.error) > 0.2: #1.2#removed abs
                            print('front')
                            vel_msg.linear.x = self.Kp_linear*(self.error)
                            vel_msg.angular.z= 0
                            velocity_publisher.publish(vel_msg)
                            
                        elif farthest_obstacle_direction=='left':
                                    print('left')
                                    vel_msg.linear.x = self.Kp_linear*(self.error)
                                    vel_msg.angular.z = self.Kp_angular*self.error*2
                                    velocity_publisher.publish(vel_msg)
                        elif farthest_obstacle_direction=='right':
                                    print('right')
                                    vel_msg.linear.x = self.Kp_linear*self.error
                                    vel_msg.angular.z = -self.Kp_angular*self.error*2
                                    velocity_publisher.publish(vel_msg)





if __name__ == '__main__':
    
    mynode =Obstacle()
    mynode.listener()


  


    