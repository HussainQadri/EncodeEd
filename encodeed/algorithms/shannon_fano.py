import collections


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
