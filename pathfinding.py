import pygame
import sys
import heapq

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 50, 50
CELL_SIZE = WIDTH // COLS

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Algorithms Visualization")

# Grid representation
grid = [[WHITE for _ in range(COLS)] for _ in range(ROWS)]

start = None
end = None

#Dijkstra algorithm logic
def dijkstra(start, end):
    count = 0
    pq = [(0, count, start)]
    distances = {start: 0}
    came_from = {}
    visited = set()

    while pq:
        current_distance, _, current_node = heapq.heappop(pq)
        visited.add(current_node)

        if current_node == end:
            reconstruct_path(came_from, end)
            return True

        for neighbor in get_neighbors(current_node):
            if neighbor in visited or grid[neighbor[0]][neighbor[1]] == BLACK:
                continue
            new_distance = current_distance + 1

            if new_distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_distance
                count += 1
                heapq.heappush(pq, (new_distance, count, neighbor))
                came_from[neighbor] = current_node
                if neighbor != end:
                    grid[neighbor[0]][neighbor[1]] = GREEN

        draw_grid()
        pygame.display.update()

    return False

#AStar algorithm logic
def a_star(start, end):
    count = 0
    pq = [(0, count, start)]
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    came_from = {}
    visited = set()

    while pq:
        current_f_score, _, current_node = heapq.heappop(pq)
        visited.add(current_node)

        if current_node == end:
            reconstruct_path(came_from, end)
            return True

        for neighbor in get_neighbors(current_node):
            if neighbor in visited or grid[neighbor[0]][neighbor[1]] == BLACK:
                continue
            tentative_g_score = g_score[current_node] + 1

            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                count += 1
                heapq.heappush(pq, (f_score[neighbor], count, neighbor))
                if neighbor != end:
                    grid[neighbor[0]][neighbor[1]] = GREEN

        draw_grid()
        pygame.display.update()

    return False

def heuristic(node, end):
    x1, y1 = node
    x2, y2 = end
    return abs(x1 - x2) + abs(y1 - y2)

def get_neighbors(node):
    neighbors = []
    row, col = node
    if row > 0: neighbors.append((row - 1, col))
    if row < ROWS - 1: neighbors.append((row + 1, col))
    if col > 0: neighbors.append((row, col - 1))
    if col < COLS - 1: neighbors.append((row, col + 1))
    return neighbors

def reconstruct_path(came_from, current):
    while current in came_from:
        current = came_from[current]
        if current != start:
            grid[current[0]][current[1]] = PURPLE
        draw_grid()
        pygame.display.update()

def draw_grid():
    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, grid[row][col], (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GREY, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def reset_grid():
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] != BLACK and (row, col) != start and (row, col) != end:
                grid[row][col] = WHITE

# Main loop 
running = True
algorithm = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            pos = pygame.mouse.get_pos()
            row, col = pos[1] // CELL_SIZE, pos[0] // CELL_SIZE
            if not start:
                start = (row, col)
                grid[row][col] = ORANGE
            elif not end and (row, col) != start:
                end = (row, col)
                grid[row][col] = BLUE
            elif (row, col) != start and (row, col) != end:
                grid[row][col] = BLACK
        if pygame.mouse.get_pressed()[2]:  # Right mouse button
            pos = pygame.mouse.get_pos()
            row, col = pos[1] // CELL_SIZE, pos[0] // CELL_SIZE
            grid[row][col] = WHITE
            if (row, col) == start:
                start = None
            elif (row, col) == end:
                end = None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                algorithm = "dijkstra"
            if event.key == pygame.K_a:
                algorithm = "a_star"
            if event.key == pygame.K_r:
                start = None
                end = None
                grid = [[WHITE for _ in range(COLS)] for _ in range(ROWS)]
                algorithm = None

    if algorithm == "dijkstra" and start and end:
        reset_grid()
        dijkstra(start, end)
        algorithm = None
    elif algorithm == "a_star" and start and end:
        reset_grid()
        a_star(start, end)
        algorithm = None

    draw_grid()
    pygame.display.flip()

pygame.quit()
sys.exit()