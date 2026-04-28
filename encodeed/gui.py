import sys
import matplotlib.pyplot as plt
from ast import literal_eval

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QBrush, QColor, QFont, QFontMetrics, QPalette, QPen
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QDialog,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from main import (
    arithmetic_coding_compress,
    arithmetic_decoding,
    explain_arithmetic_output,
    explain_huffman_output,
    explain_lz77_output,
    explain_lzw_output,
    explain_rle_output,
    explain_shannon_fano_output,
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


class RuntimeDialog(QDialog):
    def __init__(self, n, t, complexity, algo):
        super().__init__()
        self.setWindowTitle(f"{algo} Runtime - {complexity}")
        self.resize(700, 500)
        layout = QVBoxLayout()

        fig, ax = plt.subplots()
        ax.plot(n, t, marker="o", color="skyblue")
        ax.set_title(f"{algo} Runtime - {complexity}")
        ax.set_xlabel("Input Size (n)")
        ax.set_ylabel("Time (s)")
        ax.grid(True)

        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        self.setLayout(layout)


class RLEDecompressDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RLE Decompression")
        self.resize(400, 300)
        layout = QVBoxLayout()

        self.input_edit = QTextEdit()
        layout.addWidget(self.input_edit)
        self.input_edit.setPlaceholderText("1A2B3C...")

        self.decompress_button = QPushButton("Decompress")
        self.decompress_button.clicked.connect(self.decompress)
        layout.addWidget(self.decompress_button)

        self.output_edit = QTextEdit()
        self.output_edit.setReadOnly(True)
        layout.addWidget(self.output_edit)

        self.setLayout(layout)

    def decompress(self):
        compressed_data = self.input_edit.toPlainText()
        result = run_length_decompress(compressed_data)
        self.output_edit.setText(f"Decompressed Output:\n{result}")


class HuffmanDecompressDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Huffman Decompression")
        self.resize(500, 400)
        layout = QVBoxLayout()

        self.bits_edit = QTextEdit()
        self.bits_edit.setPlaceholderText("Enter Compressed Bits")
        layout.addWidget(self.bits_edit)

        self.codebook_edit = QTextEdit()
        self.codebook_edit.setPlaceholderText("Enter Codebook (Python dict format)")
        layout.addWidget(self.codebook_edit)

        self.decompress_button = QPushButton("Decompress")
        self.decompress_button.clicked.connect(self.decompress)
        layout.addWidget(self.decompress_button)

        self.output_edit = QTextEdit()
        self.output_edit.setReadOnly(True)
        layout.addWidget(self.output_edit)

        self.setLayout(layout)

    def decompress(self):
        try:
            bits = self.bits_edit.toPlainText().strip()
            codebook = literal_eval(self.codebook_edit.toPlainText().strip())
            result = huffman_decompress(bits, codebook)
            self.output_edit.setText(f"Decompressed Output:\n{result}")
        except:
            self.output_edit.setText("Invalid Input")


class ShannonDecompressDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shannon-Fano Decompression")
        self.resize(500, 400)
        layout = QVBoxLayout()

        self.bits_edit = QTextEdit()
        self.bits_edit.setPlaceholderText("Enter Compressed Bits")
        layout.addWidget(self.bits_edit)

        self.codebook_edit = QTextEdit()
        self.codebook_edit.setPlaceholderText("Enter Codebook (Python dict format)")
        layout.addWidget(self.codebook_edit)

        self.decompress_button = QPushButton("Decompress")
        self.decompress_button.clicked.connect(self.decompress)
        layout.addWidget(self.decompress_button)

        self.output_edit = QTextEdit()
        self.output_edit.setReadOnly(True)
        layout.addWidget(self.output_edit)

        self.setLayout(layout)

    def decompress(self):
        try:
            bits = self.bits_edit.toPlainText().strip()
            codebook = literal_eval(self.codebook_edit.toPlainText().strip())
            result = shannon_fano_decompress(bits, codebook)
            self.output_edit.setText(f"Decompressed Output:\n{result}")
        except:
            self.output_edit.setText("Invalid Input")


class LZWDecompressDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LZW Decompression")
        self.resize(500, 300)
        layout = QVBoxLayout()

        self.input_edit = QTextEdit()
        self.input_edit.setPlaceholderText(
            "Enter Compressed List (e.g., [65, 66, 256, 257])"
        )
        layout.addWidget(self.input_edit)

        self.decompress_button = QPushButton("Decompress")
        self.decompress_button.clicked.connect(self.decompress)
        layout.addWidget(self.decompress_button)

        self.output_edit = QTextEdit()
        self.output_edit.setReadOnly(True)
        layout.addWidget(self.output_edit)

        self.setLayout(layout)

    def decompress(self):
        try:
            compressed = literal_eval(self.input_edit.toPlainText().strip())
            result = lzw_decompress(compressed)
            self.output_edit.setText(f"Decompressed Output:\n{result}")
        except:
            self.output_edit.setText("Invalid Input")


class ArithmeticDecompressDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arithmetic Decompression")
        self.resize(500, 400)
        layout = QVBoxLayout()

        self.value_edit = QTextEdit()
        self.value_edit.setPlaceholderText("Enter Encoded Value")
        layout.addWidget(self.value_edit)

        self.length_edit = QTextEdit()
        self.length_edit.setPlaceholderText("Enter Original String Length")
        layout.addWidget(self.length_edit)

        self.prob_edit = QTextEdit()
        self.prob_edit.setPlaceholderText(
            "Enter Probability Table (Python dict format)"
        )
        layout.addWidget(self.prob_edit)

        self.decompress_button = QPushButton("Decompress")
        self.decompress_button.clicked.connect(self.decompress)
        layout.addWidget(self.decompress_button)

        self.output_edit = QTextEdit()
        self.output_edit.setReadOnly(True)
        layout.addWidget(self.output_edit)

        self.setLayout(layout)

    def decompress(self):
        try:
            value = float(self.value_edit.toPlainText().strip())
            length = int(self.length_edit.toPlainText().strip())
            probs = literal_eval(self.prob_edit.toPlainText().strip())
            result = arithmetic_decoding(value, length, probs)
            self.output_edit.setText(f"Decompressed Output:\n{result}")
        except:
            self.output_edit.setText("Invalid Input")


class LZ77DecompressDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LZ77 Decompression")
        self.resize(500, 300)
        layout = QVBoxLayout()

        self.input_edit = QTextEdit()
        self.input_edit.setPlaceholderText(
            "Enter Compressed List (e.g., [(0, 0, 'a'), (1, 1, 'b')])"
        )
        layout.addWidget(self.input_edit)

        self.decompress_button = QPushButton("Decompress")
        self.decompress_button.clicked.connect(self.decompress)
        layout.addWidget(self.decompress_button)

        self.output_edit = QTextEdit()
        self.output_edit.setReadOnly(True)
        layout.addWidget(self.output_edit)

        self.setLayout(layout)

    def decompress(self):
        try:
            compressed = literal_eval(self.input_edit.toPlainText().strip())
            result = lz77_decompress(compressed)
            self.output_edit.setText(f"Decompressed Output:\n{result}")
        except:
            self.output_edit.setText("Invalid Input")


class HuffmanTreeDialog(QDialog):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)
        self.setWindowTitle("Huffman Tree Visualization")
        self.resize(1000, 700)
        self.draw_tree()

    def draw_tree(self):
        def draw_node(node, x, y, x_shift, parent_pos=None, branch_label=""):
            if node is None:
                return

            node_radius = 75
            label = f"{node.symbol}\n{node.freq}" if node.symbol else f"{node.freq}"

            if parent_pos:
                self.scene.addLine(
                    parent_pos.x() + node_radius / 2,
                    parent_pos.y() + node_radius,
                    x + node_radius / 2,
                    y,
                    QPen(Qt.white),
                )
                mid_x = (parent_pos.x() + x + node_radius / 2) / 2
                mid_y = (parent_pos.y() + y + node_radius) / 2
                self.scene.addText(branch_label).setPos(mid_x, mid_y)

            ellipse = self.scene.addEllipse(
                x, y, node_radius, node_radius, QPen(Qt.white), QBrush(Qt.darkGray)
            )

            text_item = self.scene.addText(label)
            text_item.setDefaultTextColor(Qt.white)
            font = text_item.font()
            font.setPointSize(12)
            text_item.setFont(font)
            metrics = QFontMetrics(font)
            text_width = metrics.width(label)
            text_height = metrics.height()
            text_item.setPos(
                x + (node_radius - text_width) / 2,
                (y + (node_radius - text_height) / 2) - 20,
            )

            if node.left:
                draw_node(
                    node.left, x - x_shift, y + 100, x_shift / 2, QPointF(x, y), "0"
                )

            if node.right:
                draw_node(
                    node.right, x + x_shift, y + 100, x_shift / 2, QPointF(x, y), "1"
                )

        draw_node(self.root, 450, 20, 150)


