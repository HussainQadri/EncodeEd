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
