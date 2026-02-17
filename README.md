# 👑 Queens Game Solver

> A Python-based automated solver for the LinkedIn **Queens** logic game using a pure Brute Force algorithm.

## 📖 Description

This project is a desktop application designed to solve the "Queens" puzzle (available on LinkedIn). The goal of the game is to place one queen in each row, column, and colored region without any two queens touching (orthogonally or diagonally).

The solver implements a **Brute Force algorithm** to explore possible configurations and find a valid solution.

### Key Features & Technologies:
* **GUI with PyQt5:** A user-friendly graphical interface built with PyQt5.
* **MultiThreading:** Implements `QThread` to run the heavy algorithmic processing on a separate thread. This prevents the GUI from freezing and enables a smooth **Live Visualization** of the backtracking process.
* **Flexible Input:** Accepts puzzle configurations via:
    * **Text Files (.txt):** Character-based grid representation.
    * **Images (.png, .jpg):** Automatic color extraction from game screenshots using `Pillow`.

## ⚙️ Setup & Installation

To ensure the program runs correctly, it is recommended to use a virtual environment.

### 1. Clone the Repository
```bash
git clone [https://github.com/samuelsondhrm/Tucil1_13524001.git](https://github.com/samuelsondhrm/Tucil1_13524001.git)
cd Tucil1_13524001
```

### 2. Create a Virtual Environment (venv)
It is recommended to use a virtual environment to manage dependencies.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```
**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install the required packages (PyQt5, Pillow, etc.) listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## 🚀 How to Run
1. Ensure your virtual environment is activated.
2. Navigate to the project root directory and run the main GUI file:

```bash
python src/gui.py
```

### Usage Guide
1.  **Upload Puzzle:** Click the `📂 Upload File (.txt / Image)` button.
    * **Text Mode:** Select `.txt` files (e.g., `test/tc1.txt`) to load a character-based grid.
    * **Image Mode:** Select image files (e.g., `test/tc2.png`). A popup dialog will appear asking you to specify the board size ($N$) via a slider.
2.  **Solve:** Once the board is loaded, click the `🚀 SOLVE` button.
3.  **Visualization:** Watch the algorithm place and remove queens in real-time (Live Update).
4.  **Result:** A popup will confirm if a solution is found, displaying the execution time and total iterations.

## 📂 Project Structure
```
.
├── src/
│   ├── gui.py        # Main entry point, handles UI and QThread integration
│   ├── solver.py     # Core Brute Force logic (Backtracking)
│   └── loader.py     # File handling (TXT parsing & Image processing)
├── test/             # Sample test cases (TXT and Image files)
├── doc/              # Final report
├── requirements.txt  # Python dependencies
└── README.md
```

## 👤 Author

**Tugas Kecil 1 IF2211 Strategi Algoritma**
* **Name:** Samuelson Dharmawan Tanuraharja
* **Student ID:** 13524001
