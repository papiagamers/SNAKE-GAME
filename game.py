from tkinter import *
import random

# ===== CONSTANTS =====
SPACE_SIZE = 20
BODY_PARTS = 3
BACKGROUND_COLOR = "#111111"
BUTTON_COLOR = "#1E90FF"
BUTTON_HOVER = "#63B8FF"
TEXT_COLOR = "#FFFFFF"

# ===== GLOBAL VARIABLES =====
snake = None
food = None
score = 0
direction = 'down'
SPEED = 100
current_level = "Medium"
snake_color = "#00FF00"
food_color = "#FF0000"
ai_mode = False

# ===== SOUND SIMULATION =====
def click_sound(): window.bell()
def eat_sound(): window.bell()
def gameover_sound(): window.bell()

# ===== SNAKE CLASS =====
class Snake:
    def __init__(self):
        self.coordinates = []
        self.squares = []
        for _ in range(BODY_PARTS):
            self.coordinates.append([0, 0])
        for x, y in self.coordinates:
            square = game_canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=snake_color, tag="snake")
            self.squares.append(square)

    def delete(self):
        for sq in self.squares:
            game_canvas.delete(sq)
        self.coordinates.clear()
        self.squares.clear()

# ===== FOOD CLASS =====
class Food:
    def __init__(self):
        window.update_idletasks()
        canvas_width = max(game_canvas.winfo_width(), SPACE_SIZE * 2)
        canvas_height = max(game_canvas.winfo_height(), SPACE_SIZE * 2)
        while True:
            x = random.randint(0, (canvas_width // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (canvas_height // SPACE_SIZE) - 1) * SPACE_SIZE
            if snake is None or [x, y] not in snake.coordinates:
                break
        self.coordinates = [x, y]
        self.id = game_canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=food_color)

# ===== GAME FUNCTIONS =====
def next_turn():
    global snake, food, score, direction
    if snake is None:
        return

    if ai_mode:
        direction_ai()

    x, y = snake.coordinates[0]
    if direction == "up": y -= SPACE_SIZE
    elif direction == "down": y += SPACE_SIZE
    elif direction == "left": x -= SPACE_SIZE
    elif direction == "right": x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])
    square = game_canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=snake_color)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        update_score()
        game_canvas.delete(food.id)
        food = Food()
        eat_sound()
    else:
        del snake.coordinates[-1]
        game_canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions():
        gameover_sound()
        game_over()
    else:
        window.after(SPEED, next_turn)

def change_direction(new_direction):
    global direction
    if new_direction == 'left' and direction != 'right': direction = new_direction
    elif new_direction == 'right' and direction != 'left': direction = new_direction
    elif new_direction == 'up' and direction != 'down': direction = new_direction
    elif new_direction == 'down' and direction != 'up': direction = new_direction

def check_collisions():
    x, y = snake.coordinates[0]
    width = game_canvas.winfo_width()
    height = game_canvas.winfo_height()
    if x < 0 or x >= width or y < 0 or y >= height: return True
    for part in snake.coordinates[1:]:
        if x == part[0] and y == part[1]: return True
    return False

def game_over():
    snake.delete()
    game_canvas.delete("all")
    game_canvas.create_text(game_canvas.winfo_width()/2, game_canvas.winfo_height()/2, font=('Consolas',50), text="GAME OVER", fill="red")
    window.after(2000, back_to_menu)

# ===== AI MODE =====
def direction_ai():
    global direction
    head_x, head_y = snake.coordinates[0]
    food_x, food_y = food.coordinates

    moves = []
    if head_x < food_x: moves.append('right')
    if head_x > food_x: moves.append('left')
    if head_y < food_y: moves.append('down')
    if head_y > food_y: moves.append('up')

    safe_moves = []
    for move in moves:
        nx, ny = head_x, head_y
        if move == 'up': ny -= SPACE_SIZE
        elif move == 'down': ny += SPACE_SIZE
        elif move == 'left': nx -= SPACE_SIZE
        elif move == 'right': nx += SPACE_SIZE
        if [nx, ny] not in snake.coordinates and 0 <= nx < game_canvas.winfo_width() and 0 <= ny < game_canvas.winfo_height():
            safe_moves.append(move)

    if safe_moves:
        change_direction(safe_moves[0])
    else:
        for move in ['up','down','left','right']:
            nx, ny = head_x, head_y
            if move == 'up': ny -= SPACE_SIZE
            elif move == 'down': ny += SPACE_SIZE
            elif move == 'left': nx -= SPACE_SIZE
            elif move == 'right': nx += SPACE_SIZE
            if [nx, ny] not in snake.coordinates and 0 <= nx < game_canvas.winfo_width() and 0 <= ny < game_canvas.winfo_height():
                change_direction(move)
                break

# ===== MENU FUNCTIONS =====
def start_game():
    global snake, food, score, direction
    click_sound()
    main_menu_frame.pack_forget()
    game_frame.pack(fill=BOTH, expand=YES)
    game_canvas.delete("all")
    if snake: snake.delete()
    score = 0
    direction = 'down'
    snake = Snake()
    food = Food()
    update_score()
    next_turn()

