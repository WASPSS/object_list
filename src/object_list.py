#!/usr/bin/env python
import rospy
import numpy as np
from wasp_custom_msgs.msg import object_loc
from math import floor

april_tags = []
objects2d = []
objects3d = []

def floor_to_dec(value):
    return floor(value*10)/10

def exist_on_2d_map(object, object_list):
    for i in range(len(object_list)):
        if object.ID == object_list[i]:
            return True
    return False

def exist_on_3d_map(object, object_list):
    for i in range(len(object_list)):
        if object.ID == object_list[i][0]:
            if (floor_to_dec(object.point.x) == floor_to_dec(object_list[i][1])) and (floor_to_dec(object.point.y) == floor_to_dec(object_list[i][2])):
                return True
    return False


def new_obj_cb(data):
    global april_tags, objects2d, objects3d
    exist = False
    if (data.ID < 100):
        if not(exist_on_2d_map(data, april_tags)):
            april_tags.append(data.ID)
            print april_tags
    elif (data.ID < 200):
        if not(exist_on_2d_map(data, objects2d)):
            objects2d.append(data.ID)
            print objects2d
    else:
        if not(exist_on_3d_map(data, objects3d)):
            objects3d.append([data.ID, data.point.x, data.point.y])
            print objects3d


# Intializes everything
def start():
    global cmd_pub, twist_cmd, linear_cmd, angular_cmd
    # publishing to "turtle1/cmd_vel" to control
    rospy.init_node('object_list')
    # subscribed to joystick inputs on topic "joy"
    rospy.Subscriber("/object_location", object_loc , new_obj_cb)
    rospy.spin()



if __name__ == '__main__':
    try:
        start()
    except rospy.ROSInterruptException:
        pass
