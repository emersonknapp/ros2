import rclpy
# from rclpy.duration import Duration
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
# from rclpy.qos import QoSLivelinessPolicy
from rclpy.qos import QoSProfile
from rclpy.qos_event import PublisherEventCallbacks
from rclpy.qos_event import SubscriptionEventCallbacks

from std_msgs.msg import String


class Talker(Node):
    def __init__(self):
        super().__init__('Talker')
        qos = QoSProfile(
            # lifespan=Duration(seconds=0),
            # deadline=Duration(seconds=0),
            # liveliness=QoSLivelinessPolicy.RMW_QOS_POLICY_LIVELINESS_AUTOMATIC,
            # liveliness_lease_duration=Duration(seconds=2),
        )
        self.publisher = self.create_publisher(
            String, 'topic', qos_profile=qos,
            event_callbacks=PublisherEventCallbacks(
                # deadline=self.dead_cb,
                # liveliness=self.live_cb
            ))
        self.count = 0

        self.timer = self.create_timer(0.6, self.timer_cb)

    def fini(self):
        # Destroy the timer attached to the node explicitly
        # (optional - otherwise it will be done automatically
        # when the garbage collector destroys the node object)
        self.get_logger().info('Shutting down')
        self.destroy_timer(self.timer)
        self.get_logger().info('Destroyed timer')
        self.destroy_node()
        self.get_logger().info('Destroyed node')

    def timer_cb(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.count
        self.count += 1
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.publisher.publish(msg)

    def dead_cb(self, evt):
        self.get_logger().info('DEADLINE missed: "{}"'.format(evt))

    def live_cb(self, evt):
        self.get_logger().info('LIVELINESS failed: "{}"'.format(evt))


class Listener(Node):
    def __init__(self, name):
        super().__init__(name)
        self.subscription = self.create_subscription(
            String, 'topic', self.msg_cb,
            event_callbacks=SubscriptionEventCallbacks(
                deadline=self.dead_cb,
                liveliness=self.live_cb,
            ))

    def msg_cb(self, msg):
        self.get_logger().info('Heard: "%s"' % msg.data)

    def dead_cb(self, evt):
        self.get_logger().info('DEADLINE missed: "{}"'.format(evt))

    def live_cb(self, evt):
        self.get_logger().info('LIVELINESS changed: "{}"'.format(evt))


def main(args=None):
    rclpy.init(args=args)

    executor = SingleThreadedExecutor()

    talker = Talker()
    listener = Listener('Listen1')
    listener2 = Listener('Listen2')

    def killa():
        executor.remove_node(talker)
        talker.fini()

    killswitch = talker.create_timer(4.0, killa)  # NOQA

    executor.add_node(talker)
    executor.add_node(listener)
    executor.add_node(listener2)

    executor.spin()

    talker.fini()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
