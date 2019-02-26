<sect2 xmlns:xi="http://www.w3.org/2001/XInclude">
<title>zip</title>

<remark>from http://en.wikipedia.org/wiki/ZIP_(file_format)</remark>

<para>Zip is probably the most popular and long-lived format combining
compression and archival.  It was designed by Phil Katz and technical
documentation was released along with the first version of his PKZIP archiver,
in January 1989.  Since the format was published, several competing projects
embraced it and it quickly became the de facto standard for distributing files
over BBS systems and then on the Internet.  Thanks to a easily extendable
design, several improvements have been added over time while maintaining great
backward compatibility.</para>

<para>In a zip file, every member file is compressed separately and this allows:
to retrieve one member without reading others, to compress each members with a
different method, to better resist against archive corruption.  The downside is
that an archive with lots of small files probably ends up being larger than
could be accomplished by compressing the bundle as a whole.</para>

<sect3>
<title>Original Zip file format</title>

<para>The original file format designed in 1989 was composed by a sequence of
member files stored in arbitrary order, followed by a <structname>central
directory</structname>.  Each member file section has a <structname>local file
header</structname> followed by actual compressed file contents.</para>

<remark>FIXME, add nice graph here</remark>

<para>The local file header is a sequence of fixed size unsigned integers in
Intel byte order <remark>FIXME</remark>, plus two variable length strings with
no terminator (length is known through one of the fixed size integers).</para>

<xi:include href="tables/table_zip_orig_local_file_hdr.xml"/>

<para>The <structfield>Version needed to extract</structfield> field is split
in two parts: lower byte indicates the minimum version number of the software
required to extract this file, encoded as 10*major+minor; upper byte indicates
the host operating system for this file, for example useful to determine line
record format for text files.</para>

<xi:include href="tables/table_zip_os_values.xml"/>

<para>Only the lowest bit of the <structfield>General purpose bit
flag</structfield> was used in the original file format, indicating whether the
file content was encripted.  Other bits were left for future use.  Every file
can be compressed with a different method, chosen by a table of half a dozen
and indicated by <structfield>Compression method</structfield>.
<structfield>CRC-32</structfield> is computed with David Schwaderer's method,
using <literal>0xdebb20e3</literal> as the <structfield>magic
number</structfield>, <literal>0xffffffff</literal> as initial value and finally
taking the one's complement of the CRC residual.  Dates are in MSDOS packed
format.</para>

<remark>MSDOS packed format: http://www.vsft.com/hal/dostime.htm</remark>

<para>After all member files, the central directory section contains a sequence
of <structname>central file header</structname> records (one for each member
file, not necessarily in the same order), terminated by an <structname>End of
central dir</structname> record.</para>

<xi:include href="tables/table_zip_orig_central_file_hdr.xml"/>

<para>The <structname>central file header</structname> records are basically a
redundant copy of the <structname>local file header</structname>, with some
additional information.  <structfield>Version made by</structfield> has the same
encoding as <structfield>Version needed to extract</structfield> but refers to
the version that was used to compress the file.  
        file comment length             2 bytes
        disk number start               2 bytes
        internal file attributes        2 bytes
        external file attributes        4 bytes
        relative offset of local header 4 bytes
</para>
</sect3>

