<sect2><title>ICO</title>
<para>

The ico file format

BITMAPINFOHEADER

The actual bitmap data in the DIB begins at the tail end of the RGBQUAD
structures. While most Windows functions refer vertical dimensions from the
top down, using the top as 0, bitmap data is stored in a DIB with the lowest
scan line at the start of the bitmapped data block. Between the end of each
line and the beginning of the next, you'll find some filler bytes which are
used to align the start of the line to an address divisible by 4. Here's how
to calculate the number of bytes in a scanline, which may very well be
different from the number of pixels of width in the image:

BITMAPV4HEADER




BITMAPINFOHEADER

Format information for device-independent bitmaps

The BITMAPINFOHEADER structure stores information about the dimensions and
color palette of a device independent bitmap (DIB) used by Windows 3.0 and
newer.

       typedef struct tagBITMAPINFOHEADER{
          DWORD  biSize;
          DWORD  biWidth;
          DWORD  biHeight;
          WORD   biPlanes;
          WORD   biBitCount
          DWORD  biCompression;
          DWORD  biSizeImage;
          DWORD  biXPelsPerMeter;
          DWORD  biYPelsPerMeter;
          DWORD  biClrUsed;
          DWORD  biClrImportant;

       } BITMAPINFOHEADER;

The BITMAPINFOHEADER structure has the following members:
Field 	Type 	Description
biSize 	DWORD 	Specifies the number of bytes required by the
BITMAPINFOHEADER structure.
biWidth 	DWORD 	Specifies the width of the bitmap in pixels.
biHeight 	DWORD 	Specifies the height of the bitmap in pixels. If
biHeight is positive, the bitmap is a "bottom-up" DIB and its origin is the
lower left corner. If biHeight is negative, the bitmap is a "top-down" DIB



and its origin is the upper left corner. Note that many DaVinci functions
only support bottom-up bitmaps (biHeight >= 0).
biPlanes 	WORD 	Specifies the number of color planes on the target
device. In most cases this value must be set to 1.

DaVinci extension: For 48-bit DIBs (bitmaps with 16 bits per color value of
resolution), biPlanes should be set to 2.
biBitCount 	WORD 	Specifies the number of bits per pixels. This value must
be 1, 4, 8 or 24 in the 16 bit version; values of 16 or 32 may also be used
in the 32 bit version of DaVinci.
biCompression 	DWORD 	Specifies the compression type for a compressed
bitmap. The following values are specified as standard for Windows bitmaps:
		Value Importance

BI\_RGB Standard Windows bitmap; not compressed.

BI\_RLE4 RLE (Run Length Encoded) 4bpp (16 color) image. See the following
section on bitmap compression formats for more information.

BI\_RLE8 RLE (Run Length Encoded) 8bpp (256 color) image. See the following
section on bitmap compression formats for more information.
biSizeImage 	DWORD 	Specifies the size of the bitmap data section of the
image (the actual pixel data, excluding BITMAPINFOHEADER and RGBQUAD
structures).
biXPelsPerMeter 	DWORD 	Specifies the horizontal resolution of the
target device in pixels per metre. Applications often use this value to
select the resource bitmap that best matches the characteristics of the
current device.
biYPelsPerMeter 	DWORD 	Specifies the vertical resolution, in pixels per
metre, of the target device for the bitmap.
biClrUsed 	DWORD 	Specifies the actual number of color indices in the
color table used by the bitmap. If this value is zero, the bitmap uses the
maximum number of colors corresponding to the value of the biBitCount member
for the compression mode specified by biCompression.

If biClrUsed is nonzero and the biBitCount member is less than 16, the
biClrUsed member specifies the actual number of colors the graphics engine
or device driver accesses. If biBitCount is 16 or greater, then biClrUsed
member specifies the size of the color table. This can be used to optimize
performance of Windows color palettes. If biBitCount equals 16 or 32, the
optimal color palette starts immediately following the three doubleword
masks.

If the bitmap is a packed bitmap (a bitmap in which the bitmap's pixel data
array immediately follows the BITMAPINFO header and which is referenced by a
single pointer), the biClrUsed member must be either 0 or the actual size of
the color table.
biClrImportant 	DWORD 	Specifies the number of color indices that are
considered important for displaying the bitmap. If this value is zero, all
colors are important.

