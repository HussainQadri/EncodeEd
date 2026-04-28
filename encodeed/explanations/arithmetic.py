import collections


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
