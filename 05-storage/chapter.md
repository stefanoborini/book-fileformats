<?xml version="1.0"?>
<chapter xmlns:xi="http://www.w3.org/2001/XInclude" id="storage">
<title>Storage</title>
<sect1>
<title>Files into files</title>
<para>Here some initial comments on the storage chapter</para>
<remark>
consider the following general points points:

1) solid compression.
2) stream decoding
3) lossless file formats, for obvious reasons 
</remark>

<para>In this section we describe several ways of storing files into files, an
operation usually named <emphasis>archiving</emphasis>.  There can be different
motivations to files inside files, leading to different design decisions:</para>

<itemizedlist>
<listitem><para>grouping together several files, or a whole hierarchy of
directories, in a single easy-to-handle object;</para></listitem>
<listitem><para>applying compression algorithm to obtain a smaller
file;</para></listitem>
<listitem><para>storing file content together with their metadata (e.g.
filename, file attributes, location);</para></listitem>
<listitem><para>adding more metadata and installation instructions (e.g.
packages);</para></listitem>
<listitem><para>adding integrity checks.</para></listitem>
</itemizedlist>

<para>Over time, main goals of archive formats have changed.  Back in the
seventies the main use was to produce tape backups, to be restored in case of
hardware failure or accidental deletion.  Some years later, tapes began to
become an important exchange media as people used to mail tapes back and forth
to exchange data and software.</para>

<para>At some point, with the advent of research networks and bullettin boards
this exchange activity started to be performed over slow network connections
and this made compression a very important feature of archiving.  In the UNIX 
world where tools are normally supposed to do one single thing, compressione
was typically introduced as a two-steps process, meaning that files were
first bundled together with normal tar or cpio, and then compressed with 
compress or gzip.  Out of the UNIX world, new formats combining compression and
bundling in a single step have had more success. They are usually referred as
solid archives.</para>

<para>Nowadays, an important storage concept is the software package, that is a
way to distribute programs and make them nicely auto-install and integrate in a
live operating system.  To make this work, software and data have to be bundled
with descriptions, license info, install and uninstall scripts, information on
how to register/unregister libraries, drivers and components.</para>

</sect1>

<sect1>
<title>Simple storage</title>
<sect2 xmlns:xi="http://www.w3.org/2001/XInclude">
<title>tar</title>

<!--\MACROMimeType{application/x-tar}-->

<para>TAR (Tape ARchive) is a common storage file format under UNIX, once used
mainly for backup on magnetic tapes. Today, TAR archives are very popular in
the opensource world, in particular for packaging sources. The format focuses
on aggregating files and directories into a single file, leaving the
compression step to other tools such as the programs <command>gzip</command>
or <command>bzip2</command>.</para>

<para>Despite various attempts in standardization, TAR is a highly forked
format.  This makes very difficult to achieve true interoperability between
different implementations of the tar utility. In fact, each format is more or
less incompatible with the other ones, despite sharing a very similar
structure.</para>

<!--Magnetic tape access and writing is sequential in nature, and TAR focuses on
this sequential nature. As a result, the TAR file format has the following
disadvantages: FIXME
%\begin{itemize}
%\item Performing partial extraction is slow on average, and the access time is dependent
%on the position of the file to extract into the archive. 
%\item file removal 
%\end{itemize}
%Extensions of the formats were made for overcoming various limitations.
No compression nor encryption is supported. 
-->
<sect3>
<title>General file format</title>
<para>TAR was designed taking into account the hardware characteristics of the
early tape storage which allowed writing only in 512 bytes blocks, or
physical blocks. The physical block is the basic chunk of information in a
tar archive, and this entity is used pervasively. Data are always padded
with NUL bytes to a multiple of 512 bytes.</para>

<para>Physical blocks are aggregated for Input/Output operations into records:
each record is made by an integral number of physical blocks, and is written
with a single <function>write()</function> operation. The number of physical
blocks making a record is called <firstterm>blocking factor</firstterm>, and is
normally a command line parameter of the tar utility. The typical default
blocking factor is 20, meaning that the smallest archive that can be obtained
is made of 20*512 physical blocks, thus 10240 bytes, no matter of the actual
size of the archived file. The content of the remaining space is undefined, but
normally is NUL filled.</para>

<sidebar>
  <para>Blocking had important consequences on efficiency, reliability and
  speed when tape storage was performed: each <function>write()</function>
  operation gave rise to a contiguous stream of data on the tape, and for
  hardware reasons two different calls produced an empty gap on the tape,
  wasting it. A low blocking factor lead to huge amounts of wasted tape,
  whereas a high blocking factor lead to better tape usage and high writing
  speed, but a reduced chance of partial recovery in case of a tape failure.
  When storing to tar files on a disk, as it is common today, blocking factor
  is no longer a critical parameter: the standard value of 20 is changed only
  when efficient storage of a very high number of small files is needed.</para>
</sidebar>

<para>The file format is defined as in picture 
<xref linkend="img:tar-high-level"/>. Each
stored file is prepended by a physical block for the header, containing
information about the file itself. The header is then followed by zero or
more blocks, containing unaltered file data.  If an archived file size is
not a multiple of 512, padding is added to fill up the last block. The
archive is terminated by an end-of-archive sequence, two consecutive NUL
filled physical blocks.</para>

<figure id="img:tar-high-level">
  <title>High level structure of tar format</title>
  <graphic fileref="figs/eggplant.eps"/>
</figure>

<para>All TAR formats share the common infrastructure described above. The
difference between the various implementations of TAR resides in the
data layout in the header. These differences mainly arose from the need to
deal with the limits of the format, most notably the 100 bytes limit in the
file name length.</para>
</sect3>

<sect3>
<title>The V7 header</title>
<para>It is one of the oldest tar formats. Being old, design choices that were
appropriate at the time it was developed now are limitations. The most
important one is the size of the file, link or directory name, limited to 100
characters, and the type of file that can be stored, allowing only files,
directories and symbolic links, but no devices, named pipes and so on.  The
maximum user id and group id is <literal>2097151</literal>, and the maximum
file size is 8GB.  Finally, V7 headers store only user id and group id, not the
symbolic (user name and group name) information, therefore a currect mapping of
the ownership is not possible when moving an archive between two machines
having different id's for the same owner.</para>

