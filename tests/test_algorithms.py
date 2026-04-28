from main import (
    arithmetic_coding_compress,
    arithmetic_decoding,
    huffman_compress,
    huffman_decompress,
    lz77_compress,
    lz77_decompress,
    lzw_compress,
    lzw_decompress,
    shannon_fano_compress,
    shannon_fano_decompress,
)
from encodeed.algorithms.rle import run_length_decompress, run_length_encode


def test_run_length_round_trip():
    text = "AAAABBBCCDAA"

    encoded = run_length_encode(text)
    decoded = run_length_decompress(encoded)

    assert decoded == text


def test_huffman_round_trip():
    text = "HELLO HUFFMAN"

    encoded, codebook, _ = huffman_compress(text)
    decoded = huffman_decompress(encoded, codebook)

    assert decoded == text


def test_shannon_fano_round_trip():
    text = "SHANNON FANO"

    encoded, codebook = shannon_fano_compress(text)
    decoded = shannon_fano_decompress(encoded, codebook)

    assert decoded == text


def test_lzw_round_trip():
    text = "TOBEORNOTTOBEORTOBEORNOT"

    encoded = lzw_compress(text)
    decoded = lzw_decompress(encoded)

    assert decoded == text


def test_lz77_round_trip():
    text = "abracadabra abracadabra"

    encoded = lz77_compress(text, window_size=20)
    decoded = lz77_decompress(encoded)

    assert decoded == text


def test_arithmetic_round_trip():
    text = "ABCCC"

    encoded, probabilities = arithmetic_coding_compress(text)
    decoded = arithmetic_decoding(encoded, len(text), probabilities)

    assert decoded == text
