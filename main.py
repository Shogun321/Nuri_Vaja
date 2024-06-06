from Nurikabe import Nurikabe
from evo_solver import Evo_solver

def read_nurikabe_from_file(file_path):
    puzzle = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            symbols = line.split()
            row = []
            for symbol in symbols:
                row.append(symbol)
            puzzle.append(row)
    return puzzle


if __name__ == '__main__':
    file_path = 'complex2.txt'
    puzzle_grid = read_nurikabe_from_file(file_path)
    nurikabe = Nurikabe(puzzle_grid)
    nurikabe.print_nurikabe()
    print("  ")
    evo = Evo_solver(nurikabe.Nuri_grid)



