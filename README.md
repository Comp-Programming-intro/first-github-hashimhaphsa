# 🐍 Snake

A classic Snake game built with Python, tkinter, and pygame.

## Requirements

- Python 3.x
- pygame

```bash
pip install pygame
```

## Running the Game

```bash
python snake.py
```

## Project Structure

```
├── snake.py
└── assets/
    ├── pickup.mp3
    ├── gold_pickup.mp3
    ├── game_over.mp3
    └── game_start.mp3
```

## How to Play

| Key | Action |
|-----|--------|
| Arrow Keys,WASD | Move the snake |
| R | Restart after game over |
| P | Pause/Resume game |

## Features

- 25×25 grid with a green snake on a black canvas
- 3 food tiles spawn simultaneously — eat them to grow and score
- **Golden food** spawns randomly with a 9 second timer — eat it for +3 points
- Speed increases every 10 points
- Sound effects for pickup, golden pickup, game over, and game start

## Libraries

- **tkinter** — game window, canvas rendering, and input handling
- **pygame** — sound effects via `pygame.mixer`
- **random** — food spawn positions