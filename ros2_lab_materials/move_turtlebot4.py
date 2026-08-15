#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
import time

class MoveTurtlebot4(Node):
    def __init__(self):
        super().__init__('move_turtlebot4')
        self.publisher_ = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.run_robot()

    def run_robot(self):
        time.sleep(1.0)
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.twist.linear.x = 0.15
        self.publisher_.publish(msg)
        time.sleep(2.0)

        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = MoveTurtlebot4()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