<table id="tar-v7-header" xml:base="tables/table_tar_v7_hdr.xml"><title>V7 Header</title><tgroup cols="3"><thead><row><entry>Offset</entry><entry>Size</entry><entry>Field</entry></row></thead><tbody><row><entry>0</entry><entry>100</entry><entry>File name</entry></row><row><entry>100</entry><entry>8</entry><entry>File mode</entry></row><row><entry>108</entry><entry>8</entry><entry>Owner user ID</entry></row><row><entry>116</entry><entry>8</entry><entry>Group user ID</entry></row><row><entry>124</entry><entry>12</entry><entry>File size in bytes</entry></row><row><entry>136</entry><entry>12</entry><entry>Last modification time</entry></row><row><entry>148</entry><entry>8</entry><entry>Check sum for header block</entry></row><row><entry>156</entry><entry>1</entry><entry>Link indicator</entry></row><row><entry>157</entry><entry>100</entry><entry>Name of linked file</entry></row><row><entry>257</entry><entry>255</entry><entry>Empty</entry></row></tbody></tgroup></table>

<para>The <structfield>File name</structfield> field contains the name of the
archived file.  The field is NUL terminated only if not used completely. In the
latter case, the whole size of the field is used.</para>

<para>A file name containing a slash as the last character is meant to belong
to a directory, no matter what the <structfield>typeflag</structfield> states. 
<remark>at least in the star program.  The allowed typeflags seems to be
<literal>DIRTYPE</literal>, <literal>SYMTYPE</literal> and anything else will
be interpreted as file.</remark></para>

<para>The header contains various information about the stored file. 
Of the 512 bytes not all the space is used. Unused space is NUL filled.</para>

<para>For portability across platforms with different byte order, the
information into the various fields is ASCII encoded. Fields containing strings
are NUL terminated C-strings, except when all the field is used, where the NUL
termination is not present. Numeric fields are written in octal representation
as strings.</para>

<para>Calculation of the checksum is performed as follows: the header is filled
with the information, and the checksum is left filled with spaces. bytes of the
header are summed and the final result is written into the checksum field in
octal representation.</para>

<para>a directory is indicated either by a link indicator for directory or a
link indicator for normal file and a filename appended with a trailing
slash</para>
</sect3>

<sect3>
<title>BSD tar</title>
</sect3>

<sect3>
<title>ustar</title>

<para>The ustar format, also known as <citetitle>POSIX 1003.1-1988</citetitle>,
was designed to overcome the limitation of the original TAR format. This is
possible by adding data to the mostly empty V7 header.</para>

<para>In particular, the ustar format can store special files, like devices,
named pipes and so on, and it allows longer file names: the maximum length for
the path is increased to 256 bytes, provided that it is possible to split the
filename at a directory separator, and the resulting parts do not exceed 155
bytes and 100 bytes, respectively. Therefore, 256 bytes is the maximal value in
ideal conditions.</para>

<table id="ustar-header" xml:base="tables/table_ustar_hdr.xml"><title>USTAR header table</title><tgroup cols="3"><thead><row><entry>Offset</entry><entry>Size</entry><entry>Field</entry></row></thead><tbody><row><entry>0</entry><entry>100</entry><entry>File name</entry></row><row><entry>100</entry><entry>8</entry><entry>File mode</entry></row><row><entry>108</entry><entry>8</entry><entry>Owner user ID</entry></row><row><entry>116</entry><entry>8</entry><entry>Group user ID</entry></row><row><entry>124</entry><entry>12</entry><entry>File size</entry></row><row><entry>136</entry><entry>12</entry><entry>Last modification time</entry></row><row><entry>148</entry><entry>8</entry><entry>Header checksum</entry></row><row><entry>156</entry><entry>1</entry><entry>Type flag</entry></row><row><entry>157</entry><entry>100</entry><entry>Name of linked file</entry></row><row><entry>257</entry><entry>6</entry><entry>USTAR indicator</entry></row><row><entry>263</entry><entry>2</entry><entry>USTAR version</entry></row><row><entry>265</entry><entry>32</entry><entry>Owner user name</entry></row><row><entry>297</entry><entry>32</entry><entry>Owner group name</entry></row><row><entry>329</entry><entry>8</entry><entry>Device major number</entry></row><row><entry>337</entry><entry>8</entry><entry>Device minor number</entry></row><row><entry>345</entry><entry>155</entry><entry>File name prefix</entry></row><row><entry>500</entry><entry>12</entry><entry>Empty</entry></row></tbody></tgroup></table>

<variablelist>
<varlistentry>
  <term>File name</term>
  <listitem><para>Like in V7.  The value of the prefix field, if not NUL,
  is prefixed to this field to allow names longer then 100 characters. The
  splitting is performed keeping into account an implicit path separator
  between the two strings. Both fields are NUL terminated only if the field
  is used partially, otherwise they are not.</para></listitem>
</varlistentry>
<varlistentry>
  <term>File mode</term>
  <listitem><para>12 bit octal number representing the permission in octal
  representation.</para></listitem>
</varlistentry>
<varlistentry>
  <term>user id</term>
  <listitem><para>Leading zero-filled octal number. <remark>FIXME NUL
  terminated?  octal?</remark></para></listitem>
</varlistentry>
<varlistentry>
  <term>group id</term>
  <listitem><para>Leading zero-filled octal number. <remark>NUL-terminated,
  octal?</remark></para></listitem>
</varlistentry>
<varlistentry>
  <term>File size</term>
  <listitem><para>The size of the stored file in bytes. <remark>leading
  zero-filled octal number. NUL-terminated? should be not.</remark>  If the
  typefield is of type 1 (link) or 2 (symbolic link), this field is 0.  If the
  typefield is 5 (a directory), the size is normally zero, but it could be
  different from zero in some systems, where directory creation requires to
  specify the number of bytes that directory will contain. No data are stored
  after a header with type 1,2 or 5. If the type is set to 3 (character special
  file), 4 (block special file), or 6 (FIFO), the meaning of size is
  unspecified, and no data follows the header.</para>
  <para>If typeflag is set to any other value, the number of blocks following
  the header must be the result of (size+511)/512 as an integer division,
  ignoring any remainder.</para></listitem>
</varlistentry>
<varlistentry>
  <term>Last modification time</term>
  <listitem><para>leading zero-filled octal number. <remark>NUL-terminated? 
  should be not.</remark> The last modification time of the file when it was
  archived, in octal form.</para></listitem>
</varlistentry>
<varlistentry>
  <term>Header checksum</term>
  <listitem><para>Leading zero-filled octal number. A checksum of all the bytes
  in the header.  The checksum is calculated from the header assuming that the
  chksum field itself is all blanks. The value is a simple unsigned sum of the
  bytes in the header, with a precision at least of 17 bits (which can hold the
  maximum expected value). The final result is then converted to octal
  representation. <remark>signed or unsigned? NUL-terminated?</remark></para>
  <para>Erroneous data in the archive member will not be detected, being a
  checksum only of the header.</para>
  <remark>empty block-&gt;cksum == 0, so it is not always considered space
  filled.</remark>
  <remark>The chksum field is the ASCII representation of the octal value of
  the simple sum of all bytes in the header block. Each 8-bit byte in the
  header is added to an unsigned integer, initialized to zero, the precision of
  which shall be no less than seventeen bits. When calculating the checksum,
  the chksum field is treated as if it were all blanks.</remark></listitem>
