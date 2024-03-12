# Sudoku
This is a sudoku generator / solver written in python.

It generates a sudoku by filling in the square with random numbers (abiding by the rules of the game) until its reached a solution. Then it 'reduces' that solved state, removing a number from the grid while ensuring that the resulting board is still solvable. When it reaches a point where it can no longer remove a number without making the sudoku unsolvable (or have multiple solutions) then it is done!

To use this program, just run sudoku.py on the command line and await your newly generated sudoku!
