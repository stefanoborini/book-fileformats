<sect2 xmlns:xi="http://www.w3.org/2001/XInclude">
<title>bzip2</title>

<para>Bzip2 implements a very efficient compression algorithm, albeit slower
when compared with gzip.  The algorithm is a combination of two transformation
filters, the Burrows Wheeler and the Move to Front, followed by a Huffman
coding compression. Bzip2 processes sequential chunks on data, compressing
them and producing independent compressed blocks, as a consequence of how
the Burrows Wheeler works. This allows partial data recovery if the file is
damaged, but makes impossible to produce decompressed data until a
compressed block is completely available.</para>

<sect3>
<title>High level view</title>
<para>The high level layout of the bzip2 file is presented in figure
FIXME. 
The file begins with the magic three-bytes ASCII sequence "BZh", followed by a
single byte containing an ASCII symbol in the interval "1"-"9". 
This value represents the size of the uncompressed chunks in units
of 100 kbytes (FIXME: control if the block size is of the compressed
block or the uncompressed one). A sequence of independent compressed blocks
follows this header. The number of blocks is arbitrary, and a special block
marks the end of the file.</para>
</sect3>
<sect3>
<title>The compressed block</title>

<para>The compressed block contains an independent chunk of compressed
information. A detailed picture of the block structure can be found in
figure FIXME. It is important to note that bzip2 file format works at the
bit level, and the lenght of the fields is variable.</para>

<variablelist>
  <varlistentry><term>Block header magic (6 bytes)</term>
                <listitem><para>Contains the magic byte sequence
                0x314159265359, indicating a data block. For those who
                didn't realize, this sequence is nothing but the initial
                ciphres of pi, whose low repetitiveness makes highly
                improbable its accidental occurence in the data section.
                This is important during data recovery from a corrupted
                file. (FIXME verify)</para></listitem>
  </varlistentry> 
  <varlistentry><term>CRC (4 bytes)</term>
                <listitem><para>Contains the Cyclic Redundancy Check of the
                block (FIXME: big endian? which part?) </para></listitem>
  </varlistentry> 
  <varlistentry><term>Randomized flag (1 bit)</term>
                <listitem><para>(FIXME: i have no idea of what
                it is used for, but it is something outdated. From a comment
                i found it has something to do while sorting.. if too many
                long comparison occur, a random shuffling is performed to
                improve the situation, however it is not clear why this
                information should be saved into the file, and why now it's
                outdated)</para></listitem>
  </varlistentry> 
  <varlistentry><term>Original position (3 bytes)</term>
                <listitem><para>Stores the row index in the
                Burrows Wheeler transformation matrix where the original
                data can be found. Once the transformation is undone, this
                value allows the decoder to find the original
                data.</para></listitem>
  </varlistentry> 
  <varlistentry><term>Stored Mapping Table (variable size)</term>
                <listitem><para>Stores a mapping table indicating which
                symbols were used in the initial input data. For example,
                when english text is compressed, not all symbols from 0 to
                255 are effectively used, but only letters, numbers, and
                punctation marks. The compression strategy can take
                advantage of the reduced number of symbols, improving the
                compression rate.  </para>
                <para>The storage strategy of the mapping table is as
                follows: during compression, an array of 256 boolean values
                is initialized to false for all the values. Data is then
                scanned, and for each byte found, the corresponding array
                element is set to true. The array is then ideally
                partitioned in 16 chunks of 16 elements each.  A bit map of
                16 bits (chunkInUse) is initialized to all zero. For each
                chunk, if it contains any True value, the corresponding bit
                of chunkInUse is set to 1, otherwise is left to 0. The file
                format contains the chunkInUse bit map, followed by the used
                chunks as bit maps, where true has been mapped to a 1 and
                false to a 0. The Stored Mapping Table field can therefore
                vary in length between 32 bit (16 bit of chunkInUse + 16 bit
                of the chunk) to 272 bits (16 bits of chunkInUse + 256 bits
                for the chunks)</para>
        		</listitem>
  </varlistentry> 
  <varlistentry><term>Selectors</term>
                <listitem><para>Size: 3 bits. Number of huffman coding
                groups used.  Number of Selectors: <remark>Every GROUP_SIZE
                many symbols we select a new huffman coding group.  Read in
                the group selector list, which is stored as MTF encoded bit
                runs. </remark>
                Runs Size: variable number of bits. For each of the
                selectors as specified in Number of selectors, a dump of 1
                bits of variable length is followed by a zero bit. This ends
                the selector. There are nSelector numbers of these
                chunks.</para></listitem>
  </varlistentry> 
  <varlistentry><term>Coding table</term>
				<listitem><para>Size: variable number of bits. nGroups number of blocks. each block contains 5 bits containing a length of some sort (FIXME), followed by some bits FIXME</para></listitem>
  </varlistentry> 
  <varlistentry><term>Data</term>
				<listitem><para>Size: variable number of bits. the actual data (FIXME)</para></listitem>
  </varlistentry> 
