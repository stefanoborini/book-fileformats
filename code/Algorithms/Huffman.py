class Node:
    def __init__(self):
        self.parent = None
        self.byte = None
        self.left = None
        self.right = None
        self.probability = None

def compareNodes(node1, node2):
    res = cmp(node1.probability, node2.probability)
    if res != 0:
        return res
    return cmp(node1.byte, node2.byte) 

def dumpTree(node, indent=""):
    if node is None:
        return

    if node.byte == None:
        to_print = ""
        print indent+"["+str(node.probability)+"]"
    else:
        print indent+node.byte+" ("+str(node.probability)+")"

    dumpTree(node.left, indent+"     ")
    dumpTree(node.right, indent+"     ")

class Huffman:
    def __init__(self):
        pass
    def encode(self, data):
        tree = self.__buildHuffmanTree(data)
    
    def __buildHuffmanTree(self, data):

        # this will hold the nodes
        # The key of the dictionary is the byte found, the value is the node
        node_dictionary = dict()

        # decompose the data in unique bytes, and for each byte create a node
        for i in xrange(len(data)):
            byte = data[i]
            if node_dictionary.has_key(byte):
                node_dictionary[byte].probability = node_dictionary[byte].probability + 1
            else:
                node = Node()
                node.byte = byte
                node.probability = 1
                node_dictionary[byte] = node
           
        # transform the dictionary  
       
        leaves = node_dictionary.values()
        node_list = node_dictionary.values()
        
        while len(node_list) != 1:
            node_list.sort(compareNodes)
            node = Node()
            node.left = node_list.pop(0)
            node.left.parent = node
            node.right = node_list.pop(0)
            node.right.parent = node
            node.byte = None
            node.probability = node.left.probability + node.right.probability
            node_list.append(node)
            
        # now we have the Huffman tree. 

        root_node = node_list[0]

        dumpTree(root_node)

        for leaf in leaves:
            bits = ""
            current = leaf
            while current.parent is not None:
                if current.parent.left is current:
                    bits = "0" + bits
                elif current.parent.right is current:
                    bits = "1" + bits
                else:
                    raise Exception("Something is wrong here")
                current = current.parent
            print leaf.byte + ": "+ bits
            


         
