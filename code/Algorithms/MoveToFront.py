class MoveToFront:
    def __init__(self): pass

    def encode(self, string):
        dictionary = [ chr(i) for i in xrange(0,256) ] 
        encoded_data = []
        for pos in xrange(len(string)):
            index = dictionary.index(string[pos])
            c = dictionary.pop(index)
            dictionary.insert(0,c)
            encoded_data.append(index)
        return encoded_data
            
    def decode(self, encoded_data):
        dictionary = [ chr(i) for i in xrange(0,256) ] 
        decoded_data = []
        for pos in xrange(len(encoded_data)):
            index = encoded_data[pos]
            decoded_data.append(dictionary[index])
            c = dictionary.pop(index)
            dictionary.insert(0,c)
        return "".join(decoded_data)
        
            
