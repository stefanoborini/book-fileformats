<sect2><title>gzip</title>

<para>gzip is a compression file format based on the DEFLATE algorithm. The file format specifications
can be found in the IETF RFC1952. Focused on data exchange, it is independent of the environment and
contains information about the environment where the compression took place.</para>

<para>It can compress or decompress data from a stream, so it can operate also with piped data or from a network connection.
The resulting output is also a stream, which can be subsequently piped or redirected.</para>
<para>The deflate algorithm is based on the Lempel-Ziv 77 algorithm with Huffman coding. See section FIXME for details about the algorithm. deflate is
more efficient than the compress algorithm (FIXME name).</para>

<sect3>
<title>File format</title>

<para>A gzip file is defined with a series of blocks, called members, appended
one after another in the file.  Usually, there's only one member per file, but
in principle gzip can host multiple compressed files, each one with its own
member structure. Such file, once decompressed, behave as a single file, the result being an append
of the single files. All the numeric values are binary representations.
Each member has the structure depicted below</para>

<para>
FIXME this diagram is taken by the rfc, change it with a nice picture
         +---+---+---+---+---+---+---+---+---+---+
         |ID1|ID2|CM |FLG|     MTIME     |XFL|OS | 
         +---+---+---+---+---+---+---+---+---+---+

      (if FLG.FEXTRA set)

         +---+---+=================================+
         | XLEN  |...XLEN bytes of "extra field"...| 
         +---+---+=================================+

      (if FLG.FNAME set)

         +=========================================+
         |...original file name, zero-terminated...|
         +=========================================+

      (if FLG.FCOMMENT set)

         +===================================+
         |...file comment, zero-terminated...|
         +===================================+

      (if FLG.FHCRC set)

         +---+---+
         | CRC16 |
         +---+---+

         +=======================+
         |...compressed blocks...| (more-->)
         +=======================+

           0   1   2   3   4   5   6   7
         +---+---+---+---+---+---+---+---+
         |     CRC32     |     ISIZE     |
         +---+---+---+---+---+---+---+---+
</para>
<para>
FIXME verbatim paragraph
All the reserved bits must be set to zero.


Description of the fields:
* ID1/ID2: two bytes representing the magic number 0x1f 0x8b.
* CM: identifies the compression method used into the file. At the moment, choices between 0x00 and 0x07 are reserved, and the only admitted choice is 0x08, identifying the deflate algorithm.
* FLG: a bitfield with different flags
    bit 0   FTEXT: reports the fact that the file is probably ASCII test. 
                   This flag is an optional indication that can be added by the compressor 
                   utility. The decompressor utility can then use this flag to have hints
                   for chosing a good format on those systems where different file formats
                   for ASCII text and binary data are used. In case of doubt, the flag is
                   not used or ignored.
                   FIXME clarify more, find situations where this flag is used.
    bit 1   FHCRC: indicates the presence of a CRC16 (the two least-significant bytes of a CRC32) 
                   on the header up to and not including the CRC16 part. The CRC16 is stored immediately
                   before the compressed data.
    bit 2   FEXTRA: indicates the presence of optional extra fields.
    bit 3   FNAME: indicates the presence of the original filename of the file, terminated by a NUL byte.
                   The name must consist of ISO 8859-1 characters. The field will be used by the decompression
                   utility to produce an appropriate filename.
    bit 4   FCOMMENT: if set, a NUL terminated comment is present. It is not actively used by the decompressor.
                      it is just for human consumption. The comment must be encoded in ISO 8859-1 characters, and
                      line breaks should use a single line feed character (unix style)
    bit 5-7 reserved, must be zero.

* MTIME (4 bytes): is the last modification time of the original file, or the time when the compression started if
				   data came from a pipe. The format encodes the time in seconds since 00:00:00 GMT, Jan.  1, 1970
                   also called unix time. A value of zero means the value is not available.

* XFL: extra flags. used to specify the specific compression method. Using deflate, this flag can contain
       information about the type of choice relative to the compression efficiency. the value 0x02 is used for
       slowest algorithm wih high compression rate. The value 0x04 is used instead for the fastest algorithm.

* OS: Identifies the file system where the compression took place. This can provide important information
      to the decompressor utility, in order to produce a compatible file. At the moment, the list is standardized
      with the followings
       0 - FAT filesystem (MS-DOS, OS/2, NT/Win32)
       1 - Amiga
       2 - VMS (or OpenVMS)
       3 - Unix
       4 - VM/CMS
       5 - Atari TOS
       6 - HPFS filesystem (OS/2, NT)
       7 - Macintosh
       8 - Z-System
       9 - CP/M
      10 - TOPS-20
      11 - NTFS filesystem (NT)
      12 - QDOS
      13 - Acorn RISCOS
     255 - unknown

Optional fields:

* If FEXTRA is set, then the general header is followed by 
</para>

<para>
FIXME verbatim
         +---+---+=================================+
         | XLEN  |...XLEN bytes of "extra field"...| 
         +---+---+=================================+
</para>
<para>
FIXME verbatim
where XLEN is the total size of the extra field. This space host one or more
subfield, each one with the following representation
</para>
<para>
FIXME verbatim
            +---+---+---+---+==================================+
            |SI1|SI2|  LEN  |... LEN bytes of subfield data ...|
            +---+---+---+---+==================================+
</para>
<para>
FIXME verbatim
where SI1 and SI2 identifies an unique subfield ID, typically two ASCII letters. The gzip creator, 
Jean-Loup Gailly, keeps a registry of the allocated codes, and inquires for new extended headers
should be sent to him. The len fields contains the length of the subfield data.


* XLEN is a two bytes length of the extra field. The contents of the extra fields are not specified.

* If FHCRC is present, a two bytes CRC16 follows in the header

* The compressed data follow

* At the end, there is a CRC32 of the uncompressed data (4 bytes). The algo is the ISO3309 standard.
* following, other 4 bytes ISIZE containing the size of the uncompressed file, modulo 2^32.
</para>
</sect3>
</sect2>


