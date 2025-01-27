# Snake Game

A resizable Snake game with walls, built in Python using Pygame.

## Setup

1. Install Python 3.x
2. Install Pygame:
```bash
pip install pygame
```
3. Run the game:
```bash
python snake_game.py
```

## Controls

- Arrow keys: Move snake
- R: Reset game
- Window edges: Drag to resize play area

## Features

- Resizable window (minimum 400x400)
- Random internal walls
- Score tracking
- Game ends if snake hits walls or itself
- Food spawns randomly in valid locations

## Customization

Edit these constants in the code:
```python
GRID_SIZE = 20           # Cell size
INITIAL_WINDOW_SIZE = (600, 600)  # Starting size
SPEED = 10              # Game speed
```
