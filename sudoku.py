#To use random samples
import random
#To use type annotations
from typing import Tuple, List, Set, Optional

#The function returns a Sudoku grid from a file
def read_sudoku(filename: str) -> List[List[str]]:
    """ Прочитать Судоку из указанного файла """
    #read characters in List
    digits = [c for c in open(filename).read() if c in '123456789.']
    #Group the characters into a two dimensional array
    grid = group(digits, 9)
    return grid

#The function improves the grid output
def display(grid: List[List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(grid[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()

#The function returns a table - list of lists
def group(values: List[str], n: int) -> List[List[str]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    i = 0
    itog_l = []
    #We pass the table (grid) line by line on n elements in a row
    for c in range(n, n*n+1, n):
        l=[]
        #Collect the elements of the string in the list (get a list of list)
        for i in range(i,c):
            l.append(values[i])
        itog_l.append(l)
        i=i+1
    return itog_l

#The function gets all the values in the string by the passed position
def get_row(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row, _ = pos
    return grid[row]

#The function gets all the values in the column by the passed position
def get_col(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    _, col = pos
    col_grid = []
    #Line by line we pass the column and collect all the values in the column
    for row in range(len(grid)):
            col_grid.append(grid[row][col])
    return col_grid

#The function gets all values squared 3x3 by the transmitted position
def get_block(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    box_grid = []
    row, col = pos
    #On the transmitted position we find the starting cell of the square 3x3
    start_row = 3 * (row // 3)
    start_col = 3 * (col // 3)
    #Collect all the values in a 3x3 square
    for i in range(3):
        for j in range(3):
            box_grid.append(grid[start_row+i][start_col+j])
    return box_grid

#The function finds the first empty cell in the table
def find_empty_positions(grid: List[List[str]]) -> Optional[Tuple[int, int]]:
    """ Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for row in range(len(grid)):
        for col in range(len(grid)):
            if grid[row][col] == '.':
                return (row, col)
    return None

#The function returns a set of possible values for the passed position
def find_possible_values(grid: List[List[str]], pos: Tuple[int, int]) -> Set[str]:
    """ Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    #Find the set of values from set('123456789'), which are not present in the sets of row, column and 3x3 square at the transmitted position
    possible_set = set('123456789').difference(set(get_row(grid, pos)),set(get_col(grid, pos)),set(get_block(grid, pos)))
    return possible_set
 
#The function finds the Sudoku solution by the transferred partially filled grid
def solve(grid: List[List[str]]) -> Optional[List[List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    #Find the first free position
    free_pos = find_empty_positions(grid)
    if not free_pos:
        print("Not free pos...")
        return grid
    row, col = free_pos
    #We loop through all possible values for the passed position, recursively call the solve function
    for val in find_possible_values(grid, free_pos):
        grid[row][col] = val
        solution = solve(grid)
        if solution:
            #If the Sudoku is solved, return the solution in the form of a grid filled with all the values
            return solution
    grid[row][col] = '.'
    #There may not be a solution
    return None

#The function of checking a Sudoku solution
def check_solution(solution: List[List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    #Check line by line that the values are not repeated
    for row in range(len(solution)):
        row_values = set(get_row(solution, (row, 0)))
        if len(row_values.intersection(set('123456789')))!=9: return False
    
    #On columns we check that values do not repeat
    for col in range(len(solution)):
        col_values = set(get_col(solution, (0, col)))
        if len(col_values.intersection(set('123456789')))!=9: return False

    #Check all 3x3 squares in the 9x9 grid so that the values in the 3x3 squares are not repeated
    for row in (0, 3, 6):
        for col in (0, 3, 6):
            box_values = set(get_block(solution, (row, col)))
            #If the set of values of the 3x3 square is not equal to set('123456789'), then somewhere some value in the square is repeated and this is an error
            if len(box_values.intersection(set('123456789')))!=9: return False
    return True

#The function generates a Sudoku grid
def generate_sudoku(N: int) -> List[List[str]]:
    """ Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    #An attempt to form a Sudoku grid randomly, but with the control of possible values in the filled 
    # cells, did not yield successful Sudoku solutions (
    """    
    counter = 1
    ii=0
    for row in range(0,9):
        for col in range(0,9):
            grid[row][col] = "."
    #for _ in range(0,N):
    while ii<N:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if grid[row][col]!=".":
            continue
        if grid[row][col]==".":
            values = find_possible_values(grid,[row,col])
            ii=ii+1
            #grid[row][col] = str(random.randint(1, 9))
            grid[row][col] = str(values.pop())
    return grid
   """
    #First filled the grid with dots and solved Sudoku completely without initial values
    grid = [["." for i in range(9)]for j in range(9)]
    grid = solve(grid)
    P = 81 - N
    #Left in the table the specified N cells filled with values, the remaining cells were filled with points
    while P:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if grid[row][col] != '.': 
            grid[row][col] = '.'  
            P = P - 1
    return grid 
    
for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
    #Obtained from the files of partially-filled Sudoku grids
    grid = read_sudoku(fname)
    #Display the grid
    display(grid)
    #Get the Sudoku solution
    solution = solve(grid)
    if not solution:
        print("Error: not solution")
    else:
        display(solution)
        #Check the Sudoku solution
        check_sol = check_solution(solution)
        print("Solution:" + str(check_sol))

#Generate a Sudoku grid on N filled cells (example on 40 filled cells), solve and check the solution    
grid = generate_sudoku(40)
display(grid)
solution = solve(grid)
if not solution:
    print("Error: not solution")
else:
    display(solution)
    check_sol = check_solution(solution)
    print("!!! Solution:" + str(check_sol))