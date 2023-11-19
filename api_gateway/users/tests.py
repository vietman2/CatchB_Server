from django.test import TestCase

class TestPlaceholder(TestCase):
    def test_placeholder(self):
        self.assertEqual(1, 1)

    def test_workflow(self):
        self.assertEqual(2, 2)
