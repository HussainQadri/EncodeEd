import collections

from encodeed.algorithms.rle import run_length_decompress, run_length_encode
from encodeed.algorithms.lzw import lzw_compress, lzw_decompress
from encodeed.algorithms.lz77 import lz77_compress, lz77_decompress
from encodeed.algorithms.arithmetic import arithmetic_coding_compress, arithmetic_decoding
from encodeed.algorithms.huffman import (
    Node,
    add_edges,
    build_codes,
    huffman_compress,
    huffman_decompress,
    minHeap,
    visualize_huffman_tree,
)
from encodeed.algorithms.shannon_fano import (
    MergeLists,
    MergeSort,
    get_frequency,
    shannon_fano_compress,
    shannon_fano_decompress,
    shannon_fano_helper,
)


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
