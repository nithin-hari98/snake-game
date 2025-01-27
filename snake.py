import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 20  # Size of each grid cell
INITIAL_WINDOW_SIZE = (600, 600)  # Initial window size
MIN_WINDOW_SIZE = (400, 400)  # Minimum window size
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
SPEED = 10

# Set up the display with resizable flag
screen = pygame.display.set_mode(INITIAL_WINDOW_SIZE, pygame.RESIZABLE)
pygame.display.set_caption('Snake Game - Resizable')
clock = pygame.time.Clock()

class GameState:
    def __init__(self):
        self.window_size = INITIAL_WINDOW_SIZE
        self.grid_count_x = self.window_size[0] // GRID_SIZE
        self.grid_count_y = self.window_size[1] // GRID_SIZE
        
    def update_size(self, new_size):
        self.window_size = (max(new_size[0], MIN_WINDOW_SIZE[0]), 
                           max(new_size[1], MIN_WINDOW_SIZE[1]))
        self.grid_count_x = self.window_size[0] // GRID_SIZE
        self.grid_count_y = self.window_size[1] // GRID_SIZE
        return pygame.display.set_mode(self.window_size, pygame.RESIZABLE)

class Wall:
    def __init__(self, game_state):
        self.positions = set()
        self.generate_walls(game_state)

    def generate_walls(self, game_state):
        self.positions.clear()
        # Add some random internal walls
        num_internal_walls = (game_state.grid_count_x + game_state.grid_count_y) // 8
        
        for _ in range(num_internal_walls):
            wall_length = random.randint(3, 6)
            start_x = random.randint(5, game_state.grid_count_x - 6)
            start_y = random.randint(5, game_state.grid_count_y - 6)
            
            if random.choice([True, False]):
                # Horizontal wall
                for x in range(start_x, min(start_x + wall_length, game_state.grid_count_x - 1)):
                    self.positions.add((x, start_y))
            else:
                # Vertical wall
                for y in range(start_y, min(start_y + wall_length, game_state.grid_count_y - 1)):
                    self.positions.add((start_x, y))

    def render(self, surface, game_state):
        # Draw border walls
        pygame.draw.rect(surface, GRAY, (0, 0, game_state.window_size[0], GRID_SIZE))  # Top
        pygame.draw.rect(surface, GRAY, (0, game_state.window_size[1] - GRID_SIZE, 
                        game_state.window_size[0], GRID_SIZE))  # Bottom
        pygame.draw.rect(surface, GRAY, (0, 0, GRID_SIZE, game_state.window_size[1]))  # Left
        pygame.draw.rect(surface, GRAY, (game_state.window_size[0] - GRID_SIZE, 0, 
                        GRID_SIZE, game_state.window_size[1]))  # Right
        
        # Draw internal walls
        for position in self.positions:
            rect = (position[0] * GRID_SIZE, position[1] * GRID_SIZE,
                   GRID_SIZE - 1, GRID_SIZE - 1)
            pygame.draw.rect(surface, GRAY, rect)

class Snake:
    def __init__(self, game_state):
        self.reset(game_state)

    def reset(self, game_state):
        self.positions = [(game_state.grid_count_x // 2, game_state.grid_count_y // 2)]
        self.direction = (1, 0)
        self.grow = False

    def get_head_position(self):
        return self.positions[0]

    def update(self, walls, game_state):
        current = self.get_head_position()
        x, y = self.direction
        new = (current[0] + x, current[1] + y)
        
        # Check for collisions with walls, window edges, or self
        if (new[0] < 0 or new[0] >= game_state.grid_count_x or 
            new[1] < 0 or new[1] >= game_state.grid_count_y or 
            new in walls.positions or 
            new in self.positions[1:]):
            return False

        self.positions.insert(0, new)
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
        return True

    def render(self, surface):
        for position in self.positions:
            rect = (position[0] * GRID_SIZE, position[1] * GRID_SIZE,
                   GRID_SIZE - 1, GRID_SIZE - 1)
            pygame.draw.rect(surface, GREEN, rect)

class Food:
    def __init__(self):
        self.position = (0, 0)

    def randomize_position(self, snake, walls, game_state):
        available_positions = []
        
        for x in range(1, game_state.grid_count_x - 1):
            for y in range(1, game_state.grid_count_y - 1):
                pos = (x, y)
                if pos not in walls.positions and pos not in snake.positions:
                    available_positions.append(pos)
        
        if available_positions:
            self.position = random.choice(available_positions)

    def render(self, surface):
        rect = (self.position[0] * GRID_SIZE, position[1] * GRID_SIZE,
               GRID_SIZE - 1, GRID_SIZE - 1)
        pygame.draw.rect(surface, RED, rect)

def main():
    game_state = GameState()
    snake = Snake(game_state)
    walls = Wall(game_state)
    food = Food()
    food.randomize_position(snake, walls, game_state)
    score = 0
    high_score = 0
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = game_state.update_size(event.size)
                # Regenerate walls and reposition food for new size
                walls.generate_walls(game_state)
                food.randomize_position(snake, walls, game_state)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)
                elif event.key == pygame.K_r:  # Reset game
                    snake.reset(game_state)
                    walls.generate_walls(game_state)
                    food.randomize_position(snake, walls, game_state)
                    score = 0

        # Update snake position
        if not snake.update(walls, game_state):
            # Game over
            if score > high_score:
                high_score = score
            snake.reset(game_state)
            walls.generate_walls(game_state)
            food.randomize_position(snake, walls, game_state)
            score = 0

        # Check for food collision
        if snake.get_head_position() == food.position:
            snake.grow = True
            food.randomize_position(snake, walls, game_state)
            score += 1

        # Draw everything
        screen.fill(BLACK)
        walls.render(screen, game_state)
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