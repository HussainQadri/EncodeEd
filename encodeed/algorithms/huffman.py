import collections

import networkx as nx
import matplotlib.pyplot as plt


def add_edges(graph, node, parent_label=None):
    if node is None:
        return

    label = f"{node.symbol}\n{node.freq}"

    if parent_label:
        graph.add_edge(parent_label, label)

    add_edges(graph, node.left, label)
    add_edges(graph, node.right, label)


def visualize_huffman_tree(root):
    G = nx.DiGraph()
    add_edges(G, root)

    pos = nx.spring_layout(G, seed=42)  

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, arrows=False, node_size=2000, node_color="lightblue")
    plt.title("Huffman Tree Visualization")
    plt.show()


class Node:  # for Huffman
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huff = ""

    def __lt__(self, next):
        return self.freq < next.freq
    
    def leftNodeExists(self):
        return self.left != None
    def rightNodeExists(self):
        return self.right != None


class minHeap:
    def __init__(self):
        self.data = []
        self.heapsize = 0

    # Adding the helper functions, getting the right and left child and the root and checking if nodes exit
    def rootExists(self, position):
        return self.rootExists(position) >= 0

    def leftChildExists(self, position):
        return self.getLeftChild(position) < self.heapsize

    def rightChildExists(self, position):
        return self.getRightChild(position) < self.heapsize

    def getRoot(self, position):
        return (position - 1) // 2

    def getRightChild(self, position):
        return 2 * position + 2

    def getLeftChild(self, position):
        return 2 * position + 1

    # we only need to be able to insert and get the smallest nodes for Huffman, no need for deletion.

    def insertNode(self, value):
        self.data.append(value)
        currentNode = len(self.data) - 1
        self.heapsize += 1
        self.heapifyUp(self.heapsize - 1)

    def heapifyUp(self, position):
        if position == 0:
            return
        if self.data[position].freq < self.data[self.getRoot(position)].freq:
            root = self.getRoot(position)
            temp = self.data[position]
            self.data[position] = self.data[root]
            self.data[root] = temp

            self.heapifyUp(root)

    # We need to get the smallest value, remove it and rebuild the heap.
    def getSmallest(self):
        if self.heapsize == 0:
            return "Empty"
        smallestElement = self.data[0]
        self.data[0] = self.data[self.heapsize - 1]
        self.data.pop()
        self.heapsize -= 1
        self.heapifyDown(0)  # start at the root

        return smallestElement

    def heapifyDown(self, position):
        smallestChildPosition = position
        rightChild = self.getRightChild(position)
        leftChild = self.getLeftChild(position)

        if (self.leftChildExists(position) and self.data[leftChild].freq < self.data[smallestChildPosition].freq):
            smallestChildPosition = leftChild
        if (self.rightChildExists(position) and self.data[rightChild].freq < self.data[smallestChildPosition].freq):
            smallestChildPosition = rightChild

        if (smallestChildPosition != position):  # this means we must have changed the smallestChildPosition to somwhere else and we must swap nodes
            temp = self.data[position]
            self.data[position] = self.data[smallestChildPosition]
            self.data[smallestChildPosition] = temp

            self.heapifyDown(smallestChildPosition)


def build_codes(node, val="", codebook=None):
    if codebook is None:
        codebook = {}
    code_construction = val + str(node.huff)
    if node.left:
        build_codes(node.left, code_construction, codebook)
    if node.right:
        build_codes(node.right, code_construction, codebook)
    if not node.left and not node.right:
        codebook[node.symbol] = code_construction
    return codebook


def huffman_compress(string):
    frequency = collections.Counter(string)
    heap = minHeap()
    for char, freq in frequency.items():
        heap.insertNode(Node(freq, char))

    while heap.heapsize > 1:
        left = heap.getSmallest()
        right = heap.getSmallest()
        left.huff = 0
        right.huff = 1
        newNode = Node(left.freq + right.freq, left.symbol + right.symbol, left, right)
        heap.insertNode(newNode)

    root = heap.getSmallest()
    codebook = build_codes(root)
    encoded_text = "".join([codebook[char] for char in string])
    return encoded_text, codebook, root



def huffman_decompress(compressed, codebook):
    decode_codebook = {}
    decompressed = []

    for key in codebook:
        value = codebook[key]
        decode_codebook[value] = key
    potential_code = ""
    for bit in compressed:
            potential_code += bit
            if potential_code in decode_codebook:
                decompressed.append(decode_codebook[potential_code])
                potential_code = ""

    return ''.join(decompressed)
