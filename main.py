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


def MergeSort(array):  # just a notice this sorts the dictionary in shannon-fano in DESCENDING order

    arrayLength = len(array)
    if arrayLength <= 1:
        return
    middle = arrayLength // 2
    leftArray = array[:middle]
    rightArray = array[middle:]
    MergeSort(leftArray)
    MergeSort(rightArray)
    MergeLists(leftArray, rightArray, array)


def MergeLists(leftArray, rightArray, array):
    i = 0
    j = 0
    k = 0
    while i < len(leftArray) and j < len(rightArray):
        if leftArray[i][1] > rightArray[j][1]:
            array[k] = leftArray[i]
            k += 1
            i += 1
        else:
            array[k] = rightArray[j]
            j += 1
            k += 1

    while i < len(leftArray):
        array[k] = leftArray[i]
        i += 1
        k += 1

    while j < len(rightArray):
        array[k] = rightArray[j]
        j += 1
        k += 1


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




def lzw_compress(string):
    dictionary_length = 256  # so we can represent the first 256 ascii characters
    dictionary = {}
    existingCharacters = ""
    newEntries = []
    for i in range(dictionary_length):
        character = chr(i)
        dictionary[character] = i

    for character in string:
        charactersToAdd = existingCharacters + character
        if charactersToAdd in dictionary:
            existingCharacters = charactersToAdd

        else:
            newEntries.append(dictionary.get(existingCharacters))
            dictionary[charactersToAdd] = dictionary_length
            dictionary_length += 1
            existingCharacters = character
    if existingCharacters != "":
        newEntries.append(dictionary.get(existingCharacters))
    return newEntries




def lzw_decompress(encoded):
    dictionary_length = 256
    dictionary = {}
    decoded = []
    for i in range(dictionary_length):
        dictionary[i] = chr(i)
    characters = dictionary[encoded[0]]
    decoded.append(characters)
    encoded = encoded[1:]
    for code in encoded:
        if code in dictionary:
            entry = dictionary[code]
        elif code == dictionary_length:
            entry = characters + characters[0]
        decoded.append(entry)
        dictionary[dictionary_length] = characters + entry[0]
        dictionary_length += 1
        characters = entry
    return "".join(decoded)

def run_length_encode(string):
    encoding = ""
    i = 0

    while i < len(string):
        count = 1
        while i + 1 < len(string) and string[i] == string[i + 1]:
            count += 1
            i += 1
        encoding += str(count) + string[i]
        i += 1

    return encoding
def run_length_decompress(string):
    number = ""
    
    decoded = []
    for i in range(len(string)):
        if string[i].isdigit():
            number += string[i]
        else:
            number = int(number)
            decoded.append(string[i] * number)
            number = ""
    return ''.join(decoded)





def shannon_fano_helper(tuple, codebook={}, start=""):
    # This algo uses recursion because we are basically splitting a list until it only has one character, we use this condition for our base case
    if len(tuple) == 1:
        character = tuple[0][0]
        codebook[character] = start or "0"
        return codebook

    total_frequency = 0
    for keyvalue_pair in tuple:
        freq = keyvalue_pair[1]
        total_frequency += freq

    half_frequency = (
        total_frequency / 2
    )  # this is the target we want to reach and when we want to split our frequency table.

    sum = 0
    split_at_index = 0
    for index, (_, freq) in enumerate(
        tuple
    ):  # enumerate will simply keep a running count of the index, makes it easier to track which frequency on the table we are currently on
        sum += freq
        if (
            sum >= half_frequency
        ):  # we have just exceeded our target, this is where we stop and split
            split_at_index = index
            break
    left_split = tuple[: split_at_index + 1]
    right_split = tuple[split_at_index + 1 :]
    # we now assign 0 for the left split and 1 for the right split, add recursive calls here as we are now forming a 'tree'
    shannon_fano_helper(left_split, codebook, start + "0")
    shannon_fano_helper(right_split, codebook, start + "1")
    return codebook



def get_frequency(pair):
    return pair[1]

def shannon_fano_compress(string):
    frequency = dict(collections.Counter(string))
    tuples = list(frequency.items())
    MergeSort(tuples)
    reverse_order = tuples
    codebook = shannon_fano_helper(reverse_order)  # I have decided to implement the recursion in a helper function for readability.

    encoded = ''.join(codebook[char] for char in string)

    return encoded,codebook


def shannon_fano_decompress(compressed, codebook):
    # we want to reverse the key value pairs as every code in the compressed text corresponds to a character
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




def arithmetic_coding_compress(string):  # the start of this algo is similiar to shannon_fano

    frequency = collections.Counter(string)  # this will give a dictionary where the character and its frequency appear as key-value pairs

    length = len(string)
    probabilities = {}  # this is a dictionary that will store the character and its respective probability
    frequency_sorted = sorted(frequency.items())

    sum = 0
    for (character,frequency,) in (frequency_sorted):  # this for loop creates the cumulative range for our characters
        probablity = frequency / length
        probabilities[character] = (sum, sum + probablity)
        sum += probablity
    print(probabilities)

    lower_range = 0
    upper_range = 1
    for character in string:
        range_length = upper_range - lower_range
        character_lower_range, character_upper_range = probabilities[character]
        upper_range = lower_range + range_length * character_upper_range
        lower_range = lower_range + range_length * character_lower_range
    encoded = (lower_range + upper_range) / 2
    return encoded, probabilities

