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
GRAY = (128, 128, 128)
SPEED = 10

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

class Wall:
    def __init__(self):
        self.positions = set()
        self.generate_walls()

    def generate_walls(self):
        # Add some random internal walls
        num_internal_walls = 5
        for _ in range(num_internal_walls):
            wall_length = random.randint(3, 6)
            start_x = random.randint(5, GRID_COUNT - 6)
            start_y = random.randint(5, GRID_COUNT - 6)
            
            # Randomly choose horizontal or vertical wall
            if random.choice([True, False]):
                # Horizontal wall
                for x in range(start_x, min(start_x + wall_length, GRID_COUNT - 1)):
                    self.positions.add((x, start_y))
            else:
                # Vertical wall
                for y in range(start_y, min(start_y + wall_length, GRID_COUNT - 1)):
                    self.positions.add((start_x, y))

    def render(self, surface):
        for position in self.positions:
            rect = (position[0] * GRID_SIZE, position[1] * GRID_SIZE,
                   GRID_SIZE - 1, GRID_SIZE - 1)
            pygame.draw.rect(surface, GRAY, rect)

class Snake:
    def __init__(self):
        self.positions = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = (1, 0)  # Start moving right
        self.grow = False

    def get_head_position(self):
        return self.positions[0]

    def update(self, walls):
        current = self.get_head_position()
        x, y = self.direction
        new = (current[0] + x, current[1] + y)
        
        # Check for collision with walls, window edges, or self
        if (new[0] < 0 or new[0] >= GRID_COUNT or 
            new[1] < 0 or new[1] >= GRID_COUNT or 
            new in walls.positions or 
            new in self.positions[1:]):
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
        self.walls = None

    def randomize_position(self, snake, walls):
        self.walls = walls
        available_positions = []
        
        for x in range(1, GRID_COUNT - 1):  # Avoid edges
            for y in range(1, GRID_COUNT - 1):  # Avoid edges
                pos = (x, y)
                if pos not in walls.positions and pos not in snake.positions:
                    available_positions.append(pos)
        
        if available_positions:
            self.position = random.choice(available_positions)

    def render(self, surface):
        rect = (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE,
               GRID_SIZE - 1, GRID_SIZE - 1)
        pygame.draw.rect(surface, RED, rect)

def main():
    snake = Snake()
    walls = Wall()
    food = Food()
    food.randomize_position(snake, walls)
    score = 0
    high_score = 0
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
                elif event.key == pygame.K_r:  # Reset game with new wall layout
                    snake.reset()
                    walls = Wall()
                    food.randomize_position(snake, walls)
                    score = 0

        # Update snake position
        if not snake.update(walls):
            # Game over
            if score > high_score:
                high_score = score
            snake.reset()
            walls = Wall()
            food.randomize_position(snake, walls)
            score = 0

        # Check for food collision
        if snake.get_head_position() == food.position:
            snake.grow = True
            food.randomize_position(snake, walls)
            score += 1

        # Draw everything
        screen.fill(BLACK)
        
        # Draw window border
        pygame.draw.rect(screen, GRAY, (0, 0, WINDOW_SIZE, GRID_SIZE))  # Top
        pygame.draw.rect(screen, GRAY, (0, WINDOW_SIZE - GRID_SIZE, WINDOW_SIZE, GRID_SIZE))  # Bottom
        pygame.draw.rect(screen, GRAY, (0, 0, GRID_SIZE, WINDOW_SIZE))  # Left
        pygame.draw.rect(screen, GRAY, (WINDOW_SIZE - GRID_SIZE, 0, GRID_SIZE, WINDOW_SIZE))  # Right
        
        walls.render(screen)
        snake.render(screen)
        food.render(screen)
        
        # Draw scores
        score_text = font.render(f'Score: {score}', True, WHITE)
        high_score_text = font.render(f'High Score: {high_score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 50))

        pygame.display.update()
        clock.tick(SPEED)

if __name__ == '__main__':
    main()