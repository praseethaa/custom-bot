#!/usr/bin/env python

import rospy 
import numpy as np 
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist 


def callback(data):
    laser_data = np.array(data.ranges)
    laser_data = laser_data[~np.isinf(laser_data)]

    print(max(laser_data))

    if max(laser_data) < 0.6 and max(laser_data) >0.22:
        take_turn()
        move_forward()
        laser_data=1
    elif max(laser_data) < 0.22 :
        move_forward()
        laser_data=0.5
    else:
        move_forward()
    move_forward()

def move_forward():
    twist = Twist()
    twist.linear.x = 0.1 
    pub.publish(twist)
    print("moving forward")

def take_turn():
    twist = Twist()
    twist.angular.z = 1.57/2 # degree 180 / pi(90)
    r = rospy.Rate(5.0)
    for i in range(0,10):
        pub.publish(twist)
        r.sleep()

def main():
    sub = rospy.Subscriber("/scan", LaserScan, callback)
    rospy.spin()

rospy.init_node("Avoider")
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)

if __name__ == '__main__':
    main()
