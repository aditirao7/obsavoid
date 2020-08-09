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
    
    
 def align(angle): 
	flag=0
	while 1:
		if flag==0:
			time.sleep(0.1)
			final_yaw = yaw + angle
			if final_yaw<0:
				final_yaw=360+final_yaw
        		if final_yaw>360:
				final_yaw=final_yaw%360
			flag=1
			print(yaw, final_yaw, angle)
		angle_diff = yaw-final_yaw
		if angle_diff<1 and angle_diff>-1: 
				stop()
				break
		if angle>0:
			twist.angular.z = -1
			pub.publish(twist)
		elif angle<0:
			twist.angular.z = 1
			pub.publish(twist)

## NODE INTITIALIZATION

rospy.init_node('scan_msg', disable_signals=True)

rospy.Subscriber("/imu", Imu, callback3)

pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)

speed = Twist()
r = rospy.Rate(100)

align(45)

