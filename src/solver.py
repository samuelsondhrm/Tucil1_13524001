from PyQt5.QtCore import QThread, pyqtSignal

class QueensSolver(QThread):
    update_sig = pyqtSignal(int, int, bool)
    finished_sig = pyqtSignal(bool, int, float)

    def __init__(self, matriks_warna, n):
        super().__init__()
        self.grid = matriks_warna
        self.N = n
        self.solution = []
        self.iterations = 0

        self.occ_cols = set()
        self.occ_colors = set()
        self.queens_positions = []

    def run(self):
        import time
        start = time.time()
        success = self.solve(0)
        end = time.time()
        durations = (end - start) * 1000
        self.finished_sig.emit(success, self.iterations, durations)

    def is_safe(self, row, col):
        current_color = self.grid[row][col]

        if current_color in self.occ_colors:
            return False
        
        if col in self.occ_cols:
            return False 
        
        check_directions = [(-1, -1), (-1, 0), (-1, 1)]
        for dr, dc in check_directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.N and 0 <= nc < self.N:
                if (nr, nc) in self.queens_positions:
                    return False
        
        return True

    def solve(self, row):
        if row == self.N:
            return True
        
        for col in range(self.N):
            self.iterations += 1
            
            if self.is_safe(row, col):
                self.solution.append((row, col))
                self.occ_cols.add(col)
                self.occ_colors.add(self.grid[row][col])
                self.queens_positions.append((row, col))

                self.update_sig.emit(row, col, True)
                self.msleep(50)

                if self.solve(row+1):
                    return True
                
                self.solution.pop()
                self.occ_cols.remove(col)
                self.occ_colors.remove(self.grid[row][col])
                self.queens_positions.remove((row, col))

                self.update_sig.emit(row, col, False)
                self.msleep(20)
        
        return False
