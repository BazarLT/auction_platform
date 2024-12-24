import unittest

class TestHelloWorld(unittest.TestCase):
    def test_hello_world(self):
        self.assertEqual("Hello, World!", "Hello, World!")

def test_hello_world():
    assert 1 + 1 == 2

if __name__ == '__main__':
    unittest.main()