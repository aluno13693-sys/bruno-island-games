import pygame
import random
import math
import sys

pygame.init()

# =========================================================
# CONFIGURAÇÕES
# =========================================================

WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ilha Perdida - Sobrevivência")

clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 18)
SMALL_FONT = pygame.font.SysFont("arial", 14)
BIG_FONT = pygame.font.SysFont("arial", 28)

# Cores
GRASS = (105, 170, 95)
SAND = (224, 202, 135)
WATER = (75, 160, 195)
TREE_GREEN = (45, 125, 60)
TREE_DARK = (35, 90, 45)
WOOD_COLOR = (110, 70, 40)
ROCK = (110, 110, 110)
PLAYER_COLOR = (50, 90, 180)
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
RED = (200, 60, 60)
GREEN = (70, 180, 80)
YELLOW = (220, 190, 60)

# =========================================================
# JOGADOR
# =========================================================

player = {
    "x": WIDTH // 2,
    "y": HEIGHT // 2,
    "speed": 4,
    "health": 100,
    "hunger": 100,
    "thirst": 100
}

# =========================================================
# INVENTÁRIO
# =========================================================

inventory = {
    "wood": 0,
    "stone": 0,
    "food": 2,
    "water": 1
}

# =========================================================
# RECURSOS
# =========================================================

resources = []

for i in range(18):
    resources.append({
        "type": "tree",
        "x": random.randint(70, WIDTH - 70),
        "y": random.randint(100, HEIGHT - 70),
        "amount": random.randint(2, 5)
    })

for i in range(10):
    resources.append({
        "type": "rock",
        "x": random.randint(70, WIDTH - 70),
        "y": random.randint(100, HEIGHT - 70),
        "amount": random.randint(1, 3)
    })

for i in range(8):
    resources.append({
        "type": "food",
        "x": random.randint(70, WIDTH - 70),
        "y": random.randint(100, HEIGHT - 70),
        "amount": random.randint(1, 3)
    })

# =========================================================
# ABRIGO
# =========================================================

shelter = None

# =========================================================
# TEMPO
# =========================================================

day = 1
time_counter = 0
is_night = False

# =========================================================
# MENSAGEM
# =========================================================

message = "Explora a ilha e recolhe recursos!"
message_timer = 180


def show_message(text):
    global message, message_timer

    message = text
    message_timer = 180


# =========================================================
# FUNÇÕES
# =========================================================

def distance(x1, y1, x2, y2):
    return math.sqrt(
        (x1 - x2) ** 2 +
        (y1 - y2) ** 2
    )


def draw_text(text, x, y, font=FONT, color=WHITE):
    image = font.render(text, True, color)
    screen.blit(image, (x, y))


def draw_bar(x, y, width, height, value, color, label):
    pygame.draw.rect(
        screen,
        BLACK,
        (x, y, width, height)
    )

    pygame.draw.rect(
        screen,
        color,
        (x, y, int(width * value / 100), height)
    )

    draw_text(
        f"{label}: {int(value)}",
        x + 5,
        y + 2,
        SMALL_FONT,
        WHITE
    )


def draw_player():
    x = int(player["x"])
    y = int(player["y"])

    # Corpo
    pygame.draw.rect(
        screen,
        PLAYER_COLOR,
        (x - 10, y - 10, 20, 25)
    )

    # Cabeça
    pygame.draw.circle(
        screen,
        (235, 190, 150),
        (x, y - 17),
        9
    )


def draw_tree(x, y):
    # Tronco
    pygame.draw.rect(
        screen,
        WOOD_COLOR,
        (x - 6, y, 12, 25)
    )

    # Copa
    pygame.draw.circle(
        screen,
        TREE_DARK,
        (x, y - 5),
        25
    )

    pygame.draw.circle(
        screen,
        TREE_GREEN,
        (x - 10, y - 15),
        20
    )


def draw_rock(x, y):
    pygame.draw.circle(
        screen,
        ROCK,
        (x, y),
        15
    )


