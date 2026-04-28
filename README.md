# EncodeEd

EncodeEd is an educational desktop app for exploring lossless compression
algorithms. It was originally built as an A-level project and focuses on making
the algorithm steps visible rather than acting as a production compression tool.

The app lets a user enter or load text, choose a compression algorithm, inspect
the compressed output, view a step-by-step explanation, and compare rough runtime
behaviour for different input sizes.

## Features

- Text input and `.txt` file loading
- Compression and decompression workflows
- Step-by-step explanations for each supported algorithm
- Huffman tree visualisation
- Shannon-Fano code visualisation
- Runtime sampling with estimated complexity fit

## Supported Algorithms

- Run-Length Encoding
- Huffman Coding
- Shannon-Fano Coding
- LZW Compression
- Arithmetic Coding
- LZ77 Compression

## Project Structure

```text
EncodeEd/
├── app.py      # PyQt5 interface and visualisation dialogs
├── main.py     # Compression algorithms and explanation helpers
├── requirements.txt
├── run.sh      # Linux/macOS launcher
├── run.bat     # Windows launcher
└── README.md
```

## Requirements

EncodeEd is a Python desktop application. It uses:

- Python 3.10+
- PyQt5
- matplotlib
- networkx
- scipy
- numpy

The dependencies are listed in `requirements.txt`.

## Running the App

For the easiest setup, use the launcher script for your operating system. It
creates a local virtual environment, installs the required packages, and starts
the app.

Linux/macOS:

```bash
./run.sh
```

Windows:

```powershell
.\run.bat
```

You can also install the dependencies manually with:

```bash
python -m pip install PyQt5 matplotlib networkx scipy numpy
```

Using a virtual environment is recommended however this is handled with `run.sh` or `run.bat`

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install PyQt5 matplotlib networkx scipy numpy
```

On Windows, activate the virtual environment with:

```powershell
.venv\Scripts\activate
```

Then start the GUI with:

```bash
python app.py
```

Then:

1. Select an algorithm from the list.
2. Enter text manually or load a `.txt` file.
3. Click `Compress` to view the encoded output and explanation.
4. Click `Decompress` to open the decompression dialog for the selected
   algorithm.

## Notes

This repository preserves the project as an educational implementation. Some
choices are intentionally simple and readable, including custom data structures
and direct algorithm implementations, because the goal is to demonstrate the
process behind each compression method.

The project is not intended for compressing large real-world files. Very large
inputs may be slow, especially when tree visualisations or runtime plots are
generated.