</varlistentry>
<varlistentry>
  <term>Type flag</term>
  <listitem><para>A single character.  A compatible extension of the link field
  of the older TAR format.  The values that are recognized. 
  <remark>The values that are recognized. see table FIXME</remark>
  Specifies the type of file archived.</para></listitem>
</varlistentry>
<varlistentry>
  <term>Name of linked file</term>
  <listitem><para>NUL terminated string, except when the full field is
  used.</para></listitem>
</varlistentry>
<varlistentry>
  <term>USTAR indicator/version</term>
  <listitem><para>contains the NUL terminated string <literal>ustar</literal>.
  <structfield>version</structfield> contains the characters
  <literal>00</literal> (zero-zero).</para></listitem>
</varlistentry>
<varlistentry>
  <term>Owner user/group name</term>
  <listitem><para>The owner user and group name of the file. This information
  is used if the identification succeeds at extraction time, ignoring the
  stored user ID and group ID. The strings are NUL
  terminated.</para></listitem>
</varlistentry>
<varlistentry>
  <term>Device major/minor number</term>
  <listitem><para>leading zero-filled octal number.</para></listitem>
</varlistentry>
<varlistentry>
  <term>File name prefix</term>
  <listitem><para>NUL terminated, except when the full field is
  used.</para></listitem>
</varlistentry>
</variablelist>

<para>Numeric fields are terminated by one or more spaces or NUL.  Archives can
contain more than one member with the same name, allowing to have more than one
version of a file has been stored in the archive. When extracted, the latest
version will be restored.</para>

<para>In addition to entries describing archive members, an archive may contain
entries which tar itself uses to store information.  See label, for an example
of such an archive entry.</para>
</sect3>

<sect3>
<title>POSIX 1003.1-2001, also known as pax format</title>
<para><![CDATA[
Format 	UID 	File Size 	Path Name 	Devn
posix 	Unlimited 	Unlimited 	Unlimited 	Unlimited
    Archive format defined by POSIX.1-2001 specification. This is the most
flexible and feature-rich format. It does not impose any restrictions on
file sizes or filename lengths. This format is quite recent, so not all tar
implementations are able to handle it properly. However, this format is
designed in such a way that any tar implementation able to read `ustar'
archives will be able to read most `posix' archives as well, with the only
exception that any additional information (such as long file names etc.)
will in such case be extracted as plain text files along with the files it
refers to.
Support for the new POSIX.1-2001 extended tar format. This new tar 
	format allows to archive many new things in a standard compliant way.
	These things are currently are implemented in Gnu tar in a proprietary 
	way and have in former times been implemented in a proprietary way in 
	star. To give an example, the most interesting features that are now 
	handled in a standard compliant way are filenames without name len 
	limitation and file size without the old 8 GB tar limitation.
	An interesting aspect of the new extended header format is that the
	extended header format itself is extensible without limitation. Star
	uses this extension format to archive Access Control Lists and file
	flags from BSD-4.4 and Linux.
]]></para>
</sect3>

<sect3>
<title>gnu format</title>

<para>However, the current implementation of GNU tar, which is the reference
format for this description, was based on a draft release of the POSIX, where
parts of the header indicated as unused were used for GNU extensions. This
created an incompatible fork between the GNU and the POSIX implementation, that
incurred in subsequent modifications for the previously unused parts.</para>

<para>GNU tar 1.13.x format, derived from a draft of the POSIX standard. The
format supports extensions such as incremental archives and efficient storage
of sparse files, and is also able to deal with path names of unlimited
length</para>

<para><![CDATA[
- magic is 'ustar  '
Format 	UID 	File Size 	Path Name 	Devn
gnu 	1.8e19 	Unlimited 	Unlimited 	63
]]></para>

<table id="gnu-tar-header" xml:base="tables/table_gnu_tar_hdr.xml"><title>GNU tar header format</title><tgroup cols="3"><thead><row><entry>Offset</entry><entry>Size</entry><entry>Field</entry></row></thead><tbody><row><entry>0</entry><entry>100</entry><entry>File name</entry></row><row><entry>100</entry><entry>8</entry><entry>File mode</entry></row><row><entry>108</entry><entry>8</entry><entry>user id</entry></row><row><entry>116</entry><entry>8</entry><entry>group id</entry></row><row><entry>124</entry><entry>12</entry><entry>File size</entry></row><row><entry>136</entry><entry>12</entry><entry>mtime</entry></row><row><entry>148</entry><entry>8</entry><entry>Checksum</entry></row><row><entry>156</entry><entry>1</entry><entry>link flag</entry></row><row><entry>157</entry><entry>100</entry><entry>link name</entry></row><row><entry>257</entry><entry>8</entry><entry>magic</entry></row><row><entry>265</entry><entry>32</entry><entry>user name</entry></row><row><entry>297</entry><entry>32</entry><entry>group name</entry></row><row><entry>329</entry><entry>8</entry><entry>device major</entry></row><row><entry>337</entry><entry>8</entry><entry>device minor</entry></row><row><entry>345</entry><entry>12</entry><entry>access time</entry></row><row><entry>357</entry><entry>12</entry><entry>creation time</entry></row><row><entry>369</entry><entry>12</entry><entry>offset</entry></row><row><entry>381</entry><entry>4</entry><entry>longnames</entry></row><row><entry>386</entry><entry>4*12</entry><entry>sparse header</entry></row><row><entry>482</entry><entry>1</entry><entry>is extended?</entry></row><row><entry>483</entry><entry>12</entry><entry>real size</entry></row></tbody></tgroup></table>

