from django.test import TestCase


class SimpleTest(TestCase):

    def test_math(self):
        self.assertEqual(2 + 2, 4)

    def test_fail(self):
        self.assertEqual(2 + 2, 5)