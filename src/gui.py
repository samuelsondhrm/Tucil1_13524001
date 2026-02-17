import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                             QMessageBox, QFrame, QDialog, QSlider, QDialogButtonBox)
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt5.QtCore import Qt, pyqtSlot

import loader
from solver import QueensSolver

class SliderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pilih Ukuran Papan")
        self.setFixedWidth(300)
        
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel("Tentukan ukuran grid (N) dari gambar:"))
        
        self.value_label = QLabel("8")
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet("font-size: 24px; font-weight: bold; color: blue;")
        layout.addWidget(self.value_label)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(21)
        self.slider.setValue(8)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.update_label)
        layout.addWidget(self.slider)
        
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)
        
    def update_label(self, value):
        self.value_label.setText(str(value))

    def get_value(self):
        return self.slider.value()
    
class BoardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.grid = []
        self.N = 0
        self.queens = []
        self.colors = {}
        self.setMinimumSize(400, 400)

    def set_data(self, grid, N):
        self.grid = grid
        self.N = N
        self.queens = []
        self.generate_colors()
        self.update()

    def generate_colors(self):
        self.colors = {}
        unique_chars = sorted(list(set(char for row in self.grid for char in row)))
        
        palette = [
            "#FF9999", "#FFCC99", "#FFFF99", "#CCFF99", "#99FF99", "#99FFCC",
            "#99FFFF", "#99CCFF", "#9999FF", "#CC99FF", "#FF99FF", "#FF99CC",
            "#FF6666", "#FFB266", "#FFFF66", "#B2FF66", "#66FF66", "#66FFB2",
            "#66FFFF", "#66B2FF", "#6666FF", "#B266FF", "#FF66FF", "#FF66B2",
            "#E0E0E0", "#A0A0A0"
        ]
        
        for i, char in enumerate(unique_chars):
            color_code = palette[i % len(palette)]
            self.colors[char] = QColor(color_code)

    def update_queen(self, r, c, is_adding):
        if is_adding:
            self.queens.append((r, c))
        else:
            if (r, c) in self.queens:
                self.queens.remove((r, c))
        self.update()

    def paintEvent(self, event):
        if self.N == 0:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        cell_size = min(w, h) // self.N
        
        offset_x = (w - (cell_size * self.N)) // 2
        offset_y = (h - (cell_size * self.N)) // 2

        for r in range(self.N):
            for c in range(self.N):
                char = self.grid[r][c]
                x = offset_x + c * cell_size
                y = offset_y + r * cell_size

                bg_color = self.colors.get(char, Qt.white)
                painter.setBrush(QBrush(bg_color))
                painter.setPen(QPen(Qt.black, 1))
                painter.drawRect(x, y, cell_size, cell_size)
        
        font_size = int(cell_size * 0.6)
        emoji_font = QFont("Segoe UI Emoji", font_size)
        painter.setFont(emoji_font)
        painter.setPen(Qt.black)

        for (r, c) in self.queens:
            x = offset_x + c * cell_size
            y = offset_y + r * cell_size
            
            painter.drawText(x, y, cell_size, cell_size, Qt.AlignCenter, "👑")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Queens Solver - 13524001")
        self.setGeometry(100, 100, 600, 700)
        self.grid = []
        self.N = 0
        self.solver_thread = None
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        header_layout = QHBoxLayout()
        self.btn_upload = QPushButton("📂 Upload File (.txt / Image)")
        self.btn_upload.setStyleSheet("padding: 10px; font-weight: bold;")
        self.btn_upload.clicked.connect(self.upload_file)
        header_layout.addWidget(self.btn_upload)
        layout.addLayout(header_layout)

        self.lbl_file_info = QLabel("Belum ada file yang dimuat.")
        self.lbl_file_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_file_info)

        self.board_view = BoardWidget()
        self.board_frame = QFrame()
        self.board_frame.setFrameShape(QFrame.StyledPanel)
        frame_layout = QVBoxLayout(self.board_frame)
        frame_layout.addWidget(self.board_view)
        layout.addWidget(self.board_frame)

        stats_layout = QHBoxLayout()
        
        self.btn_solve = QPushButton("🚀 SOLVE")
        self.btn_solve.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        self.btn_solve.setEnabled(False)
        self.btn_solve.clicked.connect(self.start_solving)
        
        stats_layout.addWidget(self.btn_solve)
        layout.addLayout(stats_layout)

        self.lbl_status = QLabel("Status: Ready")
        self.lbl_time = QLabel("Waktu: - ms")
        self.lbl_iter = QLabel("Iterasi: -")
        
        font_bold = QFont(); font_bold.setBold(True)
        self.lbl_status.setFont(font_bold)
        
        info_layout = QHBoxLayout()
        info_layout.addWidget(self.lbl_status)
        info_layout.addWidget(self.lbl_time)
        info_layout.addWidget(self.lbl_iter)
        layout.addLayout(info_layout)

    def upload_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Pilih File Puzzle", "", "All Files (*);;Text Files (*.txt);;Images (*.png *.jpg)", options=options)
        
        if not file_path:
            return

        try:
            result, val = loader.read_file(file_path)

            if val == -1: 
                img = result
                
                dialog = SliderDialog(self)
                if dialog.exec_() == QDialog.Accepted:
                    n = dialog.get_value()
                    
                    self.grid = loader.image_to_grid(img, n)
                    self.N = n
                    self.lbl_file_info.setText(f"File: {file_path} (Img N={self.N})")
                else:
                    return
            else:
                self.grid = result
                self.N = val
                self.lbl_file_info.setText(f"File: {file_path} (Text N={self.N})")

            self.board_view.set_data(self.grid, self.N)
            self.btn_solve.setEnabled(True)
            self.reset_stats()

        except Exception as e:
            QMessageBox.critical(self, "Error Loading File", str(e))

    def reset_stats(self):
        self.lbl_status.setText("Status: Ready")
        self.lbl_status.setStyleSheet("color: black")
        self.lbl_time.setText("Waktu: 0 ms")
        self.lbl_iter.setText("Iterasi: 0")

    def start_solving(self):
        if not self.grid or self.N == 0: return
        self.btn_solve.setEnabled(False)
        self.btn_upload.setEnabled(False)
        self.lbl_status.setText("Solving...")
        self.lbl_status.setStyleSheet("color: blue")
        
        self.solver_thread = QueensSolver(self.grid, self.N)
        self.solver_thread.update_sig.connect(self.board_view.update_queen)
        self.solver_thread.finished_sig.connect(self.on_solver_finished)
        self.solver_thread.start()

    @pyqtSlot(bool, int, float)
    def on_solver_finished(self, success, iterations, duration_ms):
        self.btn_solve.setEnabled(True)
        self.btn_upload.setEnabled(True)
        self.lbl_iter.setText(f"Iterasi: {iterations}")
        self.lbl_time.setText(f"Waktu: {duration_ms:.2f} ms")

        if success:
            self.lbl_status.setText("SOLUSI DITEMUKAN!")
            self.lbl_status.setStyleSheet("color: green; font-size: 14px;")
            QMessageBox.information(self, "Success", f"Selesai dalam {duration_ms:.2f} ms!")
        else:
            self.lbl_status.setText("TIDAK ADA SOLUSI")
            self.lbl_status.setStyleSheet("color: red; font-size: 14px;")
            QMessageBox.warning(self, "Failed", "Tidak ada solusi.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())