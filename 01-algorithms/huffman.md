Huffman

The Huffman coding is a encoding technique for data compression. It works by
reducing the number of bits needed to represent a given symbol keeping into
account the relative probability of each symbol, so that frequently recurring
symbols are encoded with less bits. On average, the number of bits needed for
expressing the data is reduced.
The algorithm works by building an binary tree out of the symbols and the
associated probabilities.  Leaf nodes contain both symbol and probability,
internal nodes contain the sum of the probabilities of the child nodes. For
all the internal nodes, a value of 1 is assigned to a branch in one direction
(usually, by convention, the right direction) and a value of 0 is assigned to
the branch in the other direction.  The generated tree allows the definition of
a prefix-free code where the most frequent symbols are encoded with a reduced
number of bits. In the basic Huffman coding, encoder and decoder must agree on
the probability of each symbol, and thus the tree layout.  This can be done
deciding the layout once and for all (resulting in an implicit shared knowledge
of the encoder and the decoderi) or dynamically, where the encoder calculates
the probabilities of the actual data and creates the tree. For the decoder to
work of course this tree has to be made available explicitly, by transmitting
it together with the compressed data.

A variation of the Huffman coding, the Adaptive Huffman, readapts the
probabilities and changes the tree layout while encoding, in order to achieve
better adaptivity for data showing probability changes.


FIXME  Each leaf node contain

TODO
* confirm the left/right direction by checking the statement (originally found on wikipedia).
* check what is the ordering of the children nodes. who goes left, who goes right?
* check the cases where two probabilities are equal, and also the case when all the probabilities are equals.



