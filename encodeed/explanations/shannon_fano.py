import collections


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
