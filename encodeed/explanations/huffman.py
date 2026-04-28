import collections

from encodeed.algorithms.huffman import Node, minHeap


def explain_huffman_output(string, encoded, codebook):
    explanation = "Huffman Coding - Step by Step:\n"
    explanation += f"Original Input: {string}\n\n"

    frequency = collections.Counter(string)
    explanation += "Frequency Table:\n"
    for char, freq in frequency.items():
        explanation += f"'{char}': {freq}\n"

    explanation += "\nBuilding minHeap with Nodes for each character:\n"
    heap = minHeap()
    for char, freq in frequency.items():
        explanation += f"Inserting Node('{char}', frequency={freq})\n"
        heap.insertNode(Node(freq, char))

    explanation += "\nBuilding Huffman Tree by extracting two smallest nodes and merging:\n"
    while heap.heapsize > 1:
        left = heap.getSmallest()
        right = heap.getSmallest()
        explanation += f"Extracted Nodes '{left.symbol}' ({left.freq}) and '{right.symbol}' ({right.freq})\n"
        explanation += f"Creating new Node with combined frequency {left.freq + right.freq}.\n"
        left.huff = 0
        right.huff = 1
        newNode = Node(left.freq + right.freq, left.symbol + right.symbol, left, right)
        heap.insertNode(newNode)

    root = heap.getSmallest()
    explanation += "\nGenerated Huffman Tree.\n"

    # Codebook
    explanation += "\nGenerated Codebook:\n"
    for char, code in codebook.items():
        explanation += f"'{char}': {code}\n"

    # Encoding process
    explanation += "\nEncoding Input:\n"
    explanation += "For each character, replacing with corresponding code:\n"
    for char in string:
        explanation += f"'{char}' → {codebook[char]}\n"

    explanation += f"\nFinal Encoded Output: {encoded}\n"
    explanation += f"Compression Ratio: {round(len(encoded) / (len(string) * 8), 3)}"

    return explanation