<para><![CDATA[struct gnu_extended_header {
    struct sparse t_sp[SEH];/*   0  21 sparse structures (2 x 12 bytes) */
    char t_isextended;  /* 504  another extended header follows     */
};

<para>POSIX tar format uses fixed-sized unsigned octal strings to represent
numeric values. User and group IDs and device major and minor numbers have
unsigned 21-bit representations, and file sizes and times have unsigned 33-bit
representations. GNU tar generates POSIX representations when possible, but for
values outside the POSIX range it generates two's-complement base-256 strings:
uids, gids, and device numbers have signed 57-bit representations, and file
sizes and times have signed 89-bit representations. These representations are
an extension to POSIX tar format, so they are not universally portable.
\end{verbatim}

\begin{verbatim}

symbolic links: block naming the target of the link.

old tars have a limit of 100 characters. 
GNU tar: two different approaches to overcome this limit, using and extending a
format specified by a draft of some P1003.1. 
first way not successful: `@MaNgLeD@' file names

second approach `././@LongLink' and other tricks. better success

In theory, GNU tar should be able to handle file names of practically unlimited
length. 

But, being strictly POSIX, the limit was still 100 characters. For various
other purposes, GNU tar used areas left unassigned in the POSIX draft. POSIX
later revised P1003.1 ustar format by assigning previously unused header
fields, in such a way that the upper limit for file name length was raised
to 256 characters. However, the actual POSIX limit oscillates between 100
and 256, depending on the precise location of slashes in full file name
(this is rather ugly). Since GNU tar use the same fields for quite other
purposes, it became incompatible with the latest POSIX standards.

For longer or non-fitting file names, we plan to use yet another set of GNU
extensions, but this time, complying with the provisions POSIX offers for
extending the format, rather than conflicting with it. Whenever an archive
uses old GNU tar extension format or POSIX extensions, would it be for very
long file names or other specialities, this archive becomes non-portable to
other tar implementations. In fact, anything can happen. The most forgiving
tars will merely unpack the file using a wrong name, and maybe create
another file named something like `@LongName', with the true file name in
it. tars not protecting themselves may segment violate!

nothing sounds too difficult (but see below). I only have these few pages of
POSIX telling about `Extended tar Format' (P1003.1-1990 -- section 10.1.1),
and there are references to other parts of the standard I do not have, which
should normally enforce limitations on stored file names (I suspect things
like fixing what / and NUL means). There are also some points which the
standard does not make clear, Existing practice will then drive what I
should do.

There is a problem, however, which I did not intimately studied yet. Given a
truly POSIX archive with names having more than 100 characters, I guess that
GNU tar up to 1.11.8 will process it as if it were an old V7 archive, and be
fooled by some fields which are coded differently. So, the question is to
decide if the next generation of GNU tar should produce POSIX format by
default, whenever possible, producing archives older versions of GNU tar
might not be able to read correctly. I fear that we will have to suffer such
a choice one of these days, if we want GNU tar to go closer to POSIX. We can
rush it. Another possibility is to produce the current GNU tar format by
default for a few years, but have GNU tar versions from some 1.POSIX and up
able to recognize all three formats, and let older GNU tar fade out slowly.
Then, we could switch to producing POSIX format by default, with not much
harm to those still having (very old at that time) GNU tar versions prior to
1.POSIX.

GNU-format as it exists now can easily fool other POSIX tar, as it uses
fields which POSIX considers to be part of the file name prefix. I wonder if
it would not be a good idea, in the long run, to try changing GNU-format so
any added field (like ctime, atime, file offset in subsequent volumes, or
sparse file descriptions) be wholly and always pushed into an extension
block, instead of using space in the POSIX header block. I could manage to
do that portably between future GNU tars. So other POSIX tars might be at
least able to provide kind of correct listings for the archives produced by
GNU tar, if not able to process them otherwise.

Using these projected extensions might induce older tars to fail. We would
use the same approach as for POSIX. I'll put out a tar capable of reading
POSIXier, yet extended archives, but will not produce this format by
default, in GNU mode. 

In a few years, when newer GNU tars will have flooded
out tar 1.11.X and previous, we could switch to producing POSIXier extended
archives, with no real harm to users, as almost all existing GNU tars will
be ready to read POSIXier format. In fact, I'll do both changes at the same
time, in a few years, and just prepare tar for both changes, without
effecting them, from 1.POSIX. (Both changes: 1--using POSIX convention for
getting over 100 characters; 2--avoiding mangling POSIX headers for GNU
extensions, using only POSIX mandated extension techniques).

In a few years, when GNU tar will produce POSIX headers by default, --posix
will have a strong meaning and will disallow GNU extensions. But in the
meantime, for a long while, --posix in GNU tar will not disallow GNU
extensions like --label=archive-label (-V archive-label), --multi-volume
(-M), --sparse (-S), or very long file or link names. However, --posix with
GNU extensions will use POSIX headers with reserved-for-users extensions to
headers, and I will be curious to know how well or bad POSIX tars will react
to these.

GNU tar prior to 1.POSIX, and after 1.POSIX without --posix, generates and
checks `ustar ', with two suffixed spaces. This is sufficient for older GNU
tar not to recognize POSIX archives, and consequently, wrongly decide those
archives are in old V7 format. It is a useful bug for me, because GNU tar
has other POSIX incompatibilities, and I need to segregate GNU tar
semi-POSIX archives from truly POSIX archives, for GNU tar should be
somewhat compatible with itself, while migrating closer to latest POSIX
standards. So, I'll be very careful about how and when I will do the
correction. 

Archives are permitted to have more than one member with the same member
name. One way this situation can occur is if more than one version of a file
has been stored in the archive. 

In addition to entries describing archive members, an archive may contain
entries which tar itself uses to store information. See section 9.7
Including a Label in the Archive, for an example of such an archive entry.

Each file archived is represented by a header block which describes the
file, followed by zero or more blocks which give the contents of the file.
At the end of the archive file there may be a block filled with binary zeros
as an end-of-file marker. A reasonable system should write a block of zeros
at the end, but must not assume that such a block exists when reading an
archive.

All characters in header blocks are represented by using 8-bit characters in
the local variant of ASCII. Each field within the structure is contiguous;
that is, there is no padding used within the structure. Each character on
the archive medium is stored contiguously.


The name, linkname, magic, uname, and gname are null-terminated character
strings. All other fileds are zero-filled octal numbers in ASCII. Each
numeric field of width w contains w minus 2 digits, a space, and a null,
except size, and mtime, which do not contain the trailing null.

The name field is the file name of the file, with directory names (if any)
preceding the file name, separated by slashes.

The mode field provides nine bits specifying file permissions and three bits
to specify the Set UID, Set GID, and Save Text (sticky) modes. Values for
these bits are defined above. When special permissions are required to
create a file with a given mode, and the user restoring files from the
archive does not hold such permissions, the mode bit(s) specifying those
special permissions are ignored. Modes which are not supported by the
operating system restoring files from the archive will be ignored.
Unsupported modes should be faked up when creating or updating an archive;
e.g. the group permission could be copied from the other permission.

The uid and gid fields are the numeric user and group ID of the file owners,
respectively. If the operating system does not support numeric user or group
IDs, these fields should be ignored.

The size field is the size of the file in bytes; linked files are archived
with this field specified as zero. @quote-arg -xref{Modifiers}, in
particular the --incremental (-G) option.

The mtime field is the modification time of the file at the time it was
archived. It is the ASCII representation of the octal value of the last time
the file was modified, represented as an integer number of seconds since
January 1, 1970, 00:00 Coordinated Universal Time.


The typeflag field specifies the type of file archived. If a particular
implementation does not recognize or permit the specified type, the file
will be extracted as if it were a regular file. As this action occurs, tar
issues a warning to the standard error.

The atime and ctime fields are used in making incremental backups; they
store, respectively, the particular file's access time and last inode-change
time.

The offset is used by the --multi-volume (-M) option, when making a
multi-volume archive. The offset is number of bytes into the file that we
need to restart at to continue the file on the next tape, i.e., where we
store the location that a continued file is continued at.

The following fields were added to deal with sparse files. A file is sparse
if it takes in unallocated blocks which end up being represented as zeros,
i.e., no useful data. A test to see if a file is sparse is to look at the
number blocks allocated for it versus the number of characters in the file;
if there are fewer blocks allocated for the file than would normally be
allocated for a file of that size, then the file is sparse. This is the
method tar uses to detect a sparse file, and once such a file is detected,
it is treated differently from non-sparse files.

Sparse files are often dbm files, or other database-type files which have
data at some points and emptiness in the greater part of the file. Such
files can appear to be very large when an `ls -l' is done on them, when in
truth, there may be a very small amount of important data contained in the
file. It is thus undesirable to have tar think that it must back up this
entire file, as great quantities of room are wasted on empty blocks, which
can lead to running out of room on a tape far earlier than is necessary.
Thus, sparse files are dealt with so that these empty blocks are not written
to the tape. Instead, what is written to the tape is a description, of
sorts, of the sparse file: where the holes are, how big the holes are, and
how much data is found at the end of the hole. This way, the file takes up
potentially far less room on the tape, and when the file is extracted later
on, it will look exactly the way it looked beforehand. The following is a
description of the fields used to handle a sparse file:

The sp is an array of struct sparse. Each struct sparse contains two
12-character strings which represent an offset into the file and a number of
bytes to be written at that offset. The offset is absolute, and not relative
to the offset in preceding array element.

The header can hold four of these struct sparse at the moment; if more are
needed, they are not stored in the header.

The isextended flag is set when an extended_header is needed to deal with a
file. Note that this means that this flag can only be set when dealing with
a sparse file, and it is only set in the event that the description of the
file will not fit in the alloted room for sparse structures in the header.
In other words, an extended_header is needed.

The extended_header structure is used for sparse files which need more
sparse structures than can fit in the header. The header can fit 4 such
structures; if more are needed, the flag isextended gets set and the next
block is an extended_header.

Each extended_header structure contains an array of 21 sparse structures,
along with a similar isextended flag that the header had. There can be an
indeterminate number of such extended_headers to describe a sparse file.


A ... Z
    These are reserved for custom implementations. Some of these are used in
the GNU modified format, as described below.

Other values are reserved for specification in future revisions of the P1003
standard, and should not be used by any tar program.

The magic field indicates that this archive was output in the P1003 archive
format. If this field contains TMAGIC, the uname and gname fields will
contain the ASCII representation of the owner and group of the file
respectively. If found, the user and group IDs are used rather than the
values in the uid and gid fields.

For references, see ISO/IEC 9945-1:1990 or IEEE Std 1003.1-1990, pages
169-173 (section 10.1) for Archive/Interchange File Format; and IEEE Std
1003.2-1992, pages 380-388 (section 4.48) and pages 936-940 (section E.4.48)
for pax - Portable archive interchange. 

 8.5 GNU Extensions to the Archive Format

The GNU format uses additional file types to describe new types of files in
an archive. These are listed below.

\end{verbatim}

]]></para>
</sect3>

