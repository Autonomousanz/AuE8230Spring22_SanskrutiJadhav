#!/usr/bin/env python3
import rospy
import math
import time
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
PI = 3.1415926535897
x=0
y=0
yaw=0          
def rotate(angular_speed,relative_angle,vel_msg,velocity_publisher,clockwise):
 
     #We wont use linear components
     vel_msg.linear.x = 0
     vel_msg.linear.y = 0
     vel_msg.linear.z = 0
     vel_msg.angular.x = 0
     vel_msg.angular.y = 0
     
      # Checking if our movement is CW or CC
     if clockwise:
        vel_msg.angular.z = -abs(float(angular_speed))
        
     else:
        vel_msg.angular.z = abs(float(angular_speed))
      
     velocity_publisher.publish(vel_msg)
     loop_rate = rospy.Rate(5)  
     # Setting the current time for distance calculus
     t0 = rospy.Time.now().to_sec()
     
     while(True):
         velocity_publisher.publish(vel_msg)
         t1 = rospy.Time.now().to_sec()
         current_angle = angular_speed*(t1-t0)
         
         if  (current_angle>relative_angle):
            rospy.loginfo("reached")
            break        
       
     #Forcing our robot to stop
     vel_msg.linear.x = 0
     vel_msg.angular.z = 0
     velocity_publisher.publish(vel_msg)
      
     
def poseCallback(pose_message):
    global x
    global y, yaw
    x= pose_message.x
    y= pose_message.y
    yaw = pose_message.theta
    print ('x = {}'.format(pose_message.x))
    print ('y = {}'.format(pose_message.y))
    print ('yaw = {}'.format(pose_message.theta))

def gotogoal(x_goal, y_goal,vel_msg,velocity_publisher):
   

    while (True):
        K_linear = 0.7 
        distance = (math.sqrt(((x_goal-x) ** 2) + ((y_goal-y) ** 2)))
        linear_speed = distance * K_linear
        K_angular = 10.5
        desired_angle_goal = math.atan2(y_goal-y, x_goal-x)
        angular_speed = (desired_angle_goal-yaw)*K_angular

        vel_msg.linear.x = linear_speed

        vel_msg.angular.z = angular_speed

        velocity_publisher.publish(vel_msg)
        
        if (distance <0.01):
            break  
            
          
def direction(desired_angle):
    
    global yaw
    relative_angle = desired_angle - yaw
    if relative_angle < 0:
        clockwise = 1
    else:
        clockwise = 0
    
    rotate(0.5,(abs(relative_angle)),vel_msg,velocity_publisher,clockwise)
    
              
def square(vel_msg,velocity_publisher,pose_message,pose_subscriber):
             
        gotogoal(5,5,vel_msg,velocity_publisher)
        direction(math.radians(0))
        gotogoal(8,5,vel_msg,velocity_publisher)
        direction(math.radians(90))
        gotogoal(8,8,vel_msg,velocity_publisher)
        direction(math.radians(180))
        gotogoal(5,8,vel_msg,velocity_publisher)
        direction(math.radians(270))
        gotogoal(5,5,vel_msg,velocity_publisher)
        print("Let's move your robot")
     
        rospy.spin()           
           
if __name__ == '__main__':
    # Starts a new node
       rospy.init_node('square_closedloop', anonymous=True)
       
       velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
       vel_msg = Twist()
      
       
       pose_subscriber = rospy.Subscriber("/turtle1/pose", Pose, poseCallback)
       pose_message=Pose()
       
    
       #Receiveing the user's input
       print("Let's move your robot")
  
       try:
           #Testing our function
           
             square(vel_msg,velocity_publisher,pose_message,pose_subscriber)
         
       except rospy.ROSInterruptException: pass


