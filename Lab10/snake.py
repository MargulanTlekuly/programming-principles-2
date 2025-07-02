# snake.py - ИСПРАВЛЕННАЯ И БЕЗОПАСНАЯ ВЕРСИЯ
import pygame
import time
import random
import sys
import psycopg2
from config import load_config # Импортируем нашу функцию для чтения конфига

# --- НАСТРОЙКИ ИГРЫ ---
window_x = 720
window_y = 480

# Цвета
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

# Настройки уровней (стены и скорость)
levels = {
    1: {"speed": 10, "walls": []}, # 1-й уровень без стен
    2: {
        "speed": 12,
        "walls": [pygame.Rect(100, 100, 520, 10), pygame.Rect(100, 370, 520, 10)]
    },
    3: {
        "speed": 15,
        "walls": [
            pygame.Rect(100, 100, 10, 280), pygame.Rect(610, 100, 10, 280),
            pygame.Rect(100, 235, 520, 10)
        ]
    }
}

# --- БЕЗОПАСНЫЕ ФУНКЦИИ ДЛЯ РАБОТЫ С БАЗОЙ ДАННЫХ ---

def create_tables_if_not_exist():
    """ # Создает таблицы, если их нет. Выполняется один раз при старте. """
    commands = (
        """
        CREATE TABLE IF NOT EXISTS game_users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            level INT NOT NULL DEFAULT 1
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS scores (
            score_id SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            score INT NOT NULL,
            saved_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES game_users (user_id) ON DELETE CASCADE
        )
        """
    )
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Database error on table creation: {error}")
        sys.exit() # Если не можем создать таблицы, выходим

def get_or_create_user(username):
    """ # Безопасно находит или создает пользователя. """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Используем параметры (%s) для безопасности
                cur.execute("SELECT user_id, username, level FROM game_users WHERE username = %s", (username,))
                user_data = cur.fetchone()
                if user_data:
                    print(f"Welcome back, {user_data[1]}! Your current level is {user_data[2]}.")
                    return user_data
                else:
                    print(f"User '{username}' not found. Creating a new profile.")
                    cur.execute("INSERT INTO game_users (username) VALUES (%s) RETURNING user_id, username, level;", (username,))
                    new_user_data = cur.fetchone()
                    print(f"Welcome, {new_user_data[1]}! You are starting at level {new_user_data[2]}.")
                    return new_user_data
    except Exception as error:
        print(f"User operation failed: {error}")
        return None

def save_score(user_id, score):
    """ # Безопасно сохраняет счет (создает новую запись). """
    sql = "INSERT INTO scores (user_id, score) VALUES (%s, %s)"
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (user_id, score))
        print(f"Score {score} saved.")
    except Exception as error:
        print(f"Failed to save score: {error}")

def update_user_level(user_id, new_level):
    """ # Безопасно обновляет уровень пользователя. """
    sql = "UPDATE game_users SET level = %s WHERE user_id = %s"
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (new_level, user_id))
        print(f"Level updated to {new_level}!")
    except Exception as error:
        print(f"Failed to update level: {error}")

# --- НАЧАЛО ИГРЫ ---

# 1. Убедимся, что таблицы существуют
create_tables_if_not_exist()

# 2. Получаем данные пользователя
username = input("Enter your username: ")
user_info = get_or_create_user(username)

if not user_info:
    sys.exit()

user_id = user_info[0]
level = user_info[2]
score = 0

# 3. Инициализация Pygame
pygame.init()
pygame.display.set_caption('Snake Game by Beisenbek')
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()

# 4. Настройка змейки и еды
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
fruit_spawn = True
direction = 'RIGHT'
change_to = direction

# --- ГЛАВНЫЙ ИГРОВОЙ ЦИКЛ ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_score(user_id, score) # Сохраняем счет при выходе
            pygame.quit()
            sys.exit()
        
        # Обработка нажатий
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'
            # ПАУЗА И СОХРАНЕНИЕ - правильная реализация
            if event.key == pygame.K_p:
                print("Game paused. Score saved.")
                save_score(user_id, score)
                time.sleep(2) # Просто небольшая пауза, чтобы пользователь увидел сообщение

    # Логика движения
    direction = change_to
    if direction == 'UP': snake_position[1] -= 10
    if direction == 'DOWN': snake_position[1] += 10
    if direction == 'LEFT': snake_position[0] -= 10
    if direction == 'RIGHT': snake_position[0] += 10

    # Механика роста змейки и еды
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
        # Проверка на переход на следующий уровень
        if score >= 30: # Условие для перехода
            level += 1
            if level <= 3:
                update_user_level(user_id, level)
                score = 0 # Сбрасываем счет для нового уровня
            else:
                level = 3 # Максимальный уровень
    else:
        snake_body.pop()
        
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
    fruit_spawn = True

    # Отрисовка
    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, red, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    # Отрисовка стен для текущего уровня
    for wall in levels[level]["walls"]:
        pygame.draw.rect(game_window, white, wall)

    # Условия проигрыша
    if snake_position[0] < 0 or snake_position[0] > window_x - 10 or \
       snake_position[1] < 0 or snake_position[1] > window_y - 10:
        break # Выходим из цикла, чтобы показать Game Over
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            break # Выходим из цикла
    for wall in levels[level]["walls"]:
        if wall.colliderect(pygame.Rect(snake_position[0], snake_position[1], 10, 10)):
            break # Выходим из цикла

    # Отображение счета
    score_font = pygame.font.SysFont('times new roman', 20)
    score_surface = score_font.render(f'Score : {score}  Level: {level}', True, white)
    game_window.blit(score_surface, (10, 10))

    pygame.display.update()
    fps.tick(levels[level]["speed"]) # Скорость зависит от уровня

# --- КОНЕЦ ИГРЫ ---
save_score(user_id, score) # Сохраняем финальный счет
my_font = pygame.font.SysFont('times new roman', 50)
game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
game_over_rect = game_over_surface.get_rect(center=(window_x/2, window_y/4))
game_window.blit(game_over_surface, game_over_rect)
pygame.display.flip()
time.sleep(2)
pygame.quit()
sys.exit()