<para>The <structname>local file header</structname> doesn't contain the
compressed size, this means the file can be written as a stream (compressed
file length doesn't have to be known in advance) but can only be read as a
stream when files are compressed with an algorithm where file termination can
be determined implicitly.  In particular this doesn't work for files stored
uncompressed.</para>

<para>
FIXME verbatim
http://groups.google.com/group/comp.sys.ibm.pc/msg/b75c9a32f142a9d3
 General Format
--------------

  Files stored in arbitrary order.  Large zipfiles can span multiple
  diskette media.

  Overall zipfile format:

    [local file header+file data] . . .
    [central directory] end of central directory record

  A.  Local file header:

        local file header signature     4 bytes  (0x04034b50)
        version needed to extract       2 bytes
        general purpose bit flag        2 bytes
        compression method              2 bytes
        last mod file time              2 bytes
        last mod file date              2 bytes
        crc-32                          4 bytes
        compressed size                 4 bytes
        uncompressed size               4 bytes
        filename length                 2 bytes
        extra field length              2 bytes

        filename (variable size)
        extra field (variable size)

  B.  Central directory structure:

      [file header] . . .  end of central dir record

      File header:

        central file header signature   4 bytes  (0x02014b50)
        version made by                 2 bytes
        version needed to extract       2 bytes
        general purpose bit flag        2 bytes
        compression method              2 bytes
        last mod file time              2 bytes
        last mod file date              2 bytes
        crc-32                          4 bytes
        compressed size                 4 bytes
        uncompressed size               4 bytes
        filename length                 2 bytes
        extra field length              2 bytes
        file comment length             2 bytes
        disk number start               2 bytes
        internal file attributes        2 bytes
        external file attributes        4 bytes
        relative offset of local header 4 bytes

        filename (variable size)
        extra field (variable size)
        file comment (variable size)

      End of central dir record:

        end of central dir signature    4 bytes  (0x06054b50)
        number of this disk             2 bytes
        number of the disk with the
        start of the central directory  2 bytes
        total number of entries in
        the central dir on this disk    2 bytes
        total number of entries in
        the central dir                 2 bytes
        size of the central directory   4 bytes
        offset of start of central
        directory with respect to
        the starting disk number        4 bytes
        zipfile comment length          2 bytes
        zipfile comment (variable size)

  C.  Explanation of fields:

      version made by

          The upper byte indicates the host system (OS) for the
          file.  Software can use this information to determine
          the line record format for text files etc.  The current
          mappings are:

          0 - IBM (MS-DOS)      1 - Amiga       2 - VMS
          3 - *nix              4 thru 255 - unused

          The lower byte indicates the version number of the
          software used to encode the file.  The value/10
          indicates the major version number, and the value
          mod 10 is the minor version number.

      version needed to extract

          The minimum software version needed to extract the
          file, mapped as above.

      general purpose bit flag:

          The lowest bit, if set, indicates that the file is
          encrypted.  The upper three bits are reserved and
          used internally by the software when processing the
          zipfile.  The remaining bits are unused in version
          1.0.

      compression method:

          (see accompanying documentation for algorithm
          descriptions)

          0 - The file is stored (no compression)
          1 - The file is Shrunk
          2 - The file is Reduced with compression factor 1
          3 - The file is Reduced with compression factor 2
          4 - The file is Reduced with compression factor 3
          5 - The file is Reduced with compression factor 4

      date and time fields:

          The date and time are encoded in standard MS-DOS
          format.

      CRC-32:

          The CRC-32 algorithm was generously contributed by
          David Schwaderer and can be found in his excellent
          book "C Programmers Guide to NetBIOS" published by
          Howard W. Sams &amp; Co. Inc.  The 'magic number' for
          the CRC is 0xdebb20e3.  The proper CRC pre and post
          conditioning is used, meaning that the CRC register
          is pre-conditioned with all ones (a starting value
          of 0xffffffff) and the value is post-conditioned by
          taking the one's complement of the CRC residual.

      compressed size:
      uncompressed size:

          The size of the file compressed and uncompressed,
          respectively.

      filename length:
      extra field length:
      file comment length:

          The length of the filename, extra field, and comment
          fields respectively.  The combined length of any
          directory record and these three fields should not
          generally exceed 65,535 bytes.

      disk number start:

          The number of the disk on which this file begins.

      internal file attributes:

          The lowest bit of this field indicates, if set, that
          the file is apparently an ASCII or text file.  If not
          set, that the file apparently contains binary data.
          The remaining bits are unused in version 1.0.

      external file attributes:

          The mapping of the external attributes is
          host-system dependent (see 'version made by').  For
          MS-DOS, the low order byte is the MS-DOS directory
          attribute byte.

      relative offset of local header:

          This is the offset from the start of the first disk on
          which this file appears, to where the local header should
          be found.

      filename:

          The name of the file, with optional relative path.  
          The path stored should not contain a drive or
          device letter, or a leading slash.  All slashes
          should be forward slashes '/' as opposed to
          backwards slashes '\' for compatibility with Amiga
          and Unix file systems etc.

      extra field:

          This is for future expansion.  If additional information
          needs to be stored in the future, it should be stored
          here.  Earlier versions of the software can then safely
          skip this file, and find the next file or header.  This
          field will be 0 length in version 1.0.

      file comment:

          The comment for this file.

      number of this disk:

          The number of this disk, which contains central
          directory end record.

      number of the disk with the start of the central directory:

          The number of the disk on which the central
          directory starts.

      total number of entries in the central dir on this disk:

          The number of central directory entries on this disk.

      total number of entries in the central dir:

          The total number of files in the zipfile.

      size of the central directory:

          The size (in bytes) of the entire central directory.

      offset of start of central directory with respect to
      the starting disk number:

          Offset of the start of the central direcory on the
          disk on which the central directory starts.

      zipfile comment length:

          The length of the comment for this zipfile.

      zipfile comment:

          The comment for this zipfile.

  D.  General notes:

      1)  All fields unless otherwise noted are unsigned and stored
          in Intel low-byte:high-byte, low-word:high-word order.

      2)  String fields are not null terminated, since the
          length is given explicitly.

      3)  Local headers should not span disk boundries.  Also, even
          though the central directory can span disk boundries, no
          single record in the central directory should be split
          across disks.

      4)  The entries in the central directory may not necessarily
          be in the same order that files appear in the zipfile. 