<sect3>
<title>Incompatibilities</title>

<para>Sun tar is an example of how a new file format can arise out of a
probable mistake, and the need of backward compatibility. Differently from
other implementations, Sun tar computed the checksum with a signed sum, instead
of unsigned as stated by the POSIX standard. As a result storing non-ASCII
filenames (having the eight bit set) caused the signed checksum to differ from
the unsigned one, leading to a non compatible header.  As a shipped product,
Sun tar was already used by customers to store their backups, and at that point
it was impossible to simply correct the implementation without providing some
sort of compatibility.</para>
</sect3>

<sect3>
<title>FIXME find details about</title>
<para><![CDATA[
This will write a special block identifying volume-label as the name of the
archive to the front of the archive which will be displayed when the archive
is listed

The BSD "tar" format is a superset of the V7/S3/S5 "tar" format.  It puts
out "funny" entries for directories; other "tar"s don't put out any
information about directories.  Reading a BSD "tar" tape on a non-BSD system
causes some warning messages about the directory entries, but all the files
and containing directories are created as before.  (Of course, if it's a
4.2BSD "tar" tape with symbolic links, it won't work if your system doesn't
support symbolic links.) 

ANSI tar ?

        v7tar		Old UNIX V7 tar format
		tar		Old BSD tar format
		star		Old star format from 1985
		gnutar		GNU tar format 1989 (violates POSIX)
		ustar		Standard POSIX.1-1988 tar format
		xstar		Extended standard tar (star 1994)
		xustar		'xstar' format without tar signature
		exustar		'xustar' format - always x-header
		pax		Extended POSIX.1-2001 standard tar
		suntar		Sun's extended pre-POSIX.1-2001

> According to the test suite documentation, POSIX 10.1.1-12(A) says
> that Fields mode, uid, gid, size, mtime, chksum, devmajor and
> devminor are leading zero-filled octal numbers in ASCII and are
> terminated by one or more space or null characters.

From looking at the archives created by GNUtar, I see the following
deviations:

-	Checksum field repeats a bug found in ancient TAR implementaions.
	This seems to be a rudiment from early tests done by John Gilmore
	in PD tar where he did try to run "cmp" on PD-tar vs. Sun-tar
	archives.

	This is a minor deviation and easy to fix.

-	The devmajor/devminor fields are missing if the file is not
	a block/char device - here we see non left zero filled fields.

	A minor deviation that is easy to fix.

-	The Magic Version field contains spaces instead of "00".

	This is just a proof that GNUtar is not POSIX.1-1990 compliant
	and should not be changed before GNUtar has been validated to
	create POSIX.1 compliant archives

Oh, it is not a private format.  It is roughly POSIX.  GNU tar already
supports old V7 format, a few BSD idiosyncrasies, and an obsolete draft
of POSIX ustar format. 


\end{verbatim}

]]></para>
</sect3>
</sect2>
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

