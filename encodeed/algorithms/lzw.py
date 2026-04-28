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