</variablelist>

<!--xi:include href="tables/table_bzip2_format"/ -->
</sect3>
<sect3>
<title>The last block</title>

<para>The last block structure consists only the first two entries of a data
block: the magic value, which contains 0x177245385090 (the square root of
pi) and a cumulative CRC of all the blocks in the file. No compressed data
is hosted into this block, however a small padding of several bit could be
present due to byte misalignment.</para>
</sect3>
<sect3><title>An example</title>

<para>The following example represents a step by step decomposition of a bzip2
file. The original, uncompressed file contains the string "this is a test.".
As already stated, bzip2 operates at the bit level, therefore a special
notation has been used to present the information. A hexadecimal value in
parenthesis means that only a part of its bit representation has been used
for describing the field.</para>
<para>The whole file is described by the following data</para>
<para><programlisting>
0x00|   42 5a 68 39 31 41 59 26 53 59 a7 a8 cb 10 00 00
0x20|   07 11 80 40 01 22 60 0c 00 20 00 21 a6 83 6a 10
0x40|   c0 88 b0 c6 9c 11 34 f1 77 24 53 85 09 0a 7a 8c
0x60|   b1 00      
</programlisting></para>
<para>The same file, with annotations, results in the following</para>
<para><programlisting>

------------------------------ File header ----------------------------- 

42 5A 68                         File magic  ("BZh")
39                               Block size  ("9")

------------------------------ Data Block ------------------------------

31 41 59 26 53 59                Magic block
A7 A8 CB 10                      CRC32
(00)                             Randomized
(00) 00 07 (11)                  Original Position
(11) 80 40 01 22 60 0C 00 (20)   Mapping table
(20) 00 (21)                     Selectors
(21) A6 83 6A 10 C0 (88)         Huffman code lengths 
(88) B0 C6 9C 11 34 (F1)         Data

------------------------------ Last block --------------------------------
(F1) 77 24 53 85 09 (0A)         magic block end 0x177245385090
(0A) 7A 8C B1 (00)               CRC32
(00)                             pad
</programlisting>
</para>
<para>We'll go along the whole file, recreating the original input from the
presented data.</para>

<variablelist>
  <varlistentry><term>Randomized</term>
                <listitem><para>
<programlisting>
hex       binary 
--------------------
(00)    [0]0000000  
</programlisting>
                </para>
                <para>The bit is set to zero, meaning that no randomization has
                occurred (FIXME)</para></listitem>
  </varlistentry> 
  <varlistentry><term>Original position (3 bytes)</term>
                <listitem><para>
<programlisting>
hex                      binary 
----------------------------------------------------------
(00) 00 07 (11)    0 [00000000 00000000 00001110] 0010001
</programlisting>
                </para>
                <para>The original position of the string in the Burrows Wheeler
                matrix is 12 in this example.</para>
                </listitem>
  </varlistentry> 
  <varlistentry><term>Stored Mapping Table</term>
                <listitem>
                <para>
