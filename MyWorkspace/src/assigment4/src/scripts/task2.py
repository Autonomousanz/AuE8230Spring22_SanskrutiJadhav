#!/usr/bin/env python3
import rospy
import numpy as np
from geometry_msgs.msg import Twist
import math
from sensor_msgs.msg import LaserScan

def callback(msg):

    range=msg.ranges
    pub= rospy.Publisher('/cmd_vel',Twist,queue_size=30)
    vel=Twist()
    k=0.3
    omega=0.1

    front=min(min(i for i in range[330:360] if i>0),min(i for i in range[0:30] if i>0))
    # fr=np.mean(range[30:70])
    # fl=np.mean(range[290:330])
    left=min(i for i in range[30:85] if i>0)
    right=min(i for i in range[275:330] if i>0)
    rmin=(right)*(-1)
    lmin=(left)
    if front==math.inf:
        front=3
    if rmin == -math.inf:
        rmin=-3
    if lmin == math.inf:
        lmin=3
    side=rmin+lmin

    

    print(front,side,lmin,rmin)  
    # or lmin<0.3 or rmin>-0.3: 
    if front<1:
        vel.linear.x=k*front*0.5
        vel.angular.z=omega*side*(1/(front))*8
        print('turn')
        print(vel)
 
    else:
        vel.linear.x=k*front
        vel.angular.z=omega*side*(10/(front))
        # vel.angular.z=0
        print('normal',vel)


    






    pub.publish(vel)   
    
def main():
    rospy.init_node('turtlebot3', anonymous=True)
    scan=rospy.Subscriber('/scan',LaserScan,callback)
    


if __name__ == '__main__':
    while not rospy.is_shutdown():
        try:
            main()

            rospy.spin()

        except rospy.ROSInterruptException: 
            pass
    
