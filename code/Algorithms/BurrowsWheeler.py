class BurrowsWheeler:
    def __init__(self):
        pass
    def encode(self, string):
        M = []
        L = list(string)
        for i in xrange(len(L)):
            M.append("".join(L))
            L.append(L.pop(0))
        
        M.sort()
        index = M.index(string)
        
        encoded = []
        for row_index in xrange(len(M)):
            encoded.append(M[row_index][-1])

        return ("".join(encoded), index)
        
    def decode(self, string, pos):
        M = [""] * len(string)
        
        for i in xrange(len(string)):
            for j in xrange(len(string)):
                M[j] = string[j] + M[j]
            M.sort()
        
        return M[pos]
            
            
