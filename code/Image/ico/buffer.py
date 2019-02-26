import struct

def sizeof(type):
     return struct.calcsize(type)

PAD = "x"
CHAR = "c"
SIGNED_BYTE  = "b"
UBYTE = "B"
SHORT = "h"
USHORT ="H"
INT = "i"
UINT = "I"
LONG = 'l'
ULONG = "L"
FLOAT = "f"
DOUBLE = "d"
def STRING(length):
    return str(length)+"s"
        
LITTLE_ENDIAN="<"
BIG_ENDIAN=">"

class Buffer:
    
    def __init__(self, buffer):
        self.__buffer = buffer
        self.__pos = 0
        self.setEndianness(LITTLE_ENDIAN)

    def fillDict(self, d):
        retdict = dict()
        for key, value in d.items():
            retdict[key] = self.self.getDatatype(value)
        return retdict
            
    def getChar(self):
        return self.getDatatype(CHAR)
    def getByte(self):
        return self.getDatatype(BYTE)
    def getUByte(self):
        return self.getDatatype(UBYTE)
    def getShort(self):
        return self.getDatatype(SHORT)
    def getUShort(self):
        return self.getDatatype(USHORT)
    def getInt(self):
        return self.getDatatype(INT)
    def getUInt(self):
        return self.getDatatype(UINT)
    def getLong(self):
        return self.getDatatype(LONG)
    def getULong(self):
        return self.getDatatype(ULONG)
    def getFloat(self):
        return self.getDatatype(FLOAT)
    def getDouble(self):
        return self.getDatatype(DOUBLE)
    def getString(self,length):
        return self.getDatatype(STRING(length))
    def getDatatype(self,datatype):
        val = struct.unpack(self.__endianness+datatype,self.__buffer[self.__pos:self.__pos+sizeof(datatype)])[0]
        self.__pos += sizeof(datatype)
        return val
    def setEndianness(self, endianness):
        if endianness == LITTLE_ENDIAN or endianness == BIG_ENDIAN:
            self.__endianness = endianness
    def curPos(self):
        return self.__pos
    def setCurPos(self, pos):
        self.__pos = pos
    def rewind(self):
        self.setCurPos(0)