<table id="cpio-ascii-header-format" xml:base="tables/table_cpio_ascii_hdr.xml"><title>cpio ASCII format header</title><tgroup cols="4"><thead><row><entry>Offset</entry><entry>Width</entry><entry>Field Name</entry><entry>Meaning</entry></row></thead><tbody><row><entry>0</entry><entry>6</entry><entry>magic</entry><entry>magic number 070707</entry></row><row><entry>6</entry><entry>6</entry><entry>dev</entry><entry>device where file is stored</entry></row><row><entry>12</entry><entry>6</entry><entry>ino</entry><entry>inode number</entry></row><row><entry>18</entry><entry>6</entry><entry>mode</entry><entry>file mode</entry></row><row><entry>24</entry><entry>6</entry><entry>uid</entry><entry>owner user ID</entry></row><row><entry>30</entry><entry>6</entry><entry>gid</entry><entry>owner group ID</entry></row><row><entry>36</entry><entry>6</entry><entry>nlink</entry><entry>number of links to file</entry></row><row><entry>42</entry><entry>6</entry><entry>rdev</entry><entry>device major/minor (if special file)</entry></row><row><entry>48</entry><entry>11</entry><entry>mtime</entry><entry>modify time of file</entry></row><row><entry>59</entry><entry>6</entry><entry>namesize</entry><entry>file name length</entry></row><row><entry>65</entry><entry>11</entry><entry>filesize</entry><entry>file length</entry></row></tbody></tgroup></table>

<para>In the ASCII style, after the header we find the filename as a
variable length NUL-terminated string (namesize bytes long, including the
terminator) and the variable length file contents (filesize bytes).  Values in
the header are supposed to be compatible with values returned by the UNIX
<function>stat(2)</function> system call, expecially the bitmask stored in file
mode, but unfortunately the meaning of bits is slightly different on different
unix flavours.  <structfield>rdev</structfield> is used only for block and
character devices.  <structfield>filesize</structfield> is zero in case of
special files and directories.</para>

<table id="cpio-binary-header-format" xml:base="tables/table_cpio_binary_hdr.xml"><title>cpio binary format header</title><tgroup cols="3"><thead><row><entry>Offset</entry><entry>Width</entry><entry>Field Name</entry></row></thead><tbody><row><entry>0</entry><entry>2</entry><entry>magic</entry></row><row><entry>2</entry><entry>2</entry><entry>dev</entry></row><row><entry>4</entry><entry>2</entry><entry>ino</entry></row><row><entry>6</entry><entry>2</entry><entry>mode</entry></row><row><entry>8</entry><entry>2</entry><entry>uid</entry></row><row><entry>10</entry><entry>2</entry><entry>gid</entry></row><row><entry>12</entry><entry>2</entry><entry>nlink</entry></row><row><entry>14</entry><entry>2</entry><entry>rdev</entry></row><row><entry>16</entry><entry>4</entry><entry>mtime</entry></row><row><entry>20</entry><entry>2</entry><entry>namesize</entry></row><row><entry>22</entry><entry>4</entry><entry>filesize</entry></row></tbody></tgroup></table>

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

<table id="cpio-filemode-flags" xml:base="tables/table_cpio_filemode_flags.xml"><title>cpio file mode flags</title><tgroup cols="3"><thead><row><entry>Flag name</entry><entry>Flag value</entry><entry>Meaning</entry></row></thead><tbody><row><entry>C_IRUSR</entry><entry>000400</entry><entry>Readable by owner</entry></row><row><entry>C_IWUSR</entry><entry>000200</entry><entry>Writable by owner</entry></row><row><entry>C_IXUSR</entry><entry>000100</entry><entry>Executable by owner</entry></row><row><entry>C_IRGRP</entry><entry>000040</entry><entry>Readable by group</entry></row><row><entry>C_IWGRP</entry><entry>000020</entry><entry>Writable by group</entry></row><row><entry>C_IXGRP</entry><entry>000010</entry><entry>Executable by group</entry></row><row><entry>C_IROTH</entry><entry>000004</entry><entry>Readable by others</entry></row><row><entry>C_IWOTH</entry><entry>000002</entry><entry>Writable by others</entry></row><row><entry>C_IXOTH</entry><entry>000001</entry><entry>Executable by others</entry></row><row><entry>C_ISUID</entry><entry>004000</entry><entry>Set-UID</entry></row><row><entry>C_ISGID</entry><entry>002000</entry><entry>Set-GID</entry></row><row><entry>C_ISVTX</entry><entry>001000</entry><entry>Sticky bit</entry></row><row><entry>C_ISBLK</entry><entry>060000</entry><entry>Block device</entry></row><row><entry>C_ISCHR</entry><entry>020000</entry><entry>Character device</entry></row><row><entry>C_ISDIR</entry><entry>040000</entry><entry>Directory</entry></row><row><entry>C_ISFIFO</entry><entry>010000</entry><entry>Named pipe (FIFO)</entry></row><row><entry>C_ISSOCK</entry><entry>0140000</entry><entry>Unix domain socket</entry></row><row><entry>C_ISLNK</entry><entry>0120000</entry><entry>Symbolic link</entry></row><row><entry>C_ISREG</entry><entry>0100000</entry><entry>Regular file</entry></row></tbody></tgroup></table>

<para>Several UNIX versions use 32 bits to store some of the values returned by
<function>stat(2)</function> and this proved particularly problematic for the
inode number because this value is needed to find out hard links (hard links
are regular files but they share the same inode on a different file name).  The
binary format has just 16 bits available and the original portable ASCII format
has 18, which is not enough anyway.  To fix this problem a new portable format
has been designed, using hexadecimal representation instead of octal and two
more bytes per field.</para>

