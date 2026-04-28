import collections


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
