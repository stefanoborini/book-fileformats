<sect2><title>lha</title>

<para>
FIXME : verbatim
File extension:	.lzh, .lha
MIME type:	application/x-lzh-compressed
Developed by:	Haruyasu Yoshizaki
Type of format:	Data compression

LHA is a freeware compression utility and associated file format. It was created in 1988 by Haruyasu Yoshizaki (吉崎栄泰 Yoshizaki Haruyasu?), and originally named LHarc. A complete rewrite of LHarc, tentatively named LHx, was eventually released as LH. It was then renamed to LHA to avoid conflicting with the then-new MS-DOS 5.0 LH ("load high") command.
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
Multi-disk span is the process of a taking a file, optionally compressing the data and splitting it up into multiple segments to fit available space on the media. This documents describes the additional fields to the LZH format required to support this feature. Pseudo code for it’s implementation is also presented.
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
if(size_of_compressed_file > available_space()) {

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
