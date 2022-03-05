#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist


def turtle_circles(radius,velocity):
    rospy.init_node('circle',anonymous=True)
    pub= rospy.Publisher('/cmd_vel',Twist,queue_size=10)
    rate=rospy.Rate(10)
    vel=Twist()
    while not rospy.is_shutdown():
        vel.linear.x = float(velocity)
        vel.linear.y =0 
        vel.linear.z =0 

        vel.angular.x=0
        vel.angular.y=0
        vel.angular.z= float(velocity)/float(radius)

        rospy.loginfo(f"Radius is {radius}")
        pub.publish(vel)
        rate.sleep()
    rospy.on_shutdown(myhook(vel,pub))

def myhook(vel,pub):
    print ("shutdown time!")
    vel.linear.x=0
    vel.linear.y =0 
    vel.linear.z =0 

    vel.angular.x=0
    vel.angular.y=0
    vel.angular.z= 0
    pub.publish(vel)
      




if __name__ == '__main__':
    try:
        
        turtle_circles(2.0,0.20)
    except rospy.ROSInterruptException:
        pass
