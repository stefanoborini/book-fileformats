
Move-to-Front

Move-to-Front is a reversible transformation algorithm used to increase
the compression efficiency, most notably after a Burrows Wheeler
transformation. It is quite fast and not very complex to implement.  Each
symbol in the input data is substituted with a value referring to the index of
the symbol in an array L.  This array is initialized with an ordered set of all
the symbols expected in the input. Every time a byte is processed, it is moved
from its current position to the position 0 of the array, moving the symbols in
between one step forward, so to fill the empty space left by the move.  As a
result, redundant symbols are preferentially encoded as small (eventually zero)
values, which can be compressed in a very efficient way.

 For example, let's suppose to apply the move-to-front algorithm to the
result of the Burrows-Wheeler application (see FIXME) "nerrceeruc". The symbols
array is initialized as L = ["c", "e", "n", "r", "u"]. The order is preferential, and normally is
lexicographic. The following sequence is produced



The first value is the index of "n" in L, therefore we output 2. Then we move
"n" in the first position of L. The next symbol to encode is an "e", which is at index 2
in the current L array. Again, we output 2 and move the "e" symbol in the first position of L.
The final result is that frequently occurring symbols are encoded with small numbers, and long runs
of the same symbol gets encoded as long sequences of zeroes. For example, the
string "aaaabbbbaaaa" with L = ["a","b"] is encoded as "000010001000", which
can be compressed in a very efficient way. 

The decoding is equally simple and behaves similarly: the index is used
for selecting the entry in the L array, and after selection the symbol is moved
in front of the array.




