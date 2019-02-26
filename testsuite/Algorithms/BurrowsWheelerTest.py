import sys
import os
import unittest
sys.path.append(os.path.abspath("../../code/"))

from Algorithms import BurrowsWheeler

class BurrowsWheelerTest(unittest.TestCase):
    def testEncoding(self):
        bw = BurrowsWheeler.BurrowsWheeler()
        string, pos = bw.encode("this is a test.")
        self.assertEqual(string,"ssat tt hiies .")
        self.assertEqual(pos, 14)

        string, pos = bw.encode("good, jolly good")
        self.assertEqual(string, "y,dood  oloojggl")
        self.assertEqual(pos, 5)


    def testDecoding(self):
        bw = BurrowsWheeler.BurrowsWheeler()
        string = bw.decode("ssat tt hiies .", 14)
        self.assertEqual(string,"this is a test.")

        string = bw.decode("y,dood  oloojggl",5)
        self.assertEqual(string,"good, jolly good")

if __name__ == '__main__':
    unittest.main()