<table id="cpio-new-ascii-header-format" xml:base="tables/table_cpio_new_hdr.xml"><title>cpio new ASCII and CRC format headers</title><tgroup cols="4"><thead><row><entry>Offset</entry><entry>Bytes</entry><entry>Field Name</entry><entry>Notes</entry></row></thead><tbody><row><entry>0</entry><entry>6</entry><entry>magic</entry><entry>"070701" for new portable format, "070702" for CRC format</entry></row><row><entry>8</entry><entry>8</entry><entry>ino</entry><entry/></row><row><entry>16</entry><entry>8</entry><entry>mode</entry><entry/></row><row><entry>24</entry><entry>8</entry><entry>uid</entry><entry/></row><row><entry>32</entry><entry>8</entry><entry>gid</entry><entry/></row><row><entry>40</entry><entry>8</entry><entry>nlink</entry><entry/></row><row><entry>48</entry><entry>8</entry><entry>mtime</entry><entry/></row><row><entry>56</entry><entry>8</entry><entry>filesize</entry><entry>must be 0 for FIFOs and directories</entry></row><row><entry>64</entry><entry>8</entry><entry>maj</entry><entry/></row><row><entry>72</entry><entry>8</entry><entry>maj</entry><entry/></row><row><entry>80</entry><entry>8</entry><entry>rmaj</entry><entry>only valid for character and block special files</entry></row><row><entry>88</entry><entry>8</entry><entry>rmin</entry><entry>only valid for character and block special files</entry></row><row><entry>96</entry><entry>8</entry><entry>namesize</entry><entry>rounded up to multiple of four, includes terminating NULs in pathname</entry></row><row><entry>104</entry><entry>8</entry><entry>checksum</entry><entry>only used in CRC format, must be 0 for new portable format</entry></row></tbody></tgroup></table>

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
</sect1>

<sect1>
<title>Simple compression</title>
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
         |...compressed blocks...| (more--&gt;)
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
<!--xi:include href="bzip2.xml"/-->
</sect1>

<sect1>
<title>Compressed storage</title>
<sect2><title>7zip</title></sect2>
<sect2><title>ace</title></sect2>
<sect2><title>arj</title></sect2>
<sect2><title>lha</title>

<para>
FIXME : verbatim
File extension:	.lzh, .lha
MIME type:	application/x-lzh-compressed
Developed by:	Haruyasu Yoshizaki
Type of format:	Data compression

