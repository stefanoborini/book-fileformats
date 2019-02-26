from buffer import *
import struct
import sys

def dumpVars(object, varlist):
    print "Object "+object.__class__.__name__
    maxlen = 0
    for name, expected in varlist:
        maxlen = max(maxlen, len(name))

    for name, expected in varlist:
        padding = maxlen - len(name) + 2
        if expected is not None:
            print " "+name+" "*padding+" = "+str(object.__dict__.get(name))+" (expected "+str(expected)+")"
        else:
            print " "+name+" "*padding+" = "+str(object.__dict__.get(name))


#typdef struct
#{
#   BITMAPINFOHEADER   icHeader;      // DIB header
#   RGBQUAD         icColors[1];   // Color table
#   BYTE            icXOR[1];      // DIB bits for XOR mask
#   BYTE            icAND[1];      // DIB bits for AND mask
#} ICONIMAGE, *LPICONIMAGE;



class ICONDIR:
    def __init__(self,buffer):
        
        self.idReserved = buffer.getUShort()
        self.idType = buffer.getUShort()
        self.idCount = buffer.getUShort()
      
        self.idEntries=[]
        for i in xrange(self.idCount):
            iconentry = ICONDIRENTRY(buffer)
            self.idEntries.append(iconentry)

        self.images=[]
        for direntry in self.idEntries:
            buffer.setCurPos(direntry.dwImageOffset)
            self.images.append(ICONIMAGE(buffer))

    def printInfo(self):
        varlist =[ ("idReserved",0),
                  ("idType", 1),
                  ("idCount", None) ]

        dumpVars(self, varlist)
        for entry in self.idEntries:
            entry.printInfo()
        for image in self.images:
            image.printInfo()

class ICONDIRENTRY:
    def __init__(self, buffer):
        self.bWidth = buffer.getUByte()
        self.bHeight = buffer.getUByte()
        self.bColorCount = buffer.getUByte()
        self.bReserved = buffer.getUByte()
        self.wPlanes = buffer.getUShort()
        self.wBitCount = buffer.getUShort()
        self.dwBytesInRes = buffer.getUInt()
        self.dwImageOffset = buffer.getUInt()
    def printInfo(self):
        varlist = [ ("bWidth", None),
                    ("bHeight", None),
                    ("bColorCount", None),
                    ("bReserved", None),
                    ("wPlanes", None),
                    ("wBitCount", None),
                    ("dwBytesInRes", None),
                    ("dwImageOffset", None) ]

        dumpVars(self, varlist)

class ICONIMAGE:
    def __init__(self, buffer):
        self.icHeader = BITMAPINFOHEADER(buffer)
    def printInfo(self):
        self.icHeader.printInfo()

class BITMAPINFOHEADER:
    def __init__(self, buffer):
        self.biSize = buffer.getUInt()
        self.biWidth = buffer.getULong()
        self.biHeight = buffer.getULong()
        self.biPlanes = buffer.getUShort()
        self.biBitCount = buffer.getUShort()
        self.biCompression = buffer.getUInt()
        self.biSizeImage = buffer.getUInt()
        self.biXPelsPerMeter = buffer.getULong()
        self.biYPelsPerMeter = buffer.getULong()
        self.biClrUsed = buffer.getUInt()
        self.biClrImportant = buffer.getUInt()
    def printInfo(self):
        varlist = [ ("biSize",None),
                    ("biWidth",None),
                    ("biHeight",None),
                    ("biPlanes",None),
                    ("biBitCount",None),
                    ("biCompression",0),
                    ("biSizeImage",None),
                    ("biXPelsPerMeter",0),
                    ("biYPelsPerMeter",0),
                    ("biClrUsed",0),
                    ("biClrImportant",0)
                  ] 
        dumpVars(self, varlist)
         
class IcoFile:
    def __init__(self, filename):
        self.__filename = filename
        
        self.__contents = Buffer(file(filename, "r").read())

        idir = ICONDIR(self.__contents)
        idir.printInfo()

                
if __name__ == "__main__":
    
    IcoFile(sys.argv[1])

