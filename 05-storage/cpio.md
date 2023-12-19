<sect2 xmlns:xi="http://www.w3.org/2001/XInclude">
<title>cpio</title>

<para>Like tar, cpio file format is used to concatenate several files into one
single archive, usually stored on tape.  The first implementation appeared in
PWB/UNIX 1.0, released in 1977.  Back then, tar was probably unknown to people
working in AT&amp;T.   The name is an acronym and stands for 
<emphasis>CoPy In/Out</emphasis>.</para>

<para>The format is composed of a sequence of member files, each one consisting
of a header and optionally the file content.   A final empty file named
<literal>TRAILER!!!</literal> marks the archive end.</para>

<para>Two different cpio formats have been initially implemented, differing on
how the header is encoded.  ASCII archives have printable human readable
headers stored as fixed width not NUL-terminated strings containing octal
numbers padded with zeroes on the left, while binary headers use a mix of 2 and
4 bytes binary integers.  Binary was the default style.</para>

<xi:include href="tables/table_cpio_ascii_hdr.xml"/>

<para>In the ASCII style, after the header we find the filename as a
variable length NUL-terminated string (namesize bytes long, including the
terminator) and the variable length file contents (filesize bytes).  Values in
the header are supposed to be compatible with values returned by the UNIX
<function>stat(2)</function> system call, expecially the bitmask stored in file
mode, but unfortunately the meaning of bits is slightly different on different
unix flavours.  <structfield>rdev</structfield> is used only for block and
character devices.  <structfield>filesize</structfield> is zero in case of
special files and directories.</para>

<xi:include href="tables/table_cpio_binary_hdr.xml"/>

<para>Binary style uses the same values ad meaning as the ASCII format, just
coded differently, except for <structfield>namesize</structfield> which is
rounded up to the nearest 2 bytes boundary.  After this header we find again
the filename (with one or two NUL-terminators, depending on alignment) and the
file content.  The magic number is octal <literal>070707</literal> (hex
<literal>0x71c7</literal>).  Byte ordering for the integers is machine
dependent therefore the magic number has to be used to find out whether
byte-swapping is needed or not.  A file generated on a machine with a swapped
bytes is recognized by <structfield>magic</structfield>
<literal>0xc771</literal> (octal <literal>0143561</literal>).  
For maximum portability the ASCII format should be used.</para>

<para>On windows and other non-UNIX operating systems, many of the header
values are meaningless, but this doesn't compromise interoperability.</para>

<xi:include href="tables/table_cpio_filemode_flags.xml"/>

<para>Several UNIX versions use 32 bits to store some of the values returned by
<function>stat(2)</function> and this proved particularly problematic for the
inode number because this value is needed to find out hard links (hard links
are regular files but they share the same inode on a different file name).  The
binary format has just 16 bits available and the original portable ASCII format
has 18, which is not enough anyway.  To fix this problem a new portable format
has been designed, using hexadecimal representation instead of octal and two
more bytes per field.</para>

<xi:include href="tables/table_cpio_new_hdr.xml"/>

<para>This format can be automatically recognized thanks to a different magic
number.  A new field is also added, to store a checksum of the file content
(only used with magic <literal>070702</literal>) computed as the 4 least
significant bytes of the sum of all the bytes in the file.  The filename is
terminated by a variable number of NULs (minimum one, maximum four) so that the
file content begins on a 4 bytes boundary.</para>

<para>The new file format recommends all fields, including the file name,
should be encoded in ISO 646 International Reference Version (equivalent to
ASCII), and this is a serious limit for most non english languages.  The Single
UNIX Specification version 2 goes even further urging to use only characters in
the stricter Portable Filename Character Set, to promote portability between
systems configured with different charset.</para>

<para>Old binary and new cpio file formats use four bytes to encode the file
length and therefore cannot store files bigger than four gigabytes.  The old
ASCII format used 33 bits and therefore allowed 8 gigabytes.</para>

<sect3>
<title>Comparison of tar and cpio</title>

<itemizedlist>
<listitem><para>cpio archive formats, like tar, do have maximum pathname
lengths, however the limit for cpio is much higher (16 bits in the binary
format and 18 bits in the old ASCII format).</para></listitem>

<listitem><para>cpio doesn't handle BSD symbolic links but traditional tar
doesn't handle special files.</para></listitem>

<listitem><para>Original cpio formats had problems handling hard links, as
described above.  These problems have been fixed in the new portable format but
still a complete copy of the contents is stored on tape for each link.  With
tar only one copy is stored, but then you can use only that copy name for
retrieval.</para></listitem>

<listitem><para>cpio original format didn't have a checksum, but it was added
in the new portable CRC format.</para></listitem>

<listitem><para>tar is more tape oriented because each file is aligned to the
physical block size.  cpio has no alignment and is therefore more
compact.</para></listitem>

<listitem><para>tar can archive sparse files as sparse, while cpio always
expands them.</para></listitem>

</itemizedlist>

</sect3>

</sect2>
