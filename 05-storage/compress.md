<sect2><title>compress</title>
<para>Compress is an old compression utility found on UNIX. It implements the
LZC compression algorithm, a variant of the classical Lempel-Ziv-Welch. The
associated extension is .Z, and the Mime-type is application/x-compress.
As of today it is rarely used, being replaced by gzip and bzip2 for popularity
and efficiency.</para>

<sect3>
<title>File format</title>

<para>The format is quite simple. A small header of three bytes is followed by
the compressed data.  The header contains the magic value 0x1F 0x9D, followed
by a single byte used as a bit field: the high bit is set to 1 in case of block
compression. Bit 6 and 5 are reserved. bit from 4 to zero express the number of bits used for the dictionary entries.</para>
</sect3>
</sect2>
