#!/usr/bin/env python

# Sensor Data Fusion: Occupancy gridmap
# Authors: Lucila Patino Studencki / Nitin Saravana Kannan 
# 
# Gridmap Node

import rclpy
from rclpy.node import Node

import numpy as np

from nav_msgs.msg import OccupancyGrid


class Gridmap(Node):
       
    def __init__(self, size, resolution, topic_name, p_0, p_occ, p_free):
        super().__init__('my_g_map')
        print('Gridmap Node Initialized, It will publish an OccupancyGrid Message as topic:', topic_name)
    # Initialize grid map parameters
        self.size = size
        self.resolution = resolution

	# Calculate default log odds
        self.l_0 = self.prob2logOdds(p_0)
        self.l_occ = self.prob2logOdds(p_occ)
        self.l_free = self.prob2logOdds(p_free)
        self.log_odds = self.l_0 * np.ones((size, size))

    # Prepare Publisher
        self.topic_name = topic_name
        self.pub = self.create_publisher(OccupancyGrid, topic_name, 1)

    # create timer for callbacking publisher
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.publish_gridmap)                     

    # Transformation from probability to logOdds 
    def prob2logOdds(self, prob):
        # todo: calculation
        li_k = np.log(prob/(1-prob))
        return(li_k)
    
    # Transformation from logOdds to probabilities
    def logOdds2prob(self, log_o):
        # todo: calculation
        pi_k = 1 - (1/(1 + np.exp(log_o)))
        return(pi_k)

    #def update_cell(self, cell_x, cell_y, l_i):
    def update_logOdds(self, cell_x, cell_y, l_mi):
        # todo: calculation
        self.log_odds[cell_x, cell_y] = self.log_odds[cell_x, cell_y] + l_mi - self.l_0

    def publish_gridmap(self):

    # Filling OccupancyGrid Message for the topic
        msg = OccupancyGrid()
        msg.header.frame_id = "map"
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.info.resolution = self.resolution
        msg.info.width = self.size
        msg.info.height = self.size

        # Transform log_odds to probabilites and flatten array
        msg_data = self.logOdds2prob(self.log_odds).flatten('F')

    # Normalize and set to [0, 100]
        if (np.max(msg_data) != np.min(msg_data)) :
            msg_data -= np.min(msg_data)
            msg_data *= 100. / np.max(msg_data)
        else:
            msg_data *= 100 

        # assign -1 to nan-values
        msg_data[np.isnan(msg_data)] = -1

        # cast to int8
        msg.data = msg_data.astype(np.int8).tolist()

    # Publishing grid message
        self.pub.publish(msg)

# Testing the module
def test_gridmap_node_checkered(args = None):   

    rclpy.init(args=args)

    # Generate Gridmap object
    g_map = Gridmap(20, 0.2, "hsc_map", 0.5, 0.8, 0.2)
    # 20 size of grid map, 0.2 cell size individual, topic_name, p_0(first log odds), p_occ, p_free

    # Prepare Checkered Shape
    g_map.log_odds[1::2, :] = g_map.l_free
    g_map.log_odds[:, 1::2] = g_map.l_free
    g_map.initialized = True

    # Set ROS Node
    rclpy.spin(g_map)

    g_map.destroy_node()
    rclpy.shutdown()

if __name__ == '__test_gridmap_node_checkered__':
    test_gridmap_node_checkered()


#figure
def test_figure(args = None):
    
    rclpy.init(args=args)
    # Generate Gridmap object
    g_map = Gridmap(20, 0.2, "hsc_map", 0.5, 0.8, 0.2)
    # 20 size of grid map, 0.2 cell size individual, topic_name, p_0(first log odds), p_occ, p_free

    # Prepare S  Shape
    g_map.log_odds[2:4 ,2:18] = g_map.l_free
    g_map.log_odds[3:8,2:4] = g_map.l_free
    g_map.log_odds[8:10,2:18] = g_map.l_free
    g_map.log_odds[10:18,16:18] = g_map.l_free
    g_map.log_odds[16:18,2:18] = g_map.l_free



    # Set ROS Node
    rclpy.spin(g_map)

    g_map.destroy_node()
    rclpy.shutdown()

if __name__ == '__test_gridmap_node_checkered__':
    test_gridmap_node_checkered()