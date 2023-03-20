# KillerSudoku
Python tkinter desktop program for popular variant of traditional sudoku game

To add more puzzles to the pool of puzzles, create a "sudoku.csv" file in the root directory with the following format:
"puzzles,solutions" (make sure this line is included)
[puzzle values],[valid sudoku solution in single string format, left to right, top to bottom]

The code will skip the "puzzle" part of the line, as only the solution is used to generate a new puzzle at runtime.