def draw_food(x, y):
    pygame.draw.circle(
        screen,
        (200, 55, 50),
        (x, y),
        8
    )

    pygame.draw.circle(
        screen,
        (80, 150, 70),
        (x + 6, y - 7),
        5
    )


def draw_shelter():
    if shelter is None:
        return

    x = shelter["x"]
    y = shelter["y"]

    # Parede
    pygame.draw.rect(
        screen,
        WOOD_COLOR,
        (x - 45, y - 30, 90, 60)
    )

    # Telhado
    pygame.draw.polygon(
        screen,
        (80, 50, 30),
        [
            (x - 55, y - 30),
            (x, y - 70),
            (x + 55, y - 30)
        ]
    )

    # Porta
    pygame.draw.rect(
        screen,
        BLACK,
        (x - 10, y, 20, 30)
    )


def collect_resource():
    nearest = None
    nearest_distance = 45

    for resource in resources:

        if resource["amount"] <= 0:
            continue

        d = distance(
            player["x"],
            player["y"],
            resource["x"],
            resource["y"]
        )

        if d < nearest_distance:
            nearest = resource
            nearest_distance = d

    if nearest is None:
        show_message("Não estás perto de nenhum recurso.")
        return

    amount = nearest["amount"]

    if nearest["type"] == "tree":

        inventory["wood"] += amount
        show_message(
            f"Recolheste {amount} madeira!"
        )

    elif nearest["type"] == "rock":

        inventory["stone"] += amount
        show_message(
            f"Recolheste {amount} pedra!"
        )

    elif nearest["type"] == "food":

        inventory["food"] += amount
        show_message(
            f"Encontraste {amount} comida!"
        )

    nearest["amount"] = 0


def eat_food():

    if inventory["food"] <= 0:
        show_message("Não tens comida!")
        return

    inventory["food"] -= 1

    player["hunger"] = min(
        100,
        player["hunger"] + 30
    )

    show_message("Comeste alguma coisa.")


def drink_water():

    if inventory["water"] <= 0:
        show_message("Não tens água!")
        return

    inventory["water"] -= 1

    player["thirst"] = min(
        100,
        player["thirst"] + 35
    )

    show_message("Bebeste água.")


def build_shelter():

    global shelter

    if shelter is not None:
        show_message("Já tens um abrigo!")
        return

    if inventory["wood"] < 8:
        show_message("Precisas de 8 madeiras.")
        return

    if inventory["stone"] < 3:
        show_message("Precisas de 3 pedras.")
        return

    inventory["wood"] -= 8
    inventory["stone"] -= 3

    shelter = {
        "x": player["x"],
        "y": player["y"]
    }

    show_message(
        "Construíste o teu abrigo!"
    )


def update_survival():

    global time_counter
    global day
    global is_night

    time_counter += 1

    if time_counter % 30 == 0:

        player["hunger"] -= 1
        player["thirst"] -= 2

    if player["hunger"] <= 0:

        player["health"] -= 1

    if player["thirst"] <= 0:

        player["health"] -= 2

    # Ciclo dia/noite
    if time_counter % 600 == 0:

        day += 1

        is_night = not is_night

        if is_night:
            show_message(
                f"Noite do dia {day}!"
            )
        else:
            show_message(
                f"Dia {day} começou!"
            )

    player["hunger"] = max(
        0,
        player["hunger"]
    )

    player["thirst"] = max(
        0,
        player["thirst"]
    )

    player["health"] = max(
        0,
        player["health"]
    )


# =========================================================
# DESENHAR MAPA
# =========================================================

def draw_map():

    # Ilha
    screen.fill(WATER)

    pygame.draw.rect(
        screen,
        SAND,
        (45, 55, WIDTH - 90, HEIGHT - 95)
    )

    # Zona de floresta
    pygame.draw.rect(
        screen,
        (135, 185, 105),
        (60, 80, 250, 180)
    )

    # Lago
    pygame.draw.ellipse(
        screen,
        WATER,
        (570, 270, 150, 90)
    )

    # Montanha
    pygame.draw.polygon(
        screen,
        (100, 100, 90),
        [
            (400, 80),
            (500, 180),
            (300, 180)
        ]
    )

    # Recursos
    for resource in resources:

        if resource["amount"] <= 0:
            continue

        if resource["type"] == "tree":
            draw_tree(
                resource["x"],
                resource["y"]
            )

        elif resource["type"] == "rock":
            draw_rock(
                resource["x"],
                resource["y"]
            )

        elif resource["type"] == "food":
            draw_food(
                resource["x"],
                resource["y"]
            )

    draw_shelter()


