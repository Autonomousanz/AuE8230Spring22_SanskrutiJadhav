#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import sensor_msgs.msg

class Obstacle():

       def __init__(self):
           self.distances= 100

      
       def callback(self,msg):

              pub = rospy.Publisher('/revised_scan', LaserScan, queue_size = 10)
              scann = LaserScan()

              current_time = rospy.Time.now()
              scann.header.stamp = current_time
              scann.header.frame_id = 'laser'
              scann.angle_min = -3.1415
              scann.angle_max = 3.1415
              scann.angle_increment = 0.00311202858575
              scann.time_increment = 4.99999987369e-05
              scann.range_min = 0.00999999977648
              scann.range_max = 32.0
              scann.ranges = msg.ranges[0:72]
              scann.intensities = msg.intensities[0:72]
              distances= max(scann.ranges)
              self.distances=distances
              pub.publish(scann)
              print(distances)

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
                     if self.distances > 2:
                            vel_msg.linear.x = 0.5
                            vel_msg.linear.y = 0
                            vel_msg.linear.z = 0
                            vel_msg.angular.x = 0
                            vel_msg.angular.y = 0
                            vel_msg.angular.z = 0
                            velocity_publisher.publish(vel_msg)
                     else:
                            vel_msg.linear.x = 0
                            vel_msg.linear.y = 0
                            vel_msg.linear.z = 0
                            vel_msg.angular.x = 0
                            vel_msg.angular.y = 0
                            vel_msg.angular.z = 0
                            velocity_publisher.publish(vel_msg)

                     


if __name__ == '__main__':
    
    mynode =Obstacle()
    mynode.listener()
   
  