<programlisting>
hex                  binary                           
(11) 80 (40)       0 [00100011 00000000] 1000000                  chunkInUse
(40) 01 (22)       0 [10000000 00000010] 0100010                  First chunk (32 "space" and 46 ".")
(22) 60 (0C)       0 [01000100 11000000] 0001100                  Second chunk (97 "a" 101 "e" 104 "h" 105 "i")
(0C) 00 (20)       0 [00011000 00000000] 0100000                  Third chunk (115 "s" 116 "t")
</programlisting>
                </para>
                <para>FIXME
                </para>
        		</listitem>
  </varlistentry> 
  <varlistentry><term>Selectors</term>
                <listitem><para>Size: 3 bits. Number of huffman coding
                groups used.  Number of Selectors: <remark>Every GROUP_SIZE
                many symbols we select a new huffman coding group.  Read in
                the group selector list, which is stored as MTF encoded bit
                runs. </remark>
                Runs Size: variable number of bits. For each of the
                selectors as specified in Number of selectors, a dump of 1
                bits of variable length is followed by a zero bit. This ends
                the selector. There are nSelector numbers of these
                chunks.</para></listitem>
  </varlistentry> 
  <varlistentry><term>Coding table</term>
				<listitem><para>Size: variable number of bits. nGroups number of blocks. each block contains 5 bits containing a length of some sort (FIXME), followed by some bits FIXME</para></listitem>
  </varlistentry> 
  <varlistentry><term>Data</term>
				<listitem><para>Size: variable number of bits. the actual data (FIXME)</para></listitem>
  </varlistentry> 
</variablelist>
<para>






<comment>
file containing "this is a test." without \n at the end
42 5A 68                           "BZh"                                           File header
39                                 "9"                                             Block size
31 41 59 26 53 59                                                                  Magic block
A7 A8 CB 10                                                                        CRC32
(00)                               [0]0000000                                      Randomized
(00) 00 07 (11)                     0 [00000000 00000000 00001110] 0010001         Original Position
(11) 80 (40)                        0 [00100011 00000000] 1000000                  chunkInUse
(40) 01 (22)                        0 [10000000 00000010] 0100010                  First chunk (32 "space" and 46 ".")
(22) 60 (0C)                        0 [01000100 11000000] 0001100                  Second chunk (97 "a" 101 "e" 104 "h" 105 "i")
(0C) 00 (20)                        0 [00011000 00000000] 0100000                  Third chunk (115 "s" 116 "t")
(20)                                0 [010] 0000                                   number of selector groups (2)
(20) 00 (21)                     0010 [00000000 0000001] 00001                     number of selectors (1)
(21)                              001 [0] 0001                                     group selector (mtf encoded) (0)
(21) (A6)                        0010 [00011] 0100110                              huffman codes lengths for each symbol (base) : 3
(A6)                               1  [0] 100110                                   first symbol: stop. len = 3
(A6)                               10 [10] 0110                                    second symbol: add 1 to previous: 4
(A6)                             1010 [0] 110                                      second symbol: stop: 4
(A6)                            10100 [11] 0                                       third symbol: subtract 1 to previous: 3
(A6)                          1010011 [0]                                          third symbol: stop: 3
(83)                                  [10] 000011                                  fourth symbol: add 1 to previous: 4
(83)                               10 [0] 00011                                    fourth symbol: stop : 4
(83)                              100 [0] 0011                                     fifth symbol : stop : 4
(83)                             1000 [0] 011                                      sixth symbol : stop : 4
(83)                            10000 [0] 11                                       seventh symbol : stop : 4
(83)                           100000 [11]                                         eighth symbol : subtract 1 : 3
(6A)                                  [0] 1101010                                  eighth symbol : stop : 3
(6A)                                0 [11] 01010                                   ninth symbol : subtract 1 : 2
(6A)                              011 [0] 1010                                     ninth symbol : stop: 2
(6A)                             0110 [10] 10                                      tenth symbol : add 1 : 3
(6A)                           011010 [10]                                         tenth symbol : add 1 : 4
(10)                                  [0] 0010000                                  tenth symbol: stop : 4
(10)                                0 [00100] 00                                   second group, first symbol: base 4
(10) C0 (88)                   000100 [0][0][110][0][0][0][0][0][100][0] 1000      values: 4 4 3 3 3 3 3 3 4 4
(88) B0 C6 9C 11 34 (F1)                                                           Data
(F1) 77 24 53 85 09 (0A)                                                           magic block end 0x177245385090
(0A) 7A 8C B1 (00)                                                                 CRC32
(00)                                                                               pad





