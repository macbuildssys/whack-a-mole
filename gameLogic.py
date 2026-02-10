import pygame
import random
import time

# Colour constants
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
BROWN = (139, 90, 43)
DARK_BROWN = (101, 67, 33)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 30, 30)
GREY = (200, 200, 200)
LIGHT_GREEN = (144, 238, 144)
DARK_GREY = (100, 100, 100)
GOLD = (255, 215, 0)
ORANGE = (255, 140, 0)


def draw_grid(screen, grid_size, width, height):
    """Draw the game grid with styled holes."""
    hole_size = width // grid_size
    for row in range(grid_size):
        for col in range(grid_size):
            rect = pygame.Rect(col * hole_size, row * hole_size, hole_size, hole_size)
            # Draw cell background
            pygame.draw.rect(screen, LIGHT_GREEN, rect)
            pygame.draw.rect(screen, DARK_GREEN, rect, 3)
            # Draw hole (dark circle)
            centre_x = col * hole_size + hole_size // 2
            centre_y = row * hole_size + hole_size // 2
            pygame.draw.circle(screen, DARK_BROWN, (centre_x, centre_y), hole_size // 3)
            pygame.draw.circle(screen, BROWN, (centre_x, centre_y), hole_size // 3, 3)


def draw_score(score, font, screen):
    """Display the current score."""
    score_text = font.render(f"Score: {score}", True, WHITE)
    # Background box for readability
    bg_rect = score_text.get_rect(topleft=(10, 10))
    bg_rect.inflate_ip(16, 8)
    pygame.draw.rect(screen, BLACK, bg_rect, border_radius=6)
    screen.blit(score_text, (10, 10))


def draw_timer(start_time, game_started, timer_duration, font, screen, width, height):
    """Display the countdown timer."""
    if game_started and start_time:
        elapsed_time = time.time() - start_time
        remaining_time = max(0, timer_duration - int(elapsed_time))
        # Change colour when time is running low
        colour = RED if remaining_time <= 15 else WHITE
        timer_text = font.render(f"Time: {remaining_time}s", True, colour)
        bg_rect = timer_text.get_rect(topleft=(width - 160, 10))
        bg_rect.inflate_ip(16, 8)
        pygame.draw.rect(screen, BLACK, bg_rect, border_radius=6)
        screen.blit(timer_text, (width - 160, 10))


def draw_mole(mole_position, screen, width, height, mole_size, grid_size):
    """Draw the mole at its current position."""
    if mole_position is not None:
        row, col = mole_position
        hole_size = width // grid_size
        centre_x = col * hole_size + hole_size // 2
        centre_y = row * hole_size + hole_size // 2
        radius = mole_size // 2

        # Mole body
        pygame.draw.circle(screen, BROWN, (centre_x, centre_y), radius)
        pygame.draw.circle(screen, DARK_BROWN, (centre_x, centre_y), radius, 3)

        # Eyes
        eye_offset = radius // 3
        eye_radius = radius // 6
        pygame.draw.circle(screen, WHITE, (centre_x - eye_offset, centre_y - eye_offset), eye_radius)
        pygame.draw.circle(screen, BLACK, (centre_x - eye_offset, centre_y - eye_offset), eye_radius // 2)
        pygame.draw.circle(screen, WHITE, (centre_x + eye_offset, centre_y - eye_offset), eye_radius)
        pygame.draw.circle(screen, BLACK, (centre_x + eye_offset, centre_y - eye_offset), eye_radius // 2)

        # Nose
        pygame.draw.circle(screen, RED, (centre_x, centre_y + eye_offset // 2), eye_radius // 2 + 1)


def random_mole(grid_size, mole_position, last_mole_time, current_time, mole_interval=1.0):
    """Spawn a new mole at a random position after the interval."""
    if mole_position is None or current_time - last_mole_time >= mole_interval:
        new_position = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
        # Avoid spawning in the same spot twice in a row
        while new_position == mole_position and grid_size > 1:
            new_position = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
        mole_position = new_position
        last_mole_time = current_time
    return mole_position, last_mole_time


def check_hit(pos, mole_position, hit_sound, miss_sound, score, width, height, mole_size, grid_size):
    """Check whether the player clicked on the mole."""
    if mole_position is not None:
        row, col = mole_position
        hole_size = width // grid_size
        centre_x = col * hole_size + hole_size // 2
        centre_y = row * hole_size + hole_size // 2
        radius = mole_size // 2

        # Use circular hit detection
        dx = pos[0] - centre_x
        dy = pos[1] - centre_y
        if dx * dx + dy * dy <= radius * radius:
            score += 1
            if hit_sound:
                hit_sound.play()
            mole_position = None  # Remove mole after a successful hit
        else:
            if miss_sound:
                miss_sound.play()
    return mole_position, score


def draw_instructions(screen, width, height):
    """Draw the instructions screen before the game begins."""
    screen.fill((30, 60, 30))

    title_font = pygame.font.SysFont(None, 60)
    heading_font = pygame.font.SysFont(None, 42)
    body_font = pygame.font.SysFont(None, 32)
    small_font = pygame.font.SysFont(None, 28)

    # Title
    title = title_font.render("Whack-a-Mole!", True, GOLD)
    screen.blit(title, (width // 2 - title.get_width() // 2, 40))

    # Decorative line
    pygame.draw.line(screen, GOLD, (width // 4, 100), (3 * width // 4, 100), 2)

    # How to Play heading
    how_to = heading_font.render("How to Play", True, WHITE)
    screen.blit(how_to, (width // 2 - how_to.get_width() // 2, 130))

    instructions = [
        "Moles will pop up from the holes on the grid.",
        "Click on a mole to whack it and earn a point.",
        "Be quick each mole only stays for a moment!",
        "You have 90 seconds to score as many",
        "points as you can.",
        "",
        "Controls:",
        "  Click: Whack a mole",
        "  P: Pause / Resume the game",
    ]

    y = 190
    for line in instructions:
        if line.startswith("Controls:"):
            text = body_font.render(line, True, ORANGE)
        elif line.startswith("  "):
            text = small_font.render(line, True, LIGHT_GREEN)
        else:
            text = body_font.render(line, True, GREY)
        screen.blit(text, (width // 2 - text.get_width() // 2, y))
        y += 36

    # Start prompt
    prompt = heading_font.render("Press  S  to Start", True, GOLD)
    # Pulsing effect
    alpha = int(128 + 127 * abs(((time.time() * 2) % 2) - 1))
    prompt.set_alpha(alpha)
    screen.blit(prompt, (width // 2 - prompt.get_width() // 2, height - 90))


def draw_game_over(screen, width, height, score):
    """Draw the game-over screen with the final score and options."""
    # Semi-transparent overlay
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    title_font = pygame.font.SysFont(None, 56)
    score_font = pygame.font.SysFont(None, 48)
    body_font = pygame.font.SysFont(None, 36)

    # Game Over title
    title = title_font.render("Time's Up!", True, GOLD)
    screen.blit(title, (width // 2 - title.get_width() // 2, height // 2 - 120))

    # Final score
    score_text = score_font.render(f"Your Score: {score}", True, WHITE)
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2 - 50))

    # Rating message
    if score >= 50:
        message = "Absolutely brilliant! Well done!"
    elif score >= 30:
        message = "Jolly good effort!"
    elif score >= 15:
        message = "Not bad at all — keep practising!"
    else:
        message = "Better luck next time!"

    msg_text = body_font.render(message, True, ORANGE)
    screen.blit(msg_text, (width // 2 - msg_text.get_width() // 2, height // 2 + 10))

    # Options
    pygame.draw.line(screen, GOLD, (width // 4, height // 2 + 60), (3 * width // 4, height // 2 + 60), 1)

    option1 = body_font.render("Press  R  to Play Again", True, LIGHT_GREEN)
    option2 = body_font.render("Press  Q  to Quit", True, RED)
    screen.blit(option1, (width // 2 - option1.get_width() // 2, height // 2 + 80))
    screen.blit(option2, (width // 2 - option2.get_width() // 2, height // 2 + 125))