class ShannonFanoDialog(QDialog):
    def __init__(self, codebook):
        super().__init__()
        self.codebook = codebook
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)
        self.setWindowTitle("Shannon-Fano Tree Visualization")
        self.resize(1000, 700)
        self.draw_tree()

    def draw_tree(self):
        def draw_node(entries, x, y, x_shift, parent_pos=None, branch_label=""):
            if not entries:
                return

            label = ", ".join([f"{char}:{code}" for char, code in entries])
            node_radius = 75

            if parent_pos:
                self.scene.addLine(
                    parent_pos.x() + node_radius / 2,
                    parent_pos.y() + node_radius,
                    x + node_radius / 2,
                    y,
                    QPen(Qt.white),
                )
                mid_x = (parent_pos.x() + x + node_radius / 2) / 2
                mid_y = (parent_pos.y() + y + node_radius) / 2
                self.scene.addText(branch_label).setPos(mid_x, mid_y)

            ellipse = self.scene.addEllipse(
                x, y, node_radius, node_radius, QPen(Qt.white), QBrush(Qt.darkGray)
            )
            text_item = self.scene.addText(label)
            text_item.setDefaultTextColor(Qt.white)
            font = text_item.font()
            font.setPointSize(10)
            text_item.setFont(font)
            metrics = QFontMetrics(font)
            text_width = metrics.width(label)
            text_height = metrics.height()
            text_item.setPos(
                x + (node_radius - text_width) / 2,
                (y + (node_radius - text_height) / 2) - 20,
            )

            if len(entries) <= 1:
                return

            mid = len(entries) // 2
            left = entries[:mid]
            right = entries[mid:]

            draw_node(left, x - x_shift, y + 100, x_shift / 2, QPointF(x, y), "0")
            draw_node(right, x + x_shift, y + 100, x_shift / 2, QPointF(x, y), "1")

        entries = list(self.codebook.items())
        draw_node(entries, 450, 20, 150)