(88) B0 C6 9C 11 34 (F1) 

huffcode     value    permute (assoc. val)
100            4            7 
010            2            0
1100           c            4
00             0            8
1100           c            4
00             0            2
1100           c            0
011            3            2
010            2            7
011            3            8
100            4            0
00             0            8
010            2            7
00             0            5
100            4            8
1101           d            9
00             0
1111           f   


tree:






<comment>

ottieni nextSym da un lookup su permute
ottieni uc da un move to front (mtfSymbol) di nextSym - 1 
ottieni uc dalla (mapping table) e l'(uc) precedente, attraverso lookup diretto
appendi uc a dbuf
dbuf: buffer finale prima della burrows wheeler


</comment>

















(88) B0 C6 9C 11 34 (F1) 

alphasize is 10 because there are two additional entries for runa runb.
huffcode     value    permute (assoc. val)
100            4            7 
010            2            0
1100           c            4
00             0            8
1100           c            4
00             0            8
1100           c           4 
011            3           2 
010            2           0 0 
011            3           2 2
100            4           7 7
00             0           8 8
010            2           0 0
00             0           8 8
100            4           7 7
1101           d           5 5
00             0           8 8
1111           f           9 9

huffcode is subtracted by a value, base, before applying permute

tree:

code[0]: 2
code[1]: a
code[2]: 3
code[3]: b
code[4]: c
code[5]: d
code[6]: e
code[7]: 4
code[8]: 0
code[9]: f

ottieni nextSym da un lookup su permute
ottieni uc da un move to front (mtfSymbol) di nextSym - 1 
ottieni uc dalla (mapping table) e l'(uc) precedente, attraverso lookup diretto
appendi uc a dbuf
dbuf: buffer finale prima della burrows wheeler


(20)                                0 [010] 0000                                   number of selector groups (2)
(20) 00 (21)                     0010 [00000000 0000001] 00001                     number of selectors (1)
(21)                              001 [0] 0001                                     group selector (mtf encoded) (0)
(21) (A6)                        0010 [00011] 0100110                              huffman codes lengths for each symbol (base) : 3
(A6)                               1  [0] 100110                                   first symbol: stop. len = 3
(A6)                               10 [10] 0110                                    second symbol: add 1 to previous: 4
(A6)                             1010 [0] 110                                      second symbol: stop: 4
(A6)                            10100 [11] 0                                       third symbol: subtract 1 to previous: 3
(A6)                          1010011 [0]                                          third symbol: stop: 3
(83)                                  [10] 000011                                  fourth symbol: add 1 to previous: 4
(83)                               10 [0] 00011                                    fourth symbol: stop : 4
(83)                              100 [0] 0011                                     fifth symbol : stop : 4
(83)                             1000 [0] 011                                      sixth symbol : stop : 4
(83)                            10000 [0] 11                                       seventh symbol : stop : 4
(83)                           100000 [11]                                         eighth symbol : subtract 1 : 3
(6A)                                  [0] 1101010                                  eighth symbol : stop : 3
(6A)                                0 [11] 01010                                   ninth symbol : subtract 1 : 2
(6A)                              011 [0] 1010                                     ninth symbol : stop: 2
(6A)                             0110 [10] 10                                      tenth symbol : add 1 : 3
(6A)                           011010 [10]                                         tenth symbol : add 1 : 4
(10)                                  [0] 0010000                                  tenth symbol: stop : 4
(10)                                0 [00100] 00                                   second group, first symbol: base 4
(10) C0 (88)                   000100 [0][0][110][0][0][0][0][0][100][0] 1000      values: 4 4 3 3 3 3 3 3 4 4
(88) B0 C6 9C 11 34 (F1)                                                           Data
(F1) 77 24 53 85 09 (0A)                                                           magic block end 0x177245385090
(0A) 7A 8C B1 (00)                                                                 CRC32
(00)                                                                               pad
</para>
</sect3>
</sect2>