LHA is a freeware compression utility and associated file format. It was created in 1988 by Haruyasu Yoshizaki (&#x5409;&#x5D0E;&#x6804;&#x6CF0; Yoshizaki Haruyasu?), and originally named LHarc. A complete rewrite of LHarc, tentatively named LHx, was eventually released as LH. It was then renamed to LHA to avoid conflicting with the then-new MS-DOS 5.0 LH ("load high") command.
Although no longer much used in the West, LHA remains popular in Japan. It was used by id Software to compress installation files for their earlier games, such as Doom. LHA has been ported to many operating systems and is the main archiving format on Amiga computers. This is due to Aminet, the world's largest archive of Amiga related software and files, standardising on Stefan Boberg's implementation of LHA on the Amiga. Microsoft has released a Windows XP add-on, Microsoft Compression Folder for LHA archives, for the Japanese market only[1].

 	Aeco Systems
September 1996


Multi-disk span for LZH Specification Version 1.0
--------------------------------------------------

Status of this Memo
-------------------
This memo provides information for the Internet community. It does not specify an Internet standard. Distribution of this memo is unlimited.

Abstract
--------
Multi-disk span is the process of a taking a file, optionally compressing the data and splitting it up into multiple segments to fit available space on the media. This documents describes the additional fields to the LZH format required to support this feature. Pseudo code for it&#x2019;s implementation is also presented.
Knowledge about the LZH format is assumed.
LZH format
----------
In brief, LZH file is laid out in the following manner.
+------------+
| LZH header |
+------------+
| compressed |
| data       |
+------------+
| LZH header |
+------------+
| compressed |
| data       |
+------------+
...

The LZH header is described in this pseudo C struct below.

struct LZH {
  byte header_size;
  byte header_checksum;
  char method[5];
  long packed_size;
  long original_size;
  long time_stamp;
  short attribute;
  byte header_level;
  byte name_length;
  char name[...];
  }
Extensions to the header is defined by using the header_level. 3 header_levels have been defined; 0, 1 and 2.

Header_levels 1 and 2 supports additional fields that can be arbitrarily defined and bypassed by unknown LZH processor using this format.

struct additional_field {
  short field_size;
  byte field_id;
  ... // additional fields
  }
field_id is a unique value to identify a particular piece of information. Additions to LZH to support multi-disk span is built using this flexible extension.
The additional field_id(s) thus far defined are as follows:
0x00 Header CRC
0x01 Filename
0x02 Directory
0x40 DOS attribute
0x50-0x54 Unix fields

Multi-disk addition
-------------------
The multi-disk addition field_id is defined as:
0x39 Multi-disk field

In an LZH archive, these header information is laid out before each actual compressed file information. The multi-disk field (MDF) is only needed when a compressed file is to be spanned across multiple media disk. At any other time, this information is optional and holds no additional information. The MDF is defined as follows:

struct MDF {
byte span_mode;
long beginning_offset;
long size_of_run;
}

span_mode: This identifies the mode of this segment of file. The values are:
#define SPAN_COMPLETE 0
#define SPAN_MORE 1
#define SPAN_LAST 2

SPAN_COMPLETE. This specifies that the information following this header contains a complete (optionally compressed) file. This is often unused because MDF is not needed in these cases. In an unsplit file, the header information and format should follow the standard LZH format.

SPAN_MORE. This specifies that the information following this header is incomplete. The uncompressor needs to concatenate this segment with information from the following volume. It should continue to do that until it sees a volume with a header information that contains span_mode SPAN_LAST.

SPAN_LAST. This specifies that the information following this header is the last segment of the (optionally compressed) file.


beginning_offset: This value specifies the location in bytes of where this segment (run) of information will fit into.

size_of_run: This is the size of this segment of information.


The illustration below contain two volumes with two compressed files, one of them split between the two volumes. "File 1" is compressed and fits within the first volume. "File 2" is a file 100 bytes long compressed to 90 bytes. The first 50 bytes of which resides on the first volume and the last 40 bytes on the next.

Volume 1
+--------------+
| +----------+ |
| |LZH header| |  MDF not needed
| +----------+ |  header unchanged from non-spanned versions of LZH
| | File 1   | |
| |          | |
| |          | |
| +----------+ |
|              |
| +----------+ |  span_mode = SPAN_MORE
| |LZH header| |  beginning_offset = 0
| +----------+ |  size_of_run = 50
| | File 2   | |
| | split    | |
| |          | |
+--------------+

Volume 2
+--------------+
| +----------+ |  span_mode = SPAN_LAST
| |LZH header| |  beginning_offset = 50
| +----------+ |  size_of_run = 40
| | File 2   | |
| |          | |
| |          | |
| |          | |
| +----------+ |
| +----------+ |
| | [0]      | | end of volumes, a byte with value zero (0)
| +----------+ |
+--------------+
Termination
-----------
In addition to the above changes, the compressor must before closing the file after writing the last volume, write a null byte at the end of the file. This byte serves to inform the decompressor that this is the last volume and no other comes after it.

This end of volume byte is needed to tell the decompressor when to stop prompting for the next volume.
This termination byte is optional, as the decompressor may also stop when it has completed a file, i.e., see SPAN_LAST or just a regular file with MDF. However if the end of this completed file coincides with an end of volume, there would be not way for the compressor detect that the following volumes and prompt for them.
This termination byte is a way around this potential bug.

Note that this null byte coincides with header_size in the LZH header.


Pseudo code for a sample implementation
---------------------------------------

boolean spanned = false;
while(file_available()) {
compress file();
if(size_of_compressed_file &gt; available_space()) {

  while(size_of_compressed_file) {
    size_to_write = available_space();

    construct_header_with_MDF(size_to_write);
    write_header();
    write_data(size_to_write);

    size_of_compressed_file -= size_to_write;

    prompt_for_next_volume();

    spanned = true;
    }
  }
else {
  construct_header_without_MDF(size_of_compressed_file);
  write_header();
  write_data(size_of_compressed_file);
  }
}
if(spanned)
write_null_byte();
 
</para>
</sect2>
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

<table id="zip-orig-local-file-header-format" xml:base="tables/table_zip_orig_local_file_hdr.xml"><title>Local file header in original zip format</title><tgroup cols="3"><thead><row><entry>Offset</entry><entry>Bytes</entry><entry>Field</entry></row></thead><tbody><row><entry>0</entry><entry>4</entry><entry>Magic signature (0x04034b50)</entry></row><row><entry>4</entry><entry>2</entry><entry>Version needed to extract</entry></row><row><entry>6</entry><entry>2</entry><entry>General purpose bit flag</entry></row><row><entry>8</entry><entry>2</entry><entry>Compression method</entry></row><row><entry>10</entry><entry>2</entry><entry>Last modification time</entry></row><row><entry>12</entry><entry>2</entry><entry>Last modification date</entry></row><row><entry>14</entry><entry>4</entry><entry>CRC-32</entry></row><row><entry>18</entry><entry>4</entry><entry>Compressed size</entry></row><row><entry>22</entry><entry>4</entry><entry>Uncompressed size</entry></row><row><entry>26</entry><entry>2</entry><entry>File name length (fnl)</entry></row><row><entry>28</entry><entry>2</entry><entry>Extra field length (efl)</entry></row><row><entry>30</entry><entry>fnl</entry><entry>File name (variable size, fnl bytes)</entry></row><row><entry>30+fnl</entry><entry>efl</entry><entry>Extra field (variable size, efl bytes)</entry></row></tbody></tgroup></table>

<para>The <structfield>Version needed to extract</structfield> field is split
in two parts: lower byte indicates the minimum version number of the software
required to extract this file, encoded as 10*major+minor; upper byte indicates
the host operating system for this file, for example useful to determine line
record format for text files.</para>

<table id="zip-os-values" xml:base="tables/table_zip_os_values.xml"><title>Zip operating system codes</title><tgroup cols="2"><thead><row><entry>Value</entry><entry>Meaning</entry></row></thead><tbody><row><entry>0</entry><entry>FAT file system (DOS, OS/2, NT)</entry></row><row><entry>1</entry><entry>Amiga</entry></row><row><entry>2</entry><entry>VMS (VAX or Alpha AXP)</entry></row><row><entry>3</entry><entry>Unix</entry></row><row><entry>4</entry><entry>VM/CMS</entry></row><row><entry>5</entry><entry>Atari</entry></row><row><entry>6</entry><entry>HPFS file system (OS/2, NT 3.x)</entry></row><row><entry>7</entry><entry>Macintosh</entry></row><row><entry>8</entry><entry>Z-System</entry></row><row><entry>9</entry><entry>CP/M</entry></row><row><entry>10</entry><entry>TOPS-20</entry></row><row><entry>11</entry><entry>NTFS file system (NT)</entry></row><row><entry>12</entry><entry>SMS/QDOS</entry></row><row><entry>13</entry><entry>Acorn RISC OS</entry></row><row><entry>14</entry><entry>VFAT file system (Win95, NT)</entry></row><row><entry>15</entry><entry>MVS</entry></row><row><entry>16</entry><entry>BeOS (BeBox or PowerMac)</entry></row><row><entry>17</entry><entry>Tandem</entry></row></tbody></tgroup></table>

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

<table id="zip-orig-central-file-header-format" xml:base="tables/table_zip_orig_central_file_hdr.xml"><title>Zip central file header</title><tgroup cols="3"><thead><row><entry>Offset</entry><entry>Bytes</entry><entry>Field</entry></row></thead><tbody><row><entry>0</entry><entry>4</entry><entry>Magic signature (0x02014b50)</entry></row><row><entry>4</entry><entry>2</entry><entry>Version made by</entry></row><row><entry>6</entry><entry>2</entry><entry>Version needed to extract</entry></row><row><entry>8</entry><entry>2</entry><entry>General purpose bit flag</entry></row><row><entry>10</entry><entry>2</entry><entry>Compression method</entry></row><row><entry>12</entry><entry>2</entry><entry>Last modification time</entry></row><row><entry>14</entry><entry>2</entry><entry>Last modification date</entry></row><row><entry>16</entry><entry>4</entry><entry>CRC-32</entry></row><row><entry>20</entry><entry>4</entry><entry>Compressed size</entry></row><row><entry>24</entry><entry>4</entry><entry>Uncompressed size</entry></row><row><entry>28</entry><entry>2</entry><entry>File name length (fnl)</entry></row><row><entry>30</entry><entry>2</entry><entry>Extra field length (efl)</entry></row><row><entry>32</entry><entry>2</entry><entry>File comment length (fcl)</entry></row><row><entry>34</entry><entry>2</entry><entry>Disk number start</entry></row><row><entry>36</entry><entry>2</entry><entry>Internal file attributes</entry></row><row><entry>38</entry><entry>4</entry><entry>External file attributes</entry></row><row><entry>42</entry><entry>4</entry><entry>Relative offset of local header</entry></row><row><entry>46</entry><entry>fnl</entry><entry>File name (variable size, fnl bytes)</entry></row><row><entry>46+fnl</entry><entry>efl</entry><entry>Extra field (variable size, efl bytes)</entry></row><row><entry>46+fnl+efl</entry><entry>cfl</entry><entry>File comment (variable size, cfl bytes)</entry></row></tbody></tgroup></table>

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
</sect1>

<sect1>
<title>Packaging</title>
<sect2><title>autopackage</title></sect2>
<sect2><title>jar</title></sect2>
<sect2><title>rpm</title></sect2>
</sect1>
</chapter>
