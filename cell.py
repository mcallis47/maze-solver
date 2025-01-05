from points import Line, Point

class Cell:
    def __init__(self, x1, x2, y1, y2, window):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = window
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

    def draw(self):
        if self.has_left_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1),Point(self._x1, self._y2)),"RED")
        if self.has_right_wall:
            self._win.draw_line(Line(Point(self._x2, self._y1),Point(self._x2, self._y2)),"RED")
        if self.has_top_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1),Point(self._x2, self._y1)),"RED")
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(self._x1, self._y2),Point(self._x2, self._y2)),"RED")

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