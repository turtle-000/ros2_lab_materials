#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class SquareTurtle(Node):
    def __init__(self):
        super().__init__('square_turtle')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.run_square()

    def run_square(self):
        time.sleep(1.0)
        for _ in range(4):
            # 直進
            twist = Twist()
            twist.linear.x = 2.0
            self.publisher_.publish(twist)
            time.sleep(2.0)

            # 停止
            twist = Twist()
            self.publisher_.publish(twist)
            time.sleep(0.5)

            # 旋回
            twist.angular.z = 1.57
            self.publisher_.publish(twist)
            time.sleep(1.0)

            # 停止
            twist = Twist()
            self.publisher_.publish(twist)
            time.sleep(0.5)

def main(args=None):
    rclpy.init(args=args)
    node = SquareTurtle()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
