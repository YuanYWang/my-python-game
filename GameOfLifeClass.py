class GameOfLife():
    currentGrid = []
    nextGrid = []
    def __init__(self, rows=9, cols=9):
        self.rows = rows
        self.cols = cols
        for i in range(self.rows):
            self.currentGrid.append([])
            self.nextGrid.append([])
            for j in range(self.cols):
                self.currentGrid[i].append(0)
                self.nextGrid[i].append(0)
        self.grid = self.currentGrid

    def setupGliderGun(self):
        self.grid[4][1] = 1
        self.grid[4][2] = 1
        self.grid[5][1] = 1
        self.grid[5][2] = 1
        self.grid[4][11] = 1
        self.grid[5][11] = 1
        self.grid[6][11] = 1
        self.grid[3][12] = 1
        self.grid[2][13] = 1
        self.grid[2][14] = 1
        self.grid[3][16] = 1
        self.grid[4][17] = 1
        self.grid[5][17] = 1
        self.grid[6][17] = 1
        self.grid[5][18] = 1
        self.grid[5][15] = 1
        self.grid[7][12] = 1
        self.grid[8][13] = 1
        self.grid[8][14] = 1
        self.grid[7][16] = 1
        self.grid[4][21] = 1
        self.grid[4][22] = 1
        self.grid[3][21] = 1
        self.grid[3][22] = 1
        self.grid[2][21] = 1
        self.grid[2][22] = 1
        self.grid[1][23] = 1
        self.grid[1][25] = 1
        self.grid[0][25] = 1
        self.grid[5][23] = 1
        self.grid[5][25] = 1
        self.grid[6][25] = 1
        self.grid[2][35] = 1
        self.grid[2][36] = 1
        self.grid[3][35] = 1
        self.grid[3][36] = 1

    def flipState(self,x,y):
        if self.grid[x][y] == 0:
            self.grid[x][y] = 1
        else:
            self.grid[x][y] = 0

    def cellNeighbors(self, x, y):
        neighbors = []
        for i in (x - 1, x, x + 1):
            for j in (y - 1, y, y + 1):
                if not (i == x and j == y) and i >= 0 and i < self.rows and j >= 0 and j < self.cols:
                    neighbors.append((i, j))
        return neighbors

    def liveNeighbors(self,x,y):
        live = 0;
        for (r,c) in self.cellNeighbors(x,y):
            live += self.grid[r][c]
        return live

    def step(self):
        for i in range(self.rows):
            for j in range(self.cols):
                liveNeighbors = self.liveNeighbors(i,j)
                if self.grid[i][j] == 0:
                    if liveNeighbors==3:
                        self.nextGrid[i][j] = 1
                    else:
                        self.nextGrid[i][j] = 0
                else:
                    if liveNeighbors==2 or liveNeighbors==3:
                        self.nextGrid[i][j] = 1
                    else:
                        self.nextGrid[i][j] = 0
        self.grid = self.nextGrid
        self.nextGrid = self.currentGrid
        self.currentGrid = self.grid

    def gridIndexToCoord(self, row, col, width, height, margin):
        return (col*(width+margin)+margin, row*(height+margin)+margin)

    def coordToGridIndex(self, x, y, width, height, margin):
        return((int) ((y-margin)/(margin + height )),(int) ((x-margin)/(margin + width)) )