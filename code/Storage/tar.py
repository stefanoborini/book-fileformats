import sys
import buffer

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

class TarHeader:
    def __init__(self, data):
        self.filename = data.getString(100)
        self.fileMode = data.getString(8)
        self.ownerUserID = int(data.getString(8),8)
        self.ownerGroupID = int(data.getString(8),8)
        self.fileSize = int(data.getString(12),8)
        self.lastModificationTime = int(data.getString(12),8)
        self.checksum = int(data.getString(8),8)
        self.linkIndicator = data.getString(1)
        self.linkedFilename = data.getString(100)
    def printInfo(self):
        varlist = [ ("filename", None ),
          ("fileMode" , None ),
          ("ownerUserID" , None ),
          ("ownerGroupID" , None ),
          ("fileSize" , None ),
          ("lastModificationTime", None ),
          ("checksum" , None ),
          ("linkIndicator", None ),
          ("linkedFilename", None ) ]

        dumpVars(self, varlist)

class TarFile:
    def __init__(self,filename):
        self.__filename = filename
        self.__contents = buffer.Buffer(file(filename,"r").read())
        
        header = TarHeader(self.__contents)
        header.printInfo()
        self.__contents.setCurPos(512)
        header = TarHeader(self.__contents)
        header.printInfo()
        
if __name__ == "__main__":
    
    TarFile(sys.argv[1])
        
