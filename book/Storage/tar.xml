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

<xi:include href="tables/table_tar_v7_hdr.xml"/>

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

<xi:include href="tables/table_ustar_hdr.xml"/>

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
  <remark>empty block->cksum == 0, so it is not always considered space
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

<xi:include href="tables/table_gnu_tar_hdr.xml"/>

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
