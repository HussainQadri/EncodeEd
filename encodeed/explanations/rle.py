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
