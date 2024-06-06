class Nurikabe():
    adjacent_positions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    def __init__(self,Nuri_grid):
        self.Nuri_grid=Nuri_grid
        self.block_array=self.traverse_2d_array_in_blocks()

    def print_nurikabe(self):
        for r in self.Nuri_grid:
            print(r)
    def print_blocks(self):
        for i in self.block_array:
            for j in i:
                for k in j:
                    print(k,end="\n")
                print("")
    """def traverse_2d_array_in_blocks(self,array, block_size=3):
        rows, cols = len(array), len(array[0])
        for i in range(0, rows, block_size):
            for j in range(0, cols, block_size):
                block = [array[x][j:j + block_size] for x in range(i, i + block_size)]
                # Process the 3x3 block here
                print("Processing 3x3 block:")
                for row in block:
                    print(row)
    """

    def traverse_2d_array_in_blocks(self, array=None, block_size=3):
        if array is None:
            array=self.Nuri_grid

        rows, cols = len(array), len(array[0])
        block_array=[]
        for i in range(0, rows, block_size):
            temp = []
            for j in range(0, cols, block_size):
                block = [array[x][j:min(j + block_size, cols)] for x in range(i, min(i + block_size, rows))]
                temp.append(block)

            block_array.append(temp)

        return block_array


    def solve(self):
        #redovi
        n=len(self.block_array)
        #kolone
        m=len(self.block_array[0])
        for k in range(n):
            for l in range(m):
                rows, cols = len(self.block_array[k][l]), len(self.block_array[k][l][0])
                for i in range(rows):
                    for j in range(cols):
                        if self.block_array[k][l][i][j].isdigit():
                            # Check adjacent cells
                            digit = self.block_array[k][l][i][j]  # Get the digit as a string
                            valid = False  # Assume the placement is not valid
                            # Check adjacent cells
                            for x, y in self.adjacent_positions:
                                ni, nj = i + x, j + y
                                if 0 <= ni < i and 0 <= nj < j:
                                    valid = True
                                    break
                            # If the placement is valid, add it to the list
                            if valid:
                                self.block_array[k][l][i][j]="0"



    def check_neighbour_cell(self,block):
        rows, cols = len(block), len(block[0])
        count=0
        for i in range(rows):
            for j in range(cols):
                if block[i][j].isdigit():
                    for x, y in self.adjacent_positions:
                        ni, nj = i + x, j + y
                        if 0 <= ni < 3 and 0 <= nj < 3 and block[ni][nj].isdigit():
                            count+=1
        if count<2:
            return 1