</para>


<para>
FIXME verbatim

ZIP is a fairly simple archive format that compresses every file separately.
Compressing files separately allows for individual files to be retrieved
without reading through other data; in theory, it may allow better compression
by using different algorithms for different files. However a caveat to this is
that archives containing a large number of small files end up significantly
larger than if they were compressed as a single file (the classic example of
the latter is the common tar.gz archive which consists of a TAR archive
compressed using gzip).

The specification for ZIP indicates that files can be stored either uncompressed or using a variety of compression algorithms. However, in practice, ZIP is almost always used with Katz's DEFLATE algorithm, except when files being added are already compressed or are resistant to compression.

ZIP supports a simple password based symmetric encryption system which is known to be seriously flawed. In particular it is vulnerable to known-plaintext attacks which are in some cases made worse by poor implementations of random number generators[1]. It also supports spreading archives across multiple removable disks (generally floppy disks, but it could also be used with other removable media).

New features including new compression and encryption methods have been added to ZIP in more recent times, but these are not supported by many tools and are not in wide use.

Most zip programs support at most 4GB files; though various vendors have "64-bit extended format"s to store larger files. It's not clear if the various vendors use the same formats for large files.

The FAT filesystem of DOS only has a granularity of two seconds; the Zip file records mimic this. As a result, the granularity of files in a Zip archive is only two seconds.

The Info-ZIP implementations of the Zip format adds support for Unix filesystem features, such as user and group IDs, file permissions, and support for symbolic links. The Apache Ant implementation is aware of them to the extent that it can create files with predefined Unix permissions.

The Info-ZIP Windows tools also support NTFS filesystem permissions, and will make an attempt to translate from NTFS permissions to Unix permissions or vice-versa when extracting files. This is sometimes annoying, and can result in undesireable combinations, e.g. .exe files being created on NTFS volumes with executable permission denied.

Compression methods

The size for comparison figures were made using the contents of ftp://ftp.kernel.org/pub/linux/kernel/v2.6/linux-2.6.9.tar.bz2 and maximum compression.

* Shrinking (method 1)

Shrinking is a variant of LZW with a few minor tweaks. As such it was affected by the LZW patent issue. It was never clear if the patent covered unshrinking but some open source projects (for example Info-ZIP) decided to play it safe and not include unshrinking support in the default builds.

* Reducing (methods 2-5)

Reducing involves a combination of compressing repeated byte sequences then applying a probability-based encoding to the result.

* Imploding (method 6)

Imploding involves compressing repeated byte sequences with a sliding window then compressing the result using multiple Shannon-Fano trees.

* Tokenizing (Method 7)

This method number is reserved. The PKWARE specification does not define an algorithm for it. This is because the format was developed (as a non-proprietary open specification) by a third-party other than PKWARE for specialized usage.

* Deflate and enhanced deflate (methods 8 and 9)

These methods use the well-known deflate algorithm. Deflate allows a window up to 32 KiB. Enhanced deflate allows a window up to 64 KiB. The enhanced version performs slightly better but is not as widely supported.

Sizes for comparison (using pkzip 8.00.0038 for Windows):

* Deflate: 52.1 MiB
* Enhanced deflate: 51.8 MiB

* PKWARE Data Compression Library Imploding (method 10)

The official ZIP format specification gives no further information on this.

Size for comparison: 61.6 MiB (pkzip 8.00.0038 for Windows in binary mode).

* Method 11

This method number is reserved by PKWARE.

* Bzip2 (method 12)

This method uses the well-known bzip2 algorithm. This algorithm performs better than deflate but is not widely supported, particularly by Windows-based tools.

Size for comparison: 50.6 MiB (pkzip 8.00.0038 for Windows).

Note that although both the original (tar inside bzip2, 34.6 MiB) and the comparison version (bzip2 as a ZIP method, 50.6 MiB) use the same compression algorithm, the ZIP version is 46% larger. This demonstrates the compression ratio advantage of a solid archive over ZIP's strategy of compressing each individual file separately when used to archive many (16,448) files. 
</para>
</sect2>
