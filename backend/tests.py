from django.test import TestCase


class HelloTestCase(TestCase):
    def test_hello(self):
        self.assertEqual(1, 1)

    def test_hello2(self):
        self.assertEqual(2, 2)
