import pygame
import math
from queue import PriorityQueue
import queue

Width = 800
Win = pygame.display.set_mode((Width, Width))
pygame.display.set_caption("A* Path Finding Algorithm")

# Common colors saved by name
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Yellow = (255, 255, 0)
White = (255, 255, 255)
Black = (0, 0, 0)
Purple = (128, 0, 128)
Orange = (255, 165, 0)
Grey = (128, 128, 128)
Turquoise = (64, 224, 208)


class Spot:
    # constructer tanımlandı
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = White
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    # blockların durumunu anlıyoruz yani set get komutları
    def is_closed(self):
        return self.color == Red

    def is_open(self):
        return self.color == Green

    def is_barrier(self):
        return self.color == Black

    def is_start(self):
        return self.color == Orange

    def is_end(self):
        return self.color == Turquoise

    def reset(self):
        self.color = White

    def make_closed(self):
        self.color = Red

    def make_open(self):
        self.color = Green

    def make_barrier(self):
        self.color = Black

    def make_start(self):
        self.color = Orange

    def make_end(self):
        self.color = Turquoise

    def make_path(self):
        self.color = Purple

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.col < self.total_rows - 1 and self.row < self.total_rows - 1:
            if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # alt kutuya bakıyor
                self.neighbors.append(grid[self.row + 1][self.col])
            if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # üst kutuya bakıyor
                self.neighbors.append(grid[self.row - 1][self.col])

            if self.col < self.total_rows + 1 and not grid[self.row][self.col + 1].is_barrier():  # sağ kutuya bakıyor
                self.neighbors.append(grid[self.row][self.col + 1])

            if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # sol kutuya bakıyor
                self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


# heristik fonksiyonu yani H fonksiyonu
def h(p1, p2):
    # manathan yada taksi metodu ile mesafe tespit edildi
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, Draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        Draw()

def algorithm(Draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end:
            reconstruct_path(came_from, end, Draw)
            end.make_path()
            return True
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        if current != start:
            current.make_closed()
        Draw()
    return False


# kare kare oluşacak ızgara oluşturduk
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, Grey, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, Grey, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(White)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None
    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue
            # get_pressed [0] sol mous tıklanmasını belirtir
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    spot.make_start()

                elif not end and spot != start:
                    end = spot
                    spot.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()
            # get_pressed [2] sağ mous tıklanmasını belirtir
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

    pygame.quit()
main(Win, Width)
