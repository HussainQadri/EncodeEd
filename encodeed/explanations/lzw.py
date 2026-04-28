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
