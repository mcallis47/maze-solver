from window import Window
from points import Line, Point
from cells import Cell, Maze

def main():
    win = Window(800,600)

    maze = Maze(200,200,25,25,10,10,win)
    maze.solve()
    win.wait_for_close()




main()