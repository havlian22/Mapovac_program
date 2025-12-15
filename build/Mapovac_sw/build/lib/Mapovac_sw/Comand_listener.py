import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist




class CommandListener(Node):
    def __init__(self):
        super().__init__('command_listener')
        self.subscription = self.create_subscription(
            Twist,
            '/robot_movement',
            self.command_callback,
            10)
        self.subscription
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)


    def command_callback(self, msg):
        self.get_logger().info(
            f"Received Twist - linear: x={msg.linear.x}, y={msg.linear.y}, z={msg.linear.z}, "
            f"angular: x={msg.angular.x}, y={msg.angular.y}, z={msg.angular.z}"
        )
        self.move_publish(msg.linear.x, msg.angular.z, msg.linear.y)


    def move_publish(self, lin_x, lin_y, ang_z):
        self.ride = Twist()

        #Linear
        self.ride.linear.x = 0.0 if round(lin_x + lin_y, 1) == 0.0 else 1.0 if round(lin_x + lin_y, 1) > 0.0 else -1.0
        self.ride.linear.y = math.atan2(lin_x, lin_y)
        self.ride.linear.z = 0.0
        #Axial
        self.ride.angular.x = 0.0
        self.ride.angular.y = 0.0
        self.ride.angular.z = ang_z

        self.publisher_.publish(self.ride)




def main(args=None):
    rclpy.init(args=args)
    node = CommandListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()