from random import random, shuffle
import copy

class Evo_solver():
    population = []
    adjacent_positions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    diagonal_position = [(-1,-1),(1,-1),(-1,1),(1,1)]
    def __init__(self, pop_init):
        self.original_nuri=pop_init
        self.sum_of_digits = sum(int(digit)-1 for row in pop_init for digit in row if digit.isdigit())
        self.population.append(self.init_fitness())
        self.solve(10000)

    def solve(self,gen):
        for i in range(gen):
            #self.mutate(self.population[-1][0])
            mutation=self.mutate()
            self.populate(mutation)
            self.selection()
            if(self.calc_fitness(self.population[-1][0]) == 0 and self.check_mistakes(self.population[-1][0])):
                #the goal is to exit through here
                print("Generacija je: "+str(i))
                break
        self.print_nurikabe(self.selection()[0])
        print(self.population[0][1])
        #print(self.sum_of_digits)
    def populate(self,matrix):
        score = self.calc_fitness(matrix)
        prep=[copy.deepcopy(matrix), score]
        self.population.append(prep)

    def selection(self):
        population=self.population
        if len(self.population) < 10:
            return min(population, key=lambda x: x[1])
        else:
            min_element = min(population, key=lambda x: x[1])
            self.population=[min_element]

    def init_fitness(self):
        count_zeros=self.count_zeros(self.original_nuri)
        score = abs(count_zeros - self.sum_of_digits)
        init_pop=[self.original_nuri,score]
        return init_pop

    def calc_fitness(self,matrix):
        count_zeros = self.count_zeros(matrix)
        score = abs(count_zeros - self.sum_of_digits)
        if not self.check_sea_connectivity(matrix):
            score +=2
        square_count=0
        """for i in range(len(matrix) - 1):
            for j in range(len(matrix[0]) - 1):
                square = [matrix[i][j], matrix[i][j + 1], matrix[i + 1][j], matrix[i + 1][j + 1]]
                if square.count('.') == 4:
                    square_count+=1
        score += square_count"""
        return score

    def mutate(self, matrix=None):
        if matrix is None:
            matrix = self.original_nuri
        mutated_matrix = copy.deepcopy(matrix)
        for i in range(len(mutated_matrix)):
            for j in range(len(mutated_matrix[i])):
                if mutated_matrix[i][j].isdigit() and mutated_matrix[i][j] != '0':
                    self.fill_nearby_islands(mutated_matrix,i,j)
        return mutated_matrix

    def fill_nearby_islands(self, matrix, i, j):
        digit = int(matrix[i][j])-1
        #generate islands starting from this core island
        self.generate_islands(matrix, i, j, digit)

    def generate_islands(self, matrix, i, j, digit):
        if digit < 1:
            return
        shuffle(self.adjacent_positions)
        for x, y in self.adjacent_positions:
            if digit > 0:
                ni, nj = i + x, j + y
                if 0 <= ni < len(matrix) and 0 <= nj < len(matrix[0]):
                    if matrix[ni][nj] == '.':
                        if self.check_no_violation(matrix, ni, nj):
                            matrix[ni][nj] = '0'
                            digit=digit - 1
                            # Recursively fill neighboring cells
                            self.generate_islands(matrix, ni, nj, digit)

    def check_no_violation(self, matrix, i, j):
        #check neighbours of sea of core island
        #don't change core islands
        if matrix[i][j].isdigit() and matrix[i][j]!='0':
            return False
        #check if surroundings have to core island digits
        digit_count = 0
        for x, y in self.adjacent_positions:
            ni, nj = i + x, j + y
            if 0 <= ni < len(matrix) and 0 <= nj < len(matrix[0]):
                if matrix[ni][nj].isdigit() and matrix[i][j] != '0':
                    digit_count += 1
        if digit_count > 1:
            return False
        # Check if placing an island here would block any adjacent sea cells
        for x, y in self.adjacent_positions:
            ni, nj = i + x, j + y
            if 0 <= ni < len(matrix) and 0 <= nj < len(matrix[0]):
                if matrix[ni][nj] == '.':
                    # Check sea neighbour of sea near core island
                    if not self.check_sea_blocked(matrix, ni, nj):
                        return False

        return True

    def check_sea_blocked(self, matrix, i, j):
        # Check if the sea cell at position (i, j) is blocked by island cells
        tick=0
        digit_count = 0
        for x, y in self.adjacent_positions:
            ni, nj = i + x, j + y
            if 0 <= ni < len(matrix) and 0 <= nj < len(matrix[0]):
                if matrix[ni][nj] == '0' or matrix[ni][nj].isdigit():
                    digit_count+=1
            else:
                tick+=1
        if digit_count+tick < 3:
            return True
        return False  # The sea cell is not blocked


    def check_mistakes(self,matrix=[]):
        if matrix!=[]:
            for i in range(len(matrix) - 1):
                for j in range(len(matrix[0]) - 1):
                    square = [matrix[i][j], matrix[i][j + 1], matrix[i + 1][j], matrix[i + 1][j + 1]]
                    if square.count('.') == 4:
                        return False

                    if matrix[i][j].isdigit() and matrix[i][j]!='0':
                        zero_count = 0
                        # every number must have an island
                        for x, y in self.adjacent_positions:
                            ni, nj = i + x, j + y
                            if 0 <= ni < len(matrix) and 0 <= nj < len(matrix[0]):
                                if matrix[ni][nj] == '0':
                                    zero_count+=1
                        if zero_count == 0 and matrix[i][j]!='1':
                            return False
                    #core islands cannot share islands
                    elif matrix[i][j]=='0':
                        digit_count=0
                        for x, y in self.adjacent_positions:
                            ni, nj = i + x, j + y
                            if 0 <= ni < len(matrix) and 0 <= nj < len(matrix[0]):
                                if matrix[ni][nj].isdigit() and matrix[i][j]!='0':
                                    digit_count+=1

                        if digit_count>1:
                            return False
            if not self.check_sea_connectivity(matrix):
                return False
            return True

    def check_sea_connectivity(self, matrix):
        sea_cells = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == '.':
                    sea_cells.append((i, j))

        # Check connectivity of sea cells
        visited = set()
        for i, j in sea_cells:
            if (i, j) not in visited:
                if not self.is_sea_connected(matrix, visited, i, j, sea_cells):
                    return False
        return True

    def is_sea_connected(self, matrix, visited, i, j, sea_cells):
        stack = [(i, j)]
        while stack:
            x, y = stack.pop()
            if (x, y) not in visited:
                visited.add((x, y))
                for dx, dy in self.adjacent_positions:
                    ni, nj = x + dx, y + dy
                    if 0 <= ni < len(matrix) and 0 <= nj < len(matrix[0]) and matrix[ni][nj] == '.' and (
                    ni, nj) not in visited:
                        stack.append((ni, nj))
        return len(visited) == len(sea_cells)

    def count_zeros(self,matrix):
        return sum(row.count('0') for row in matrix)
    def print_nurikabe(self,matrix):
        for r in matrix:
            print(r)