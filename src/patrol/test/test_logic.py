import unittest

from patrol.patrol_node import validate_parameter


class TestPatrolParams(unittest.TestCase):

    def test_valid_params(self):
        self.assertTrue(validate_parameter('linear_speed', 0.5)[0])
        self.assertTrue(validate_parameter('turn_rate', -0.3)[0])
        self.assertTrue(validate_parameter('publish_hz', 5.0)[0])

    def test_invalid_params(self):
        self.assertFalse(validate_parameter('linear_speed', 1.5)[0])
        self.assertFalse(validate_parameter('turn_rate', -2.0)[0])
        self.assertFalse(validate_parameter('publish_hz', 0.0)[0])
        self.assertFalse(validate_parameter('publish_hz', -5.0)[0])
        self.assertFalse(validate_parameter('publish_hz', float('nan'))[0])


if __name__ == '__main__':
    unittest.main()
