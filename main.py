from window import Window
from points import Line, Point
from cell import Cell

def main():
    win = Window(800,600)
    line = Line(Point(0,0),Point(800,600))
    line_2 = Line(Point(50,150),Point(300,11))
    win.draw_line(line, "black")
    win.draw_line(line_2, "red")
    cell_1 = Cell(10,20,10,20,win)
    cell_1.draw()
    cell_2 = Cell(20,30,20,30,win)
    cell_2.has_bottom_wall = False
    cell_2.draw()
    cell_3 = Cell(250,500,200,300,win)
    cell_3.has_left_wall = False
    cell_3.has_right_wall = False
    cell_3.draw()
    cell_1.draw_move(cell_2)
    cell_3.draw_move(cell_2, True)

    win.wait_for_close()




main()