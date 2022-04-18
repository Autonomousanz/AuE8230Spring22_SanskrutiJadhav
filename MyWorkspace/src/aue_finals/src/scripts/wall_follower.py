#! /usr/bin/env python3

import rospy

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist 

pub = None

def LIDAR(msg):
    regions = {
        'Right': (min(msg.ranges[40:95])),
        'Forward':  min(min(msg.ranges[0:20]),min(msg.ranges[340:360])),
        'Left': min(msg.ranges[260:320]),

    }
    print('lidar')
    take_action(regions)
    
def take_action(regions):

   msg = Twist()

   linear_x = 0 
   angular_z = 0
   FL = 0.2
   FA = 0.46
   FA2 = -0.05
   
   
   if regions['Forward'] > 0.7:
       linear_x = regions['Forward']*FL
       angular_z = 0
       print('step1')


   if regions['Right'] <0.4 or regions['Left'] <0.4 or regions['Forward'] < 1.5:
        print('step3')

        if regions['Right'] < ((regions['Right'])+regions['Left']):
            angular_z = (regions['Right']-regions['Left'])*FA
            print('step4') 

   elif regions['Right'] <0.8 or regions['Left'] <0.8 or regions['Forward'] < 1.5:
        
        angular_z=angular_z = (regions['Right']-regions['Left'])*FA2
        print('step6')
   
   else:
        angular_z=0


   #elif regions['']


   msg.linear.x = linear_x
   msg.angular.z = angular_z
   pub.publish(msg)
   
def main():
    global pub
    rospy.init_node('obs')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    sub = rospy.Subscriber('/scan', LaserScan, LIDAR)
    rospy.spin()

if __name__ == '__main__':
    main()