# =========================================================
# INTERFACE
# =========================================================

def draw_interface():

    # Painel superior
    pygame.draw.rect(
        screen,
        (25, 25, 25),
        (0, 0, WIDTH, 55)
    )

    draw_text(
        f"🏝️ ILHA PERDIDA",
        15,
        10,
        BIG_FONT
    )

    draw_text(
        f"Dia {day}",
        220,
        17
    )

    draw_bar(
        300,
        8,
        130,
        18,
        player["health"],
        RED,
        "❤️ Vida"
    )

    draw_bar(
        445,
        8,
        130,
        18,
        player["hunger"],
        YELLOW,
        "🍖 Fome"
    )

    draw_bar(
        590,
        8,
        130,
        18,
        player["thirst"],
        WATER,
        "💧 Sede"
    )

    # Inventário
    pygame.draw.rect(
        screen,
        (25, 25, 25),
        (10, HEIGHT - 48, 400, 38)
    )

    draw_text(
        f"🪵 {inventory['wood']}   "
        f"🪨 {inventory['stone']}   "
        f"🍎 {inventory['food']}   "
        f"💧 {inventory['water']}",
        20,
        HEIGHT - 38,
        SMALL_FONT
    )

    # Mensagem
    if message_timer > 0:

        pygame.draw.rect(
            screen,
            (25, 25, 25),
            (420, HEIGHT - 48, 470, 38)
        )

        draw_text(
            message,
            430,
            HEIGHT - 38,
            SMALL_FONT
        )


# =========================================================
# MOVIMENTO
# =========================================================

def move_player(keys):

    dx = 0
    dy = 0

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        dy -= 1

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        dy += 1

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        dx -= 1

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        dx += 1

    # Normalizar diagonal
    if dx != 0 and dy != 0:

        dx *= 0.707
        dy *= 0.707

    player["x"] += dx * player["speed"]
    player["y"] += dy * player["speed"]

    # Limites da ilha
    player["x"] = max(
        60,
        min(WIDTH - 60, player["x"])
    )

    player["y"] = max(
        80,
        min(HEIGHT - 65, player["y"])
    )


# =========================================================
# JOGO PRINCIPAL
# =========================================================

running = True

while running:

    clock.tick(60)

    # Eventos
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_e:
                collect_resource()

            if event.key == pygame.K_f:
                build_shelter()

            if event.key == pygame.K_r:
                # Reiniciar o programa
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_q:
                eat_food()

            if event.key == pygame.K_x:
                drink_water()

    # Movimento
    keys = pygame.key.get_pressed()

    if player["health"] > 0:
        move_player(keys)

    # Sobrevivência
    update_survival()

    # Mensagem
    if message_timer > 0:
        message_timer -= 1

    # =====================================================
    # DESENHO
    # =====================================================

    draw_map()

    # Efeito de noite
    if is_night:

        night_surface = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        night_surface.fill(
            (10, 15, 40, 120)
        )

        screen.blit(
            night_surface,
            (0, 0)
        )

    draw_player()
    draw_interface()

    # Jogador morto
    if player["health"] <= 0:

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 180)
        )

        screen.blit(
            overlay,
            (0, 0)
        )

        draw_text(
            "FICASTE SEM FORÇAS",
            WIDTH // 2 - 150,
            HEIGHT // 2 - 30,
            BIG_FONT,
            WHITE
        )

        draw_text(
            "Pressiona R para reiniciar",
            WIDTH // 2 - 120,
            HEIGHT // 2 + 15,
            FONT,
            WHITE
        )

    pygame.display.flip()


pygame.quit()
