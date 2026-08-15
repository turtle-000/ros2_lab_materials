#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import LaserScan
from rclpy.qos import qos_profile_sensor_data

class ObstacleAvoidance(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance')
        self.cmd_pub = self.create_publisher(TwistStamped, '/cmd_vel', 1)
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            qos_profile_sensor_data
        )

    def scan_callback(self, msg: LaserScan):
        num_samples = len(msg.ranges)
        if num_samples == 0:
            return

        # 全方向の最接近物体を表示（0.8m 以下のみ）
        all_valid = [(r, i) for i, r in enumerate(msg.ranges) if msg.range_min < r < msg.range_max]
        if all_valid:
            min_dist_all, min_idx_all = min(all_valid)
            if min_dist_all < 0.8:
                self.get_logger().info(
                    f"【検知】最接近物体 ── 距離: {min_dist_all:.2f}m | インデックス: {min_idx_all} (全{num_samples}点中)"
                )

        # ★測定結果に基づき、正面インデックスを 200 に設定★
        front_idx = 200
        
        # 正面±30点（計60点：約60度分）のデータを取得
        front_ranges = msg.ranges[max(0, front_idx - 30) : min(num_samples, front_idx + 30)]
        valid_ranges = [r for r in front_ranges if msg.range_min < r < msg.range_max]
        
        twist_msg = TwistStamped()
        twist_msg.header.stamp = self.get_clock().now().to_msg()
        
        if valid_ranges:
            min_dist = min(valid_ranges)
            
            # 正面 0.6m 以内に障害物を検知した場合 -> 回避動作（右旋回）
            if min_dist < 0.6:
                self.get_logger().warn(
                    f"⚠️【回避動作】正面 {min_dist:.2f}m に障害物を検知！右旋回を開始します。"
                )
                twist_msg.twist.linear.x = 0.0
                twist_msg.twist.angular.z = -1.2  # 素早く右旋回
            else:
                twist_msg.twist.linear.x = 0.15
                twist_msg.twist.angular.z = 0.0
        else:
            twist_msg.twist.linear.x = 0.15
            twist_msg.twist.angular.z = 0.0

        self.cmd_pub.publish(twist_msg)

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidance()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        stop_msg = TwistStamped()
        stop_msg.header.stamp = node.get_clock().now().to_msg()
        node.cmd_pub.publish(stop_msg)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
