import unittest
import numpy as np

from src.turntable_alignment.Line import Line

class TestLine(unittest.TestCase):

    def test__get_angle(self):
        testee = Line(0, 0, 10, 10)
        self.assertEqual(testee.get_angle(), 45 / 180 * np.pi)

    def test__is_at_angle__exactly(self):
        testee = Line(0, 0, 10, 10)
        self.assertEqual(testee.is_at_angle(45), True)

    def test__is_at_angle__wrong_angle_without_threshold(self):
        testee = Line(0, 0, 10, 10)
        self.assertEqual(testee.is_at_angle(44, 0), False)

    def test__is_at_angle__wrong_angle_with_threshold(self):
        testee = Line(0, 0, 10, 10)
        self.assertEqual(testee.is_at_angle(44, 1), True)

    def test__deviation_from_horizontal_with_5(self):
        testee = Line(0, 0, 0.9961947, 0.08715574)
        self.assertEqual(testee.deviation_from_horizontal(), 5)

        # 5 Deg -> 5
        testee = Line(0, 0, 0.9961947, 0.08715574)
        print(testee.deviation_from_horizontal_deg())

        # 355 Deg -> 5
        testee = Line(0, 0, 0.9961947, -0.08715574)
        print(testee.deviation_from_horizontal_deg())

        # 175 Deg -> 5
        testee = Line(0, 0, -0.9961947, 0.08715574)
        print(testee.deviation_from_horizontal_deg())


if __name__ == '__main__':
    unittest.main()