Remarks

The BITMAPINFO structure combines the BITMAPINFOHEADER structure and a color
table to provide a complete definition of the dimensions and colors of a
DIB. For more information about DIBs, see the description of the BITMAPINFO
data structure in the WinAPI helpfiles.

An application should use the information stored in the biSize member to
locate the color table in a BITMAPINFO structure, as follows:

    pColor = ((LPSTR) pBitmapInfo + (UINT) (pBitmapInfo -> biSize))

A Windows DIB consists of two different parts: the BITMAPINFO data structure
containing the bitmap's image dimensions and color table, and a byte field
or data array representing the pixels that make up the image itself. The
bits in this field are packed, but each screen line (each vertical row of
pixels) must be filled with zeros as needed in order to end at a LONG limit.
64 KB segment boundaries for 16 bit applications can appear within one pixel
of the graphic.

Note that the origin ("starting point") for DIBs is the lower left corner of
the bitmap, while the origin of a DDB is the upper left corner.
biBitCount

The biBitCount member of the BITMAPINFOHEADER structure determines the
number of bits in each pixel and also defines the maximum number of colors
which may be used in the bitmap. This member may use the following values:

Value Importance

1 The bitmap is monochrome and the bmciColors member of the BITMAPINFO
structure must contain two entries. Every bit in the bitmap represents a
pixel. If the bit is deleted, the pixel is displayed with the color of first
entry in the table bmciColors. If the bit is set, the pixel has the color of
second entry in the table. The bits are interpreted in the order
7,6,5,4,3,2,1,0.

4 The bitmap has a maximum of 16 colors and the bmciColors member of the
BITMAPINFO structure contains 16 entries. Every pixel in the bitmap is
represented by an index four bits long which defines which color in the
bitmap's palette will be used by that pixel. If the first byte in the bitmap
is 0x1F, for example, then the first pixel will be the color in the second
table entry (palette index 1) and the second pixel will be the color in the
sixteenth table entry (palette index 15).

8 The bitmap has a maximum of 256 colors and the bmciColors member of the
BITMAPINFO structure can contain a maximum of 256 entries. Every byte
represents the color in the palette index for an individual pixel.

16 (Only defined for Windows NT 3.5+, Windows 95/98 and Video for Windows.)
The bitmap can have a maximum of 32,767 colors. In this case the bmciColors
member will be left empty. Every two bytes in the bitmaps data field
represent the relative intensities of red, green and blue (RGB) for a
specific pixel.

24 The bitmap can have a maximum of 2\^24 (usually referred to, though not
entirely accurately, as 16 million) colors. The bmciColors member is left
empty. Every three bytes in the bitmaps data field represent the relative
intensities of blue, green and red for (BGR) every pixel. The order of the
bytes is blue, green, red.

32 The bitmap can have a maximum of 2\^24 colors (see above). The bmciColors
field is once again left empty. Every four bytes in the bitmaps data field
represent the relative intensities of blue, green and red (BGR) for a given
pixel, and the fourth byte, which is not used, is usually set to 0.
Notes

The biClrUsed member of the structure BITMAPINFOHEADER specifies the actual
number of color indices currently in use in that images palette.

Colors listed in the bmiColors table should appear in order of their
importance.
Bitmap compression formats

Windows provides its own internal bitmap compression formats for 4- and
8-bit-per-pixel images. The RLE (run-length encoding) compression used by
Windows will often, but not always, reduce the storage and main memory
requirement for bitmaps. DaVinci functions do not support Windows RLE image
formats directly, however. When images are imported, DaVinci will instead
call its own internal decompression routines and return an uncompressed DIB.
See also:

BITMAPINFOHEADER

BITMAPINFO


http://msdn.microsoft.com/library/default.asp?url=/library/en-us/dnwui/html/msdn\_icons.asp
http://msdn.microsoft.com/library/default.asp?url=/library/en-us/gdi/bitmaps\_1rw2.asp

</para>
</sect2>