class EncodeEdApp(QWidget):
    def __init__(self):
        super().__init__()
        self.current_algorithm = None
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()

        self.algo_selector = QListWidget()
        self.algo_selector.addItems(
            [
                "Run-Length Encoding",
                "Huffman Coding",
                "Shannon Fano",
                "LZW Compression",
                "Arithmetic Coding",
                "LZ77 Compression",
            ]
        )
        self.algo_selector.currentRowChanged.connect(self.algorithm_selected)
        main_layout.addWidget(self.algo_selector)

        input_layout = QVBoxLayout()
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter string to compress here.")
        input_layout.addWidget(self.input_text)

        self.load_button = QPushButton("Load File")
        self.load_button.clicked.connect(self.loadFile)
        input_layout.addWidget(self.load_button)

        self.compress_button = QPushButton("Compress")
        self.compress_button.clicked.connect(self.compress_data)
        input_layout.addWidget(self.compress_button)

        self.decompress_button = QPushButton("Decompress")
        self.decompress_button.clicked.connect(self.decompress_data)
        input_layout.addWidget(self.decompress_button)

        self.output_edit = QTextEdit()
        self.output_edit.setReadOnly(True)
        self.output_edit.setPlaceholderText(
            "Output of the selected compression algorithm will be here."
        )
        input_layout.addWidget(self.output_edit)

        main_layout.addLayout(input_layout)

        self.visual_output = QTextEdit()
        self.visual_output.setReadOnly(True)
        self.visual_output.setPlaceholderText(
            "The explaination of the algorithm will appear here."
        )
        main_layout.addWidget(self.visual_output)
        self.history_label = QLabel("Select an algorithm to view its history.")
        self.history_label.setWordWrap(True)
        main_layout.addWidget(self.history_label)

        self.setLayout(main_layout)
        self.setWindowTitle("EncodeEd - Compression Visualizer")
        self.resize(1300, 650)
        self.show()

    def ask_large_input_visualisation(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Large Input Warning")
        msg.setText(
            "The input is large.\nThe app may lag or crash.\nDo you want to proceed with visualization? You will get the graph plot regardless."
        )
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return msg.exec_() == QMessageBox.Yes

    def algorithm_selected(self, index):
        histories = [
            "Run-Length Encoding: A simple form of lossless data compression where runs of data are stored as a single data value and count.",
            "Huffman Coding: An entropy encoding algorithm used for lossless data compression based on character frequencies.",
            "Shannon-Fano: A precursor to Huffman coding, creates prefix codes based on character probabilities.",
            "LZW Compression: Uses a dictionary-based approach to replace sequences of characters with single codes.",
            "Arithmetic Coding: Represents an entire message as a single number between 0 and 1 using probability ranges.",
            "LZ77 Compression: Uses a sliding window technique to replace repeated occurrences of data with references.",
        ]
        algorithms = ["RLE", "Huffman", "Shannon", "LZW", "Arithmetic", "LZ77"]

        if 0 <= index < len(algorithms):
            self.current_algorithm = algorithms[index]
            self.history_label.setText(histories[index])

        self.visual_output.clear()
        self.output_edit.clear()

    def loadFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Text File",
            "",
            "Text Files (*.txt);;All Files (*)",
            options=options,
        )
        if file_name:
            with open(file_name, "r", encoding="utf-8") as file:
                data = file.read()
            self.input_text.setText(data)

    def compress_data(self):
        import time
        import numpy as np

        text = self.input_text.toPlainText()

        if not text:
            return

        if len(text) > 500 and (
            self.current_algorithm == "Huffman" or self.current_algorithm == "Shannon"
        ):
            proceed = self.ask_large_input_visualisation()
            if not proceed:
                self.visual_output.setText("Visualization skipped due to large input.")
            else:
                self.visual_output.setText("Visualization proceeding...")

        # Proceed with compression and display compressed output
        if self.current_algorithm == "RLE":
            encoded = run_length_encode(text)
            explanation = explain_rle_output(text, encoded)
            self.output_edit.setText(f"Compressed Data:\n{encoded}")
            self.visual_output.setText(explanation)

        elif self.current_algorithm == "Huffman":
            encoded, codebook, root = huffman_compress(text)
            self.output_edit.setText(
                f"Compressed Data:\n{encoded}\n\nCodebook:\n{codebook}"
            )

            if len(text) <= 500 or self.ask_large_input_visualisation():
                dialog = HuffmanTreeDialog(root)
                dialog.exec_()

            explanation = explain_huffman_output(text, encoded, codebook)
            self.visual_output.setText(explanation)

        elif self.current_algorithm == "Shannon":
            encoded, codebook = shannon_fano_compress(text)
            self.output_edit.setText(
                f"Compressed Data:\n{encoded}\n\nCodebook:\n{codebook}"
            )

            if len(text) <= 500 or self.ask_large_input_visualisation():
                dialog = ShannonFanoDialog(codebook)
                dialog.exec_()

            explanation = explain_shannon_fano_output(text, encoded, codebook)
            self.visual_output.setText(explanation)

        elif self.current_algorithm == "LZW":
            compressed = lzw_compress(text)
            explanation = explain_lzw_output(text, compressed)
            self.output_edit.setText(f"Compressed Data:\n{compressed}")
            self.visual_output.setText(explanation)

        elif self.current_algorithm == "Arithmetic":
            encoded, probs = arithmetic_coding_compress(text)
            explanation = explain_arithmetic_output(text, encoded, probs)
            self.output_edit.setText(
                f"Encoded Value:\n{encoded}\n\nProbability Table:\n{probs}"
            )
            self.visual_output.setText(explanation)

        elif self.current_algorithm == "LZ77":
            compressed = lz77_compress(text, window_size=20)
            explanation = explain_lz77_output(text, compressed, window_size=20)
            self.output_edit.setText(f"Compressed Data:\n{compressed}")
            self.visual_output.setText(explanation)

        input_sizes = []
        times = []
        multipliers = [
            0.05,
            0.1,
            0.15,
            0.2,
            0.25,
            0.3,
            0.35,
            0.4,
            0.45,
            0.5,
            0.55,
            0.6,
            0.65,
            0.7,
            0.75,
            0.8,
            0.85,
            0.9,
            0.95,
            1.0,
        ]
        total_times = 0

        number_of_times = 10
        for multiplier in multipliers:
            sample_size = max(1, int(len(text) * multiplier))
            sample = text[:sample_size]
            total_times = 0
            for i in range(number_of_times):
                start_time = time.perf_counter()
                if self.current_algorithm == "RLE":
                    run_length_encode(sample)
                elif self.current_algorithm == "Huffman":
                    huffman_compress(sample)
                elif self.current_algorithm == "Shannon":
                    shannon_fano_compress(sample)
                elif self.current_algorithm == "LZW":
                    lzw_compress(sample)
                elif self.current_algorithm == "Arithmetic":
                    arithmetic_coding_compress(sample)
                elif self.current_algorithm == "LZ77":
                    lz77_compress(sample, window_size=20)
                end_time = time.perf_counter()

                total_times += end_time - start_time

            input_sizes.append(sample_size)
            average_time = total_times / number_of_times
            times.append(average_time)

        input_sizes = np.array(input_sizes)
        times = np.array(times)

        linear_fit = np.polyfit(input_sizes, times, 1)
        nlogn_fit = np.polyfit(input_sizes * np.log(input_sizes), times, 1)
        quadratic_fit = np.polyfit(input_sizes**2, times, 1)

        linear_predicted_values = np.polyval(linear_fit, input_sizes)
        nlogn_predicted_values = np.polyval(
            nlogn_fit, input_sizes * np.log(input_sizes)
        )
        quadratic_predicted_values = np.polyval(quadratic_fit, input_sizes**2)

        # just an application of the formula for the r^2 statistic
        def r2(y, y_predicted_value):
            return 1 - np.sum((y - y_predicted_value) ** 2) / np.sum(
                (y - np.mean(y)) ** 2
            )

        r2_linear = r2(times, linear_predicted_values)
        r2_nlogn = r2(times, nlogn_predicted_values)
        r2_quadratic = r2(times, quadratic_predicted_values)

        best = max(r2_linear, r2_nlogn, r2_quadratic)
        if best == r2_linear:
            complexity = "O(n)"
        elif best == r2_nlogn:
            complexity = "O(n log n)"
        else:
            complexity = "O(n²)"

        dialog = RuntimeDialog(input_sizes, times, complexity, self.current_algorithm)
        dialog.exec_()

    def decompress_data(self):
        if self.current_algorithm == "RLE":
            dialog = RLEDecompressDialog()
            dialog.exec_()

        elif self.current_algorithm == "Huffman":
            dialog = HuffmanDecompressDialog()
            dialog.exec_()

        elif self.current_algorithm == "Shannon":
            dialog = ShannonDecompressDialog()
            dialog.exec_()

        elif self.current_algorithm == "LZW":
            dialog = LZWDecompressDialog()
            dialog.exec_()

        elif self.current_algorithm == "Arithmetic":
            dialog = ArithmeticDecompressDialog()
            dialog.exec_()

        elif self.current_algorithm == "LZ77":
            dialog = LZ77DecompressDialog()
            dialog.exec_()


def main():
    app = QApplication(sys.argv)

    # Spotify-like dark theme
    app.setStyle("Fusion")
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.Text, QColor(220, 220, 220))
    dark_palette.setColor(QPalette.Button, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))
    dark_palette.setColor(QPalette.Highlight, QColor(80, 80, 80))
    dark_palette.setColor(QPalette.HighlightedText, QColor(220, 220, 220))

    app.setPalette(dark_palette)
    app.setFont(QFont("Segoe UI", 10))

    window = EncodeEdApp()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
