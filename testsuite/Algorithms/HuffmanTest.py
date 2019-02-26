import sys
import os
import unittest
sys.path.append(os.path.abspath("../../code/"))

from Algorithms import Huffman

class HuffmanTest(unittest.TestCase):
    def testEncoding(self):
        huffman = Huffman.Huffman()
        huffman.encode("abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+-=:;.,<>/?|ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        #huffman.encode( "A"*12 + "E"*42 + "I"*9 + "O"*30+"U"*7)
        self.assertEqual(encoded,'\x73\x00')


if __name__ == '__main__':
    unittest.main()

