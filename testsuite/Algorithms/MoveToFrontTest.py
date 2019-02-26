import sys
import os
import unittest
sys.path.append(os.path.abspath("../../code/"))

from Algorithms import MoveToFront

class MoveToFrontTest(unittest.TestCase):
    def testEncoding(self):
        mtf = MoveToFront.MoveToFront()
        value_list = mtf.encode("aaaaabbbb")
        self.assertEqual(value_list,[97,0,0,0,0,98,0,0,0])
        value_list = mtf.encode("poppy")
        self.assertEqual(value_list,[112, 112, 1, 0, 121])

    def testDecoding(self):
        mtf = MoveToFront.MoveToFront()
        decoded_data = mtf.decode([97,0,0,0,0,98,0,0,0])
        self.assertEqual(decoded_data, "aaaaabbbb")
        decoded_data = mtf.decode([112, 112, 1, 0, 121])
        self.assertEqual(decoded_data, "poppy")

if __name__ == '__main__':
    unittest.main()

