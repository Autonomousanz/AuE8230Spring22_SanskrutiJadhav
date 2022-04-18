#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from apriltag_ros.msg import AprilTagDetectionArray


class Apriltag():

    def __init__(self):
        
        #initializing the node
        rospy.init_node('Apriltag_ros',anonymous=True)
        self.x=0
        self.z=0
        self.vel_pub = rospy.Publisher('/cmd_vel',Twist,queue_size=10)          
        #publisher - velocity commands
        self.tag_sub = rospy.Subscriber('/tag_detections',AprilTagDetectionArray,self.position)    
        #subscriber -Apriltagdetection array callback function that stores the tag detection array coordinates in xyz world frame
        self.rate = rospy.Rate(10)
    
    def position(self,tag_array):

        self.x = tag_array.detections[0].pose.pose.pose.position.x
        self.z = tag_array.detections[0].pose.pose.pose.position.z

    def move(self):
            self.vel_msg = Twist()
               
            while not rospy.is_shutdown():
                    K_linear = 2
                    K_angular = 1
                    #PID control of the velocities of turtlebot 
                    self.vel_msg.linear.x =self.x*K_linear # Linear velocity
                    self.vel_msg.angular.z = self.z*K_angular #ANgular Velocity
                    self.vel_pub.publish(self.vel_msg)               
                    self.rate.sleep()
           
if __name__=='__main__':
        turtlebot = Apriltag()
        turtlebot.move()
    
