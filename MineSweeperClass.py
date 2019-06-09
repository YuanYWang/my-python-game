import random
class MineSweeperTile:
    covered = True
    marked = False
    isMine = False
    mineNeighbor = 0

    def printObjAsDictKey(self):
        if self.marked:
            return 'Marked'
        elif self.covered:
            return 'Covered'
        elif not self.isMine:
            return str(self.mineNeighbor)
        else:
            return 'Mine'

    def printObj(self):
        if self.covered:
            printStr = 'Covered;'
        else:
            printStr = 'UnCovered;'
        if self.marked:
            printStr += 'Marked;'
        else:
            printStr += 'UnMarked;'
        if self.isMine:
            printStr += 'Mine'
        else:
            printStr += str(self.mineNeighbor)
        return printStr

    def __str__(self):
        return self.printObj()

class MineSweeperGrid:
    rows = 3
    cols = 2
    numMines = 10
    grid = []
    backupGrid = []
    fail = False
    firstClick = True

    def __init__(self, rows=9, cols=9, mines=10):
        self.rows = rows
        self.cols = cols
        self.numMines = mines
        self.mineUnMarked = mines
        for i in range(self.rows):
            self.grid.append([])
            self.backupGrid.append([])
            for j in range(self.cols):
               self.grid[i].append(MineSweeperTile())
               self.backupGrid[i].append(MineSweeperTile())

    def revert(self):
        a = self.grid
        self.grid = self.backupGrid
        self.backupGrid = a

    def makeBackup(self):
        if not self.fail:
            for i in range(self.rows):
                for j in range(self.cols):
                    self.backupGrid[i][j].covered = self.grid[i][j].covered
                    self.backupGrid[i][j].marked = self.grid[i][j].marked
                    self.backupGrid[i][j].isMine = self.grid[i][j].isMine
                    self.backupGrid[i][j].mineNeighbor = self.grid[i][j].mineNeighbor


    def cellNeighbors(self, x, y):
        neighbors = []
        for i in (x - 1, x, x + 1):
            for j in (y - 1, y, y + 1):
                if not (i == x and j == y) and i >= 0 and i < self.rows and j >= 0 and j < self.cols:
                    neighbors.append((i, j))
        return neighbors

    #init the grid with mines after the first click, the first click point can not be a mine
    def initGrid(self, x, y):
        minePlanted = 0
        while minePlanted < self.numMines:
            rX = random.randint(0, self.rows - 1)
            rY = random.randint(0, self.cols - 1)
            if not (rX == x and rY == y) and self.grid[rX][rY].isMine == False:
                self.grid[rX][rY].isMine = True
                minePlanted += 1
        for i in range(self.rows):
            for j in range(self.cols):
                mines = 0
                for (r,c) in self.cellNeighbors(i, j):
                    if self.grid[r][c].isMine:
                        mines += 1
                self.grid[i][j].mineNeighbor = mines

    def openNoMineTile(self, x, y):
        if self.grid[x][y].covered == False:
            return
        self.grid[x][y].covered = False
        if self.grid[x][y].mineNeighbor == 0:
            for (r,c) in self.cellNeighbors(x, y):
                self.openNoMineTile(r, c)

    def openAllMineTiles(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j].isMine:
                    self.grid[i][j].covered = False
                    self.grid[i][j].marked = False

    def openTile(self, x, y):
        if self.grid[x][y].marked:
            return
        if self.grid[x][y].isMine:
            self.fail = True
            self.openAllMineTiles() # game over, lost, reveal all mines
            return
        else:
            self.openNoMineTile(x, y)

    def openFirstTile(self, x, y):
        self.firstClick = False
        self.initGrid(x, y)
        self.openTile(x, y)

    def openMultiTile(self,x,y):
        if self.grid[x][y].covered or self.grid[x][y].marked:
            return
        neighbors = self.cellNeighbors(x,y)
        mark = 0
        for (r,c) in neighbors:
            if self.grid[r][c].marked:
                mark += 1
        if mark == self.grid[x][y].mineNeighbor:
            for (r,c) in neighbors:
                if not self.grid[r][c].marked and self.grid[r][c].covered:
                    self.openTile(r, c)

    def success(self):
        if self.firstClick:
            return False    #hav't even started
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j].marked != self.grid[i][j].isMine:
                    return False
                if self.grid[i][j].covered and not self.grid[i][j].isMine:
                    return False
        print('Success')
        return True

    def gridIndexToCoord(self, row, col, width, height, margin):
        return (col*(width+margin)+margin, row*(height+margin)+margin)

    def coordToGridIndex(self, x, y, width, height, margin):
        return((int) ((y-margin)/(margin + height )),(int) ((x-margin)/(margin + width)) )
