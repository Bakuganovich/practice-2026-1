import pygame
import random
import time

# Инициализация
pygame.init()
pygame.font.init()

# Константы
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Тайп-марафон — Уровни сложности!")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (200, 0, 0)
LIGHT_BLUE = (100, 200, 200)
YELLOW = (255, 200, 0)
GRAY_dark = (34, 39, 46)
# Шрифты
FONT_LARGE = pygame.font.SysFont('arial', 48, bold=True)
FONT_MEDIUM = pygame.font.SysFont('arial', 36)
FONT_SMALL = pygame.font.SysFont('arial', 28)

# === УРОВНИ СЛОЖНОСТИ ===
LEVELS = {
    1: {
        "name": "Новичок",
        "color": GREEN,
        "words": ["кот", "дом", "друг", "мама", "папа", "сон", "день", "ночь", "вода", "еда"],
        "time": 60
    },
    2: {
        "name": "Средний",
        "color": YELLOW,
        "words": ["клавиатура", "программа", "компьютер", "монитор", "процессор", "интернет", "браузер", "сервер",
                  "файл", "папка"],
        "time": 60
    },
    3: {
        "name": "Профи",
        "color": RED,
        "words": ["разработчик", "алгоритм", "архитектура", "микросервис", "контейнер", "деплоймент", "инфраструктура",
                  "автоматизация", "тестирование", "документация"],
        "time": 45
    }
}

# FPS
FPS = 60
CLOCK = pygame.time.Clock()

# Игровые переменные
current_level = 1
level_data = LEVELS[current_level]
current_word = ""
input_text = ""
start_time = None
correct_chars = 0
total_chars = 0
game_state = "menu"  # menu, playing, game_over


# Функции
def draw_text(text, font, color, x, y, center=True):
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    WIN.blit(surface, rect)


def reset_game():
    global current_word, input_text, start_time, correct_chars, total_chars
    current_word = random.choice(level_data["words"])
    input_text = ""
    start_time = time.time()
    correct_chars = 0
    total_chars = 0


def get_accuracy():
    return (correct_chars / total_chars * 100) if total_chars > 0 else 0


def get_wpm():
    elapsed = max(time.time() - start_time, 1)
    words_typed = correct_chars / 5
    return round(words_typed * 60 / elapsed)


def draw_menu():
    WIN.fill(GRAY_dark)
    draw_text("ТАЙП-МАРАФОН", FONT_LARGE, GRAY, WIDTH // 2, 100)
    draw_text("Выбери уровень:", FONT_MEDIUM, GRAY, WIDTH // 2, 200)

    y = 280
    for level, data in LEVELS.items():
        color = data["color"] if current_level == level else GRAY
        draw_text(f"{level}. {data['name']}", FONT_MEDIUM, color, WIDTH // 2, y)
        y += 60

    draw_text("Стрелки ↑↓ — выбор, ENTER — старт", FONT_SMALL, GRAY, WIDTH // 2, 500)


def draw_game():
    WIN.fill(GRAY_dark)

    # Заголовок
    draw_text(f"Уровень: {level_data['name']}", FONT_MEDIUM, level_data["color"], WIDTH // 2, 40)

    # Таймер
    elapsed = int(time.time() - start_time) if start_time else 0
    remaining = max(level_data["time"] - elapsed, 0)
    timer_color = GRAY if remaining > 10 else RED
    draw_text(f"Время: {remaining}с", FONT_MEDIUM, timer_color, WIDTH // 2, 100)

    # Прогресс-бар
    progress = elapsed / level_data["time"]
    pygame.draw.rect(WIN, GRAY, (150, 140, 600, 20))
    pygame.draw.rect(WIN, GREEN, (150, 140, 600 * progress, 20))

    # Текущее слово
    word_y = 235
    draw_text("Напечатай:", FONT_MEDIUM, GRAY, 150, word_y, center=False)

    # Подсветка букв
    word_x = 350
    for i, char in enumerate(current_word):
        color = GREEN if i < len(input_text) and input_text[i] == char else \
            RED if i < len(input_text) else GRAY
        draw_text(char, FONT_LARGE, color, word_x + i * 38, word_y + 10, center=False)

    # Поле ввода
    input_rect = pygame.Rect(150, 340, 600, 60)
    pygame.draw.rect(WIN, WHITE, input_rect, border_radius=15)
    pygame.draw.rect(WIN, GRAY, input_rect, 3, border_radius=15)
    draw_text(input_text + "▎", FONT_LARGE, GRAY_dark, 170, 310 + input_rect.height // 2, center=False)

    # Статистика
    if start_time:
        wpm = get_wpm()
        acc = get_accuracy()
        draw_text(f"WPM: {wpm}", FONT_MEDIUM, GRAY, 200, 430, center=False)
        draw_text(f"Точность: {acc:.1f}%", FONT_MEDIUM, GRAY, 200, 480, center=False)


def draw_game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    WIN.blit(overlay, (0, 0))
    final_wpm = get_wpm()
    final_acc = get_accuracy()
    draw_text("ВРЕМЯ ВЫШЛО!", FONT_LARGE, WHITE, WIDTH // 2, 180)
    draw_text(f"Уровень: {level_data['name']}", FONT_MEDIUM, level_data["color"], WIDTH // 2, 240)
    draw_text(f"Скорость: {final_wpm} WPM", FONT_MEDIUM, GREEN, WIDTH // 2, 300)
    draw_text(f"Точность: {final_acc:.1f}%", FONT_MEDIUM, GREEN, WIDTH // 2, 350)
    draw_text("R — повторить, ESC — меню", FONT_SMALL, GRAY, WIDTH // 2, 440)


# Основной цикл
def main():
    global current_level, level_data, current_word, input_text, start_time
    global correct_chars, total_chars, game_state
    running = True
    while running:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_state == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        current_level = max(1, current_level - 1)
                    elif event.key == pygame.K_DOWN:
                        current_level = min(3, current_level + 1)
                    elif event.key == pygame.K_RETURN:
                        level_data = LEVELS[current_level]
                        reset_game()
                        game_state = "playing"
            elif game_state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = "menu"
                        continue
                    if event.key == pygame.K_RETURN:
                        if input_text == current_word:
                            correct_chars += len(current_word)
                        total_chars += len(input_text)
                        input_text = ""
                        current_word = random.choice(level_data["words"])
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        char = event.unicode.lower()
                        if char.isalpha() or char in " -":
                            input_text += char
                            total_chars += 1
                            if len(input_text) <= len(current_word) and input_text[-1] == current_word[
                                len(input_text) - 1]:
                                correct_chars += 1
            elif game_state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reset_game()
                        game_state = "playing"
                    elif event.key == pygame.K_ESCAPE:
                        game_state = "menu"

        # Проверка времени
        if game_state == "playing" and start_time and time.time() - start_time >= level_data["time"]:
            game_state = "game_over"

        # Отрисовка
        if game_state == "menu":
            draw_menu()
        elif game_state == "playing":
            draw_game()
        elif game_state == "game_over":
            draw_game()
            draw_game_over()

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
