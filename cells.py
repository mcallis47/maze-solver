import random
import time
from points import Line, Point

class Cell:
    def __init__(self, x1, x2, y1, y2, window=None):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = window
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False

    def draw(self):
        if self.has_left_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1),Point(self._x1, self._y2)),"RED")
        else:
            self._win.draw_line(Line(Point(self._x1, self._y1),Point(self._x1, self._y2)),"WHITE")
        if self.has_right_wall:
            self._win.draw_line(Line(Point(self._x2, self._y1),Point(self._x2, self._y2)),"RED")
        else:
            self._win.draw_line(Line(Point(self._x2, self._y1),Point(self._x2, self._y2)),"WHITE")
        if self.has_top_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1),Point(self._x2, self._y1)),"RED")
        else:
            self._win.draw_line(Line(Point(self._x1, self._y1),Point(self._x2, self._y1)),"WHITE")
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(self._x1, self._y2),Point(self._x2, self._y2)),"RED")
        else:
            self._win.draw_line(Line(Point(self._x1, self._y2),Point(self._x2, self._y2)),"WHITE")

    def draw_move(self, to_cell, undo=False):
        color = "RED"
        if undo:
            color = "GRAY"
        line = Line(
            Point(
                (self._x1 + self._x2)/2,(self._y1 + self._y2)/2
                ), 
            Point(
                (to_cell._x1 + to_cell._x2)/2,(to_cell._y1 + to_cell._y2)/2
                )
            )
        self._win.draw_line(line, color)

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._create_cells()
        if seed:
            random.seed(seed)
        self._break_walls_r(0,0)
        self._break_entrance_and_exit()
        self._reset_cells_visited()

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        #up
        if j > 0 and not self._cells[i][j-1].visited and not self._cells[i][j].has_top_wall:
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if self._solve_r(i, j-1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j-1], True)
        #down
        if j < self._num_rows - 1 and not self._cells[i][j+1].visited and not self._cells[i][j].has_bottom_wall:
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if self._solve_r(i, j+1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j+1], True)
        #left
        if i > 0 and not self._cells[i-1][j].visited and not self._cells[i][j].has_left_wall:
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i-1][j], True)
        #right
        if i < self._num_cols - 1 and not self._cells[i+1][j].visited and not self._cells[i][j].has_right_wall:
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i+1][j], True)
        return False

    def _create_cells(self):
        self._cells = []
        for i in range(self._num_cols):
            self._cells.append([])
            col = self._cells[i]
            for j in range(self._num_rows):
                col.append(Cell(self._x1 + i * self._cell_size_x, self._x1 + (i+1) * self._cell_size_x, self._y1 + j * self._cell_size_y, self._y1 + (j+1) * self._cell_size_y, self._win))
                self._draw_cell(i, j)
            

    def _draw_cell(self, i, j):
        if self._win:
            self._cells[i][j].draw()
            self._animate()
        
    def _animate(self):
        self._win.redraw()
        time.sleep(0.01)    

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_left_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_right_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        cur_cell = self._cells[i][j]
        cur_cell.visited = True
        while(True):
            to_visit = []
            #up
            if j > 0 and not self._cells[i][j-1].visited:
                to_visit.append((i, j-1))
            #down
            if j < self._num_rows - 1 and not self._cells[i][j+1].visited:
                to_visit.append((i, j+1))
            #left
            if i > 0 and not self._cells[i-1][j].visited:
                to_visit.append((i-1, j))
            #right
            if i < self._num_cols - 1 and not self._cells[i+1][j].visited:
                to_visit.append((i+1, j))
            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return
            dir = to_visit.pop(random.randrange(len(to_visit)))
            next_cell = self._cells[dir[0]][dir[1]]
            #left
            if cur_cell._x1 > next_cell._x1:
                cur_cell.has_left_wall = False
                next_cell.has_right_wall = False
            #right
            if cur_cell._x1 < next_cell._x1:
                cur_cell.has_right_wall = False
                next_cell.has_left_wall = False
            #up
            if cur_cell._y1 > next_cell._y1:
                cur_cell.has_top_wall = False
                next_cell.has_bottom_wall = False
            #down
            if cur_cell._y1 < next_cell._y1:
                cur_cell.has_bottom_wall = False
                next_cell.has_top_wall = False
            self._break_walls_r(dir[0],dir[1])
            

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False





        