def arithmetic_decoding(encoded_value, string_length, probabilities):
    lower_range = 0
    upper_range = 1
    decoded = ""


    probability_list = []
    for character in probabilities:
        low, high = probabilities[character]
        probability_list.append((character, low, high))

    for i in range(len(probability_list)): # we need to sort the probabilities, implemented a bubble sort here
        for j in range(i + 1, len(probability_list)):
            if probability_list[i][1] > probability_list[j][1]:
                probability_list[i], probability_list[j] = probability_list[j], probability_list[i]

    for i in range(string_length):  
        range_size = upper_range - lower_range
        normalised_encoded_value = (encoded_value - lower_range) / range_size

        for character, character_lower, character_upper in probability_list:
            if character_lower <= normalised_encoded_value < character_upper:
                decoded += character
                lower_range = lower_range + range_size * character_lower
                upper_range = lower_range + range_size * (character_upper - character_lower)
                break  

    return decoded



def lz77_compress(string, window_size):
   compressed = []
   position = 0
   while position < len(string):
        # at the near beginning of the string
      if position - window_size < 0:
         search_window_position = 0
      else:
         search_window_position = position - window_size
      
      best_match_length = 0
      best_match_offset = 0

   # we are going back to characters we have seen before
      for history_pointer in range(search_window_position, position):
         possible_match_length = 0
         while position + possible_match_length < len(string):
            if string[possible_match_length + history_pointer] == string[position + possible_match_length]:
               possible_match_length += 1
               if history_pointer + possible_match_length >= position: # we can't look forward from our current position
                  break
            else:
               break

         if possible_match_length > best_match_length:
            best_match_length = possible_match_length
            best_match_offset = position - history_pointer

      if best_match_length > 0:
         if position + best_match_length < len(string):
            character = string[position + best_match_length]
         else:
            character = ""
         position += best_match_length + 1
         compressed.append((best_match_offset,best_match_length,character))
      else:
         compressed.append((0,0,string[position]))
         position += 1
   return compressed

def lz77_decompress(compressed):
   decompressed = []
   for offset, match_length, character in compressed:
      if offset == 0 and match_length == 0:
         decompressed.append(character)
      else:
         goBackPosition = len(decompressed) - offset
         charactersAdded = 0
         while charactersAdded != match_length:
            decompressed.append(decompressed[goBackPosition])
            goBackPosition += 1
            charactersAdded += 1
         decompressed.append(character)
      
   return ''.join(decompressed)


# these functions are for UI, to explain the algorithms. They use the EXACT SAME algorithms as above but have a narration style to them for my UI, the only real difference is the use of the explaination variable, these don’t need to be marked algorithmically again. They are the same. 

def explain_rle_output(original, encoded):
    explanation = "RLE Compression - Step by Step:\n"
    count = 1
    for i in range(1, len(original)):
        if original[i] == original[i - 1]:
            count += 1
            explanation += f"Found '{original[i]}', same as previous, increasing count to {count}.\n"
        else:
            explanation += f"Character changed from '{original[i - 1]}' to '{original[i]}'.\n"
            explanation += f"Adding '{count}{original[i - 1]}' to output and resetting count.\n"
            count = 1
    explanation += f"End of input. Adding '{count}{original[-1]}' to output.\n"
    explanation += f"\nFinal Encoded Output: {encoded}\n"
    explanation += f"Compression Ratio: {round(len(encoded) / len(original), 3)}"
    return explanation

def explain_lzw_output(string, compressed):
    explanation = "LZW Compression - Step by Step:\n"
    dictionary_length = 256
    dictionary = {}
    existingCharacters = ""
    explanation += "Initial dictionary contains all ASCII characters (0-255).\n"

    for i in range(dictionary_length):
        character = chr(i)
        dictionary[character] = i

    for character in string:
        charactersToAdd = existingCharacters + character
        if charactersToAdd in dictionary:
            explanation += f"'{charactersToAdd}' exists in dictionary. Extending existingCharacters.\n"
            existingCharacters = charactersToAdd
        else:
            explanation += f"'{charactersToAdd}' not found in dictionary.\n"
            explanation += f"Adding code for '{existingCharacters}': {dictionary.get(existingCharacters)}.\n"
            dictionary[charactersToAdd] = dictionary_length
            explanation += f"Adding '{charactersToAdd}' to dictionary with code {dictionary_length}.\n"
            dictionary_length += 1
            existingCharacters = character

    if existingCharacters != "":
        explanation += f"End of input. Adding code for '{existingCharacters}': {dictionary.get(existingCharacters)}.\n"

    explanation += f"\nFinal Compressed Output: {compressed}\n"
    explanation += f"Compression Ratio: {round(len(compressed) / len(string), 3)}"
    return explanation


