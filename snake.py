import tkinter
import random
import pygame

import os
os.environ["SDL_AUDIODRIVER"] = "pulseaudio" #allows sfx for WSL

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * ROWS
WINDOW_HEIGHT = TILE_SIZE * COLS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# game window
window = tkinter.Tk()
window.title("snake")
window.resizable(False, False)
canvas = tkinter.Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

# center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# initialise game
snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
food_list = [Tile(random.randint(0, COLS - 1) * TILE_SIZE, random.randint(0, ROWS - 1) * TILE_SIZE) for _ in range(3)]
golden_food = None
snake_body = []
velocityX = 0
velocityY = 0
game_over = False
score = 0
paused = False
speed = 230
high_score = 0
new_hs = False

# pygame mixer
pygame.mixer.pre_init(
    frequency=44100,
    size=-16,
    channels=2,
    buffer=256
)
pygame.mixer.init()

sound_pickup   = pygame.mixer.Sound("assets/pickup.mp3")
sound_game_over = pygame.mixer.Sound("assets/game_over.mp3")
sound_start    = pygame.mixer.Sound("assets/game_start.mp3")
sound_gpickup  = pygame.mixer.Sound("assets/gold_pickup.mp3")
sound_high_score  = pygame.mixer.Sound("assets/high_score.mp3")


def reset_game():
    sound_start.play()
    global snake, golden_food, food_list, snake_body, velocityX, velocityY, game_over, score, speed, paused,new_hs
    snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
    food_list = [Tile(random.randint(0, COLS - 1) * TILE_SIZE, random.randint(0, ROWS - 1) * TILE_SIZE) for _ in range(3)]
    golden_food = None
    snake_body = []
    velocityX = 0
    velocityY = 0
    game_over = False
    score = 0
    paused = False
    speed = 230
    new_hs = False


def spawn_golden_food():
    global golden_food
    pos_x = random.randint(0, COLS - 1) * TILE_SIZE
    pos_y = random.randint(0, ROWS - 1) * TILE_SIZE
    if not any(f.x == pos_x and f.y == pos_y for f in food_list):
        golden_food = Tile(pos_x, pos_y)
        window.after(9000, despawn_golden_food)


def despawn_golden_food():
    global golden_food
    if golden_food is None:
        return
    golden_food = None


def change_direction(e):
    global velocityX, velocityY, game_over, paused
    key = e.char
    print(e, 'is pressed')

    if game_over:
        if e.keysym == "r":
            reset_game()
        return

    if e.keysym == "space":
        paused = not paused

    elif (e.keysym == "Up" or e.keysym == "w") and velocityY != 1:
        velocityX = 0
        velocityY = -1

    elif (e.keysym == "Down" or e.keysym == "s") and velocityY != -1:
        velocityX = 0
        velocityY = 1

    elif (e.keysym == "Left" or e.keysym == "a") and velocityX != 1:
        velocityX = -1
        velocityY = 0

    elif (e.keysym == "Right" or e.keysym == "d") and velocityX != -1:
        velocityX = 1
        velocityY = 0


def move():
    global snake, golden_food, food_list, snake_body, game_over, score,high_score, speed, paused,new_hs
    if game_over or paused:
        return

    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        sound_game_over.play()
        game_over = True
        if(score > high_score):
            new_hs = True
            high_score = score
            sound_high_score.play() 
        return

    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            sound_game_over.play()
            game_over = True
            if(score > high_score):
                new_hs = True
                high_score = score
                sound_high_score.play()
            return

    # normal food collision
    for food in food_list:
        if snake.x == food.x and snake.y == food.y:
            sound_pickup.play()
            snake_body.append(Tile(food.x, food.y))
            # respawn away from golden food
            while True:
                new_x = random.randint(0, COLS - 1) * TILE_SIZE
                new_y = random.randint(0, ROWS - 1) * TILE_SIZE
                if golden_food is None or (new_x != golden_food.x or new_y != golden_food.y):
                    food.x = new_x
                    food.y = new_y
                    break
            score += 1
            if score % 10 == 0:
                speed = max(50, speed - 20)
            if golden_food is None and random.randint(1, 5) == 1:
                spawn_golden_food()

    # golden food collision
    if golden_food and snake.x == golden_food.x and snake.y == golden_food.y:
        sound_gpickup.play()
        score += 3
        golden_food = None

    # update snake body
    for i in range(len(snake_body) - 1, -1, -1):
        tile = snake_body[i]
        if i == 0:
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i - 1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE


def draw():
    global snake, golden_food, food_list, snake_body, game_over, score, speed, paused,new_hs
    move()

    canvas.delete("all")

    # draw food
    for food in food_list:
        canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="#e74c3c", outline="")

    # draw golden food
    if golden_food:
        canvas.create_rectangle(golden_food.x, golden_food.y, golden_food.x + TILE_SIZE, golden_food.y + TILE_SIZE, fill="#f1c40f", outline="")

    # draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="#2ecc71", outline="")
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="#27ae60", outline="")

    # HUD — score always visible unless game over
    if not game_over:
        canvas.create_text(10, 10, anchor="nw", font=("Courier", 13, "bold"), text=f"SCORE  {score}", fill="#ecf0f1")

    # overlay messages
    if game_over and new_hs:
        canvas.create_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, fill="black", stipple="gray50")
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 70,font=("Courier", 22, "bold"), text=f"NEW HIGH SCORE", fill="#28e745")
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 39,font=("Courier", 22, "bold"), text=f"GAME OVER", fill="#e74c3c")
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 9,font=("Courier", 13), text=f"score: {score}\n\n", fill="#ecf0f1")
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 12,font=("Courier", 13), text=f"highest score: {high_score}", fill="#ecf0f1")
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 38,font=("Courier", 11), text="press R to restart", fill="#95a5a6")

    if game_over:
        canvas.create_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, fill="black", stipple="gray50")
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 39,font=("Courier", 22, "bold"), text=f"GAME OVER", fill="#e74c3c")
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 9,font=("Courier", 13), text=f"score: {score}\n\n", fill="#ecf0f1")
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 12,font=("Courier", 13), text=f"highest score: {high_score}", fill="#ecf0f1")
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 38,font=("Courier", 11), text="press R to restart", fill="#95a5a6")

    elif paused:
        canvas.create_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, fill="black", stipple="gray50")
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 12,font=("Courier", 22, "bold"), text="PAUSED", fill="#f1c40f")
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 18,font=("Courier", 11), text="press SPACE to resume", fill="#95a5a6")

    window.after(speed, draw)


draw()
window.bind("<KeyRelease>", change_direction)
window.mainloop()