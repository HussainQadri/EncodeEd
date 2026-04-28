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