def explain_lz77_output(string, compressed, window_size):
    explanation = "LZ77 Compression - Step by Step:\n"
    explanation += f"Window size: {window_size}\n"
    position = 0

    while position < len(string):
        if position - window_size < 0:
            search_window_position = 0
        else:
            search_window_position = position - window_size

        best_match_length = 0
        best_match_offset = 0

        explanation += f"\nPosition {position}: Searching in window [{search_window_position}:{position}]\n"

        for history_pointer in range(search_window_position, position):
            possible_match_length = 0
            while position + possible_match_length < len(string):
                if string[possible_match_length + history_pointer] == string[position + possible_match_length]:
                    possible_match_length += 1
                    if history_pointer + possible_match_length >= position:
                        break
                else:
                    break

            if possible_match_length > best_match_length:
                best_match_length = possible_match_length
                best_match_offset = position - history_pointer

        if best_match_length > 0:
            if position + best_match_length < len(string):
                character = string[position + best_match_length]
            else:
                character = ""
            explanation += f"Found match of length {best_match_length} at offset {best_match_offset}.\n"
            explanation += f"Adding tuple ({best_match_offset}, {best_match_length}, '{character}') to output.\n"
            position += best_match_length + 1
        else:
            explanation += f"No match found. Adding tuple (0, 0, '{string[position]}').\n"
            position += 1

    explanation += f"\nFinal Compressed Output: {compressed}\n"
    explanation += f"Compression Ratio: {round(len(compressed) / len(string), 3)}"
    return explanation

            
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

def explain_shannon_fano_output(string, encoded, codebook):
    explanation = "Shannon-Fano Coding - Step by Step:\n"
    explanation += f"Original Input: {string}\n\n"

    # Frequency table
    frequency = collections.Counter(string)
    tuples = list(frequency.items())
    tuples.sort(key=lambda x: x[1], reverse=True)
    explanation += "Frequency Table (sorted descending):\n"
    for char, freq in tuples:
        explanation += f"'{char}': {freq}\n"

    # Splitting process
    explanation += "\nBuilding Shannon-Fano Tree by splitting at half of total frequency:\n"
    total_frequency = sum(freq for _, freq in tuples)
    explanation += f"Total Frequency: {total_frequency}\n"

    def recursive_explain(tuple, start=""):
        if len(tuple) == 1:
            character = tuple[0][0]
            explanation_lines.append(f"Only one character '{character}' left. Assign code '{start or '0'}'.\n")
            return

        total = sum(freq for _, freq in tuple)
        half = total / 2
        running_sum = 0
        split_index = 0

        for index, (_, freq) in enumerate(tuple):
            running_sum += freq
            if running_sum >= half:
                split_index = index
                break

        left = tuple[: split_index + 1]
        right = tuple[split_index + 1:]

        left_symbols = [char for char, _ in left]
        right_symbols = [char for char, _ in right]

        explanation_lines.append(
            f"Split at index {split_index}. Left: {left_symbols}, Right: {right_symbols}.\n"
        )
        recursive_explain(left, start + "0")
        recursive_explain(right, start + "1")

    explanation_lines = []
    recursive_explain(tuples)
    explanation += "".join(explanation_lines)

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


def explain_arithmetic_output(string, encoded, probabilities):
    explanation = "Arithmetic Coding - Step by Step:\n"
    explanation += f"Original Input: {string}\n\n"

    # Frequency table
    frequency = collections.Counter(string)
    explanation += "Frequency Table:\n"
    for char, freq in frequency.items():
        explanation += f"'{char}': {freq}\n"

    explanation += "\nProbability Table and cumulative ranges:\n"
    cumulative = 0
    for character, freq in sorted(frequency.items()):
        prob = freq / len(string)
        explanation += f"'{character}': Probability = {round(prob, 3)}, Range = ({round(cumulative, 3)}, {round(cumulative + prob, 3)})\n"
        cumulative += prob

    lower_range = 0
    upper_range = 1
    explanation += "\nEncoding Process:\n"
    for character in string:
        range_length = upper_range - lower_range
        character_lower_range, character_upper_range = probabilities[character]
        explanation += f"Character '{character}': Current Range ({round(lower_range, 5)}, {round(upper_range, 5)}).\n"
        explanation += f"Character Range: ({round(character_lower_range, 5)}, {round(character_upper_range, 5)})\n"
        upper_range = lower_range + range_length * character_upper_range
        lower_range = lower_range + range_length * character_lower_range
        explanation += f"Updated Range: ({round(lower_range, 5)}, {round(upper_range, 5)})\n\n"

    explanation += f"Final Encoded Value: {encoded}\n"

    ratio = round(1 / (len(string) * 8), 5)  # Arithmetic always outputs 1 number
    explanation += f"Compression Ratio: {ratio}"

    return explanation
