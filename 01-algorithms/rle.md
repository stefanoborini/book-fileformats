Run Length Encoding

Run Length Encoding is one of the most simple lossless compression
algorithms, and in some sense also the most intuitive. It is very simple to implement,
and needs a very limited amount of resources. Many different encoding schemes
exist, but all of them work on the same principle: to replace repetitions of symbols
with a single symbol and a counter indicating the number of repetitions. For example


aaaaabbbccdeeeeeeeee -> a5b3c2d1e9


The algorithm reduces a 20 bytes long string to a 10 bytes long string, under the
assumption that only one byte is used for the counter. Of course, Run Length
Encoding is efficient only with aggregated repeated information.  Typical
examples of this kind of data are bitmapped images containing large areas of
uniform color like fax data, and sparse files like databases.  When repeated
sequences do not occur, the algorithm leads to an increase of the data size,
instead of a reduction:


abccccdef -> a1b1c4d1e1f1


A possible solution to this problem is to use an escape information to flag the
presence of the counter only when needed, so to avoid its storage when a single
occurrence of a character is present. A very clever trick is to use the
repetition of the symbol itself twice as the escape information: when the
algorithm meets the same symbol twice, what will follow is a run length counter
of the remaining repetitions of the symbol, and not a symbol. With this scheme,
the strings given above becomes


aaaaabbbccdeeeeeeeee -> aa3bb1cc0dee7

abccccdef -> abcc2def


Although an encoding of two bytes leads to a three bytes occupation (two values
and a count of zero), this choice is a good compromise.

