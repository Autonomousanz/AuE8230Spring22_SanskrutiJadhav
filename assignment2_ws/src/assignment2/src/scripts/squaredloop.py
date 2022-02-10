#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
PI = 3.1415926535897

def move(vel_msg,velocity_publisher):
     
     distance=2
     vel_msg.linear.x = 0.2
     #Since we are moving just in x-axis
     vel_msg.linear.y = 0
     vel_msg.linear.z = 0
     vel_msg.angular.x = 0
     vel_msg.angular.y = 0
     vel_msg.angular.z = 0
     #Setting the current time for distance calculus
     t0 = rospy.Time.now().to_sec()
     current_distance = 0
     while(current_distance < distance):
               #Publish the velocity
               velocity_publisher.publish(vel_msg)
               #Takes actual time to velocity calculus
               t1=rospy.Time.now().to_sec()
               #Calculates distancePoseStamped
               current_distance= 0.2*(t1-t0)
     #After the loop, stops the robot
     vel_msg.linear.x = 0
     #Force the robot to stop
     velocity_publisher.publish(vel_msg)
           
          
           
def rotate(vel_msg,velocity_publisher):

     print(" rotate robot")  
     #We wont use linear components
     vel_msg.linear.x = 0
     vel_msg.linear.y = 0
     vel_msg.linear.z = 0
     vel_msg.angular.x = 0
     vel_msg.angular.y = 0
     
     angular_speed = 0.2
     relative_angle = PI/2
     
     vel_msg.angular.z = abs(float(angular_speed))
     
     # Setting the current time for distance calculus
     t0 = rospy.Time.now().to_sec()
     current_angle=0.00
     while(current_angle < relative_angle):
         velocity_publisher.publish(vel_msg)
         t1 = rospy.Time.now().to_sec()
         current_angle = angular_speed*(t1-t0)
     #Forcing our robot to stop
     vel_msg.angular.z = 0
     velocity_publisher.publish(vel_msg)
def square():
        # Starts a new node
        rospy.init_node('square_closedloop', anonymous=True)
        velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        vel_msg = Twist()
        #Receiveing the user's input
        print("Let's move your robot")
        side=0
        while side<4:
           move(vel_msg,velocity_publisher)
           rotate(vel_msg,velocity_publisher)
           side+=1 
        rospy.spin()           
   
if __name__ == '__main__':
   
    
    try:
          #Testing our function
          square()
                       
    except rospy.ROSInterruptException: pass


