from geometry_msgs.msg import Twist
from rcl_interfaces.msg import SetParametersResult
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from turtlesim_msgs.msg import Pose


def validate_parameter(name: str, value: float) -> tuple[bool, str]:
    if name == 'linear_speed' and not (0.0 <= value <= 1.0):
        return False, 'linear_speed must be between 0.0 and 1.0'
    if name == 'turn_rate' and not (-1.0 <= value <= 1.0):
        return False, 'turn_rate must be between -1.0 and 1.0'
    if name == 'publish_hz' and not (1.0 <= value <= 30.0):
        return False, 'publish_hz must be between 1.0 and 30.0'
    return True, ''


def get_command(last_pose: Pose | None, linear_speed: float, turn_rate: float) -> Twist:
    msg = Twist()
    if last_pose is None:
        msg.linear.x = 0.0
        msg.angular.z = 0.0
    else:
        msg.linear.x = linear_speed
        msg.angular.z = turn_rate
    return msg


class PatrolNode(Node):

    def __init__(self):
        super().__init__('patrol')
        self.last_pose = None

        self.declare_parameter('linear_speed', 0.5)
        self.declare_parameter('turn_rate', 0.3)
        self.declare_parameter('publish_hz', 10.0)

        self.linear_speed = self.get_parameter('linear_speed').value
        self.turn_rate = self.get_parameter('turn_rate').value
        self.publish_hz = self.get_parameter('publish_hz').value

        self.pose_sub = self.create_subscription(
            Pose, '/turtle1/pose', self.pose_callback, 10
        )
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)

        self.timer = self.create_timer(1.0 / self.publish_hz, self.timer_callback)
        self.add_on_set_parameters_callback(self.parameter_callback)

        self.get_logger().info('Нода patrol запущена с параметрами по умолчанию.')

    def parameter_callback(self, params: list[Parameter]):
        for param in params:
            is_valid, reason = validate_parameter(param.name, param.value)
            if not is_valid:
                return SetParametersResult(successful=False, reason=reason)

            if param.name == 'publish_hz' and param.value != self.publish_hz:
                self.publish_hz = param.value
                self.destroy_timer(self.timer)
                self.timer = self.create_timer(1.0 / self.publish_hz, self.timer_callback)
                self.get_logger().info(f'Таймер пересоздан с частотой {self.publish_hz} Гц')
            else:
                setattr(self, param.name, param.value)

        return SetParametersResult(successful=True)

    def pose_callback(self, msg: Pose):
        self.last_pose = msg

    def timer_callback(self):
        cmd = get_command(self.last_pose, self.linear_speed, self.turn_rate)
        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = PatrolNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
