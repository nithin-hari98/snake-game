import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SPEED = 10

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.positions = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = (1, 0)  # Start moving right
        self.grow = False

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        current = self.get_head_position()
        x, y = self.direction
        new = ((current[0] + x) % GRID_COUNT, (current[1] + y) % GRID_COUNT)
        
        # Check for collision with self
        if new in self.positions[1:]:
            return False

        self.positions.insert(0, new)
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
        return True

    def reset(self):
        self.positions = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = (1, 0)
        self.grow = False

    def render(self, surface):
        for position in self.positions:
            rect = (position[0] * GRID_SIZE, position[1] * GRID_SIZE,
                   GRID_SIZE - 1, GRID_SIZE - 1)
            pygame.draw.rect(surface, GREEN, rect)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_COUNT - 1),
                        random.randint(0, GRID_COUNT - 1))

    def render(self, surface):
        rect = (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE,
               GRID_SIZE - 1, GRID_SIZE - 1)
        pygame.draw.rect(surface, RED, rect)

def main():
    snake = Snake()
    food = Food()
    score = 0
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)

        # Update snake position
        if not snake.update():
            # Game over
            snake.reset()
            food.randomize_position()
            score = 0

        # Check for food collision
        if snake.get_head_position() == food.position:
            snake.grow = True
            food.randomize_position()
            score += 1

        # Draw everything
        screen.fill(BLACK)
        snake.render(screen)
        food.render(screen)
        
        # Draw score
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(SPEED)

if __name__ == '__main__':
    main()