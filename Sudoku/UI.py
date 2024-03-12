import pygame
import math

pygame.init()

WIDTH = 700
HEIGHT = 700

BLACK = (0,0,0)
BLUE = (200,200,255)
LIGHT_BLUE = (220, 220, 255)

# Set up the drawing window
screen = pygame.display.set_mode([WIDTH, HEIGHT])

class Board:
    def __init__(self):
        self.grid = []
        for i in range(9):
            self.grid.append([])
            for j in range(9):
                self.grid[i].append("")
    
    def draw(self):
        
        font = pygame.font.Font(None, 64)

        for i in range(9):

            if i % 3:
                w = 1
            else:
                w = 5
            if i:
                pygame.draw.line(screen, BLACK, (i * WIDTH/9, 0), (i * WIDTH/9, HEIGHT), w)
                pygame.draw.line(screen, BLACK, (0, i * HEIGHT/9), (WIDTH, i * HEIGHT/9), w)

            for j in range(9):
                text = font.render(str(self.grid[i][j]), True, BLACK)
                textRect = text.get_rect()
                textRect.center = ((i+0.5) * WIDTH/9, (j+0.5) * HEIGHT/9)
                screen.blit(text, textRect)

    def highlight(self, pos):
        pygame.draw.rect(screen, LIGHT_BLUE, pygame.Rect(pos[0]*WIDTH/9, pos[1]*HEIGHT/9, WIDTH/9, HEIGHT/9))

# Run until the user asks to quit
running = True
selected = [0, 0]
board = Board()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                selected[0] = max(0, selected[0]-1)
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                selected[0] = min(8, selected[0]+1)
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                selected[1] = max(0, selected[1]-1)
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                selected[1] = min(8, selected[1]+1)
            
            char = str(event.unicode)
            if char in "123456789":
                board.grid[selected[0]][selected[1]] = char
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            selected = [math.floor(x/(WIDTH/9)), math.floor(y/(HEIGHT/9))]



    
    screen.fill(BLUE)
    board.highlight(selected)
    board.draw()
    pygame.display.flip()

pygame.quit()