def back_to_menu():
    if snake: snake.delete()
    game_frame.pack_forget()
    main_menu_frame.pack(fill=BOTH, expand=YES)

def hover_enter(e): e.widget['background'] = BUTTON_HOVER
def hover_leave(e): e.widget['background'] = BUTTON_COLOR
def set_level(speed, name):
    global SPEED, current_level
    SPEED = speed
    current_level = name
    click_sound()
    update_score()
def update_score():
    ai_status = "AI ON" if ai_mode else "AI OFF"
    game_score_label.config(text=f"Score: {score} | Level: {current_level} | {ai_status}")
def set_snake_color(selection):
    global snake_color
    snake_color_map = {"Green":"#00FF00","Red":"#FF0000","Yellow":"#FFFF00"}
    snake_color = snake_color_map[selection]
def set_food_color(selection):
    global food_color
    food_color_map = {"Red":"#FF0000","Pink":"#FF69B4","Navy":"#000080"}
    food_color = food_color_map[selection]
def toggle_ai():
    global ai_mode
    ai_mode = not ai_mode
    click_sound()
    ai_button.config(text=f"AI Mode: {'ON' if ai_mode else 'OFF'}")
    update_score()

# ===== WINDOW SETUP =====
window = Tk()
window.title("Papia Snake Game")
window.state('zoomed')
window.configure(bg="#000000")
window.resizable(True, True)

# ===== FRAMES =====
main_menu_frame = Frame(window, bg="#111111")
main_menu_frame.pack(fill=BOTH, expand=YES)
game_frame = Frame(window)

# ===== MENU UI =====
center_frame = Frame(main_menu_frame, bg="#111111")
center_frame.pack(expand=True)

Label(center_frame, text="🐍 Papia Snake Game", font=('Consolas',40), fg=TEXT_COLOR, bg="#111111").pack(pady=30)

button_font = ('Consolas', 18)
button_pad = 8

play_button = Button(center_frame, text="PLAY", font=button_font, bg=BUTTON_COLOR, fg=TEXT_COLOR, width=12, height=1, command=start_game)
play_button.pack(pady=button_pad)
play_button.bind("<Enter>", hover_enter)
play_button.bind("<Leave>", hover_leave)

Label(center_frame, text="Select Level", font=('Consolas',20), fg=TEXT_COLOR, bg="#111111").pack(pady=5)
level_frame = Frame(center_frame, bg="#111111")
level_frame.pack(pady=5)
Button(level_frame, text="Easy", font=('Consolas',14), bg=BUTTON_COLOR, fg=TEXT_COLOR, width=7, command=lambda:set_level(150,"Easy")).pack(side=LEFT,padx=5)
Button(level_frame, text="Medium", font=('Consolas',14), bg=BUTTON_COLOR, fg=TEXT_COLOR, width=7, command=lambda:set_level(100,"Medium")).pack(side=LEFT,padx=5)
Button(level_frame, text="Hard", font=('Consolas',14), bg=BUTTON_COLOR, fg=TEXT_COLOR, width=7, command=lambda:set_level(50,"Hard")).pack(side=LEFT,padx=5)

snake_color_menu = StringVar(value="Green")
food_color_menu = StringVar(value="Red")
OptionMenu(center_frame, snake_color_menu,"Green","Red","Yellow",command=set_snake_color).pack(pady=5)
OptionMenu(center_frame, food_color_menu,"Red","Pink","Navy",command=set_food_color).pack(pady=5)

ai_button = Button(center_frame, text="AI Mode: OFF", font=('Consolas',16), bg=BUTTON_COLOR, fg=TEXT_COLOR, width=15, command=toggle_ai)
ai_button.pack(pady=5)

exit_button = Button(center_frame, text="EXIT", font=('Consolas',18), bg=BUTTON_COLOR, fg=TEXT_COLOR, width=12, command=window.destroy)
exit_button.pack(pady=15)
exit_button.bind("<Enter>", hover_enter)
exit_button.bind("<Leave>", hover_leave)

# ===== GAME UI =====
game_score_label = Label(game_frame, text=f"Score: {score} | Level: {current_level} | AI OFF", font=('Consolas',25), bg="#000000", fg="#FFFFFF")
game_score_label.pack()
game_canvas = Canvas(game_frame, bg=BACKGROUND_COLOR)
game_canvas.pack(fill=BOTH, expand=YES)

back_button = Button(game_frame, text="BACK TO MENU", font=('Consolas',18), bg=BUTTON_COLOR, fg=TEXT_COLOR, width=15, command=back_to_menu)
back_button.pack(pady=10)
back_button.bind("<Enter>", hover_enter)
back_button.bind("<Leave>", hover_leave)

# ===== KEY BINDINGS =====
for key, dir in {'Left':'left','Right':'right','Up':'up','Down':'down',
                 'w':'up','W':'up','s':'down','S':'down','a':'left','A':'left','d':'right','D':'right'}.items():
    window.bind(f'<{key}>', lambda e,d=dir: change_direction(d))

window.mainloop()
