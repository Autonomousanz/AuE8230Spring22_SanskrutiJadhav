#!/usr/bin/env python3

import rospy
import numpy as np
from sensor_msgs.msg import LaserScan
import sensor_msgs.msg

pub = rospy.Publisher('/revised_scan', LaserScan, queue_size = 10)
scann = LaserScan()

def callback(msg):
    #print(len(msg.ranges)) len is 2019 from 0-360
    current_time = rospy.Time.now()
    scann.header.stamp = current_time
    scann.header.frame_id = 'laser'
    scann.angle_min = -3.1415
    scann.angle_max = 3.1415
    scann.angle_increment = 0.00311202858575
    scann.time_increment = 4.99999987369e-05
    scann.range_min = 0.00999999977648
    scann.range_max = 32.0
    scann.ranges = msg.ranges
    scann.intensities = msg.intensities
    laser_range = np.array(scann.ranges)
    print(laser_range)
    pub.publish(scann)

def listener():
    rospy.init_node('revised_scan', anonymous=True)
    sub = rospy.Subscriber('/scan', LaserScan, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
