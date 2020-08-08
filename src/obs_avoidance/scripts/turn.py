#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Point, Twist
from sensor_msgs.msg import LaserScan, Imu, NavSatFix, Range
from tf.transformations import euler_from_quaternion
from pyproj import Geod
import numpy as np
import math
import time

yaw =0 
flag = 0
##CALLBACK


def callback3(pose):
    global yaw
    quaternion = (pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w)

    euler = euler_from_quaternion(quaternion)
    yaw= math.degrees(euler[2]) +180
    yaw = abs(yaw-360)
    yaw = yaw%360

## NODE INTITIALIZATION

rospy.init_node('scan_msg', disable_signals=True)

rospy.Subscriber("/imu", Imu, callback3)

pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)

speed = Twist()
r = rospy.Rate(100)

while not rospy.is_shutdown():
    
    if flag == 0:
        ## to get a constant initial yaw
        time.sleep(1)
        initial = yaw
        flag=1 
    ## initial yaw - 45 is goal for now... you can change this
    goal = initial - 45

    #our changing yaw - goal is 45 degree... it'll be -45 degree depending on the goal values

    ## If statements are same more or less... 
    angle_diff = yaw - goal
    print(angle_diff)
    if angle_diff<5 :
        speed.linear.x = 0
        speed.angular.z = 0
        pub.publish(speed)
    
    if angle_diff>1:
            speed.angular.z = +0.4
    #        print("aligning right")
            pub.publish(speed)
    
    elif angle_diff<-45:
            speed.angular.z = +0.4
     #       print("aligning left")

            pub.publish(speed)
    
    r.sleep()

