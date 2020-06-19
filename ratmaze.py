import random
import pygame
pygame.init()
clock = pygame.time.Clock()

blocksize = 20
maze_length = 20
maze_width = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 4

Color_line = (255, 0, 0)

screen = pygame.display.set_mode([500, 500])
screen.fill(WHITE)

class Ratmaze:

    def __init__(self):
        self.running = True
        self.maze = []
        self.maze_solved = False
        self.list = [[1, 0], [0, 1]]
        self.path = [(0, 0)]

    def get_maze(self):
        for x in range(maze_length):
            row = []
            for y in range(maze_width):
                row.append(random.choice([0, 1, 1, 1, 1, 1, 1 ,1 ,1]))
            self.maze.append(row)

    def is_inside_maze(self, elem):
        return 0 <= elem[0] < len(self.maze) and 0 <= elem[1] < len(self.maze[0]) and self.maze[elem[0]][elem[1]] == 1

    def solve(self):

        if self.maze_solved:
            return

        yield self.path

        if len(self.maze) == 0 or len(self.maze[0]) == 0:
            self.maze_solved = True

        if self.path[-1][0] == len(self.maze) - 1 and self.path[-1][1] == len(self.maze[0]) - 1:
            self.maze_solved = True

        if not self.maze_solved:
            for elem in self.list:
                new_elem = (self.path[-1][0] + elem[0], self.path[-1][1] + elem[1])
                if self.is_inside_maze(new_elem):
                    self.path.append(new_elem)
                    yield from self.solve()
                    if not self.maze_solved:
                        self.path.pop()

    def draw_maze(self):

        generator = self.solve()

        while self.running:

            if self.maze[0][0] == 0 or self.maze[maze_length-1][maze_width-1] == 0:
                self.maze_solved = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if not self.maze_solved:

                for i, row in enumerate(self.maze):
                    for j, cell in enumerate(row):
                        rect = pygame.Rect(j * blocksize, i * blocksize,
                                        blocksize, blocksize)
                        pygame.draw.rect(screen, BLACK, rect, cell)

                for i, elem in enumerate(self.path[:-1]):
                    x_axis = True if elem[0] == self.path[i + 1][0] else False
                    y_axis = True if elem[1] == self.path[i + 1][1] else False
                    rect = pygame.Rect(elem[1] * blocksize + blocksize / 4, elem[0] * blocksize + blocksize / 4, blocksize if x_axis else blocksize / 2, blocksize if y_axis else blocksize / 2)
                    pygame.draw.rect(screen, Color_line, rect)

                try:
                    next(generator)
                except StopIteration:
                    pass

                pygame.display.flip()
                clock.tick(FPS)
                screen.fill(WHITE)

        pygame.quit()

ratmaze = Ratmaze()
ratmaze.get_maze()
ratmaze.draw_maze()
