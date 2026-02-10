import pygame
import time
import random
import sys
import os
from gameLogic import (
    draw_grid, draw_score, draw_timer, draw_mole,
    random_mole, check_hit, draw_instructions, draw_game_over,
)

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 600
GRID_SIZE = 3
HOLE_SIZE = WIDTH // GRID_SIZE
MOLE_SIZE = HOLE_SIZE - 20
MOLE_INTERVAL = 1.0        # seconds a mole stays visible
TIMER_DURATION = 90         # 90-second game
BG_COLOUR = (34, 120, 34)  # pleasant green background

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whack-a-Mole")
clock = pygame.time.Clock()
  
def load_sound(name):
    """Try .mp3 first, then .wav, then return None."""
    for ext in ("mp3", "wav"):
        path = os.path.join(os.path.dirname(__file__) or ".", f"{name}.{ext}")
        if os.path.isfile(path):
            try:
                return pygame.mixer.Sound(path)
            except Exception:
                pass
    return None

hit_sound = load_sound("hit")
miss_sound = load_sound("miss")

if hit_sound is None or miss_sound is None:
    print("Warning: One or more sound files (hit.mp3/.wav, miss.mp3/.wav) "
          "were not found. The game will run without sound.")

font = pygame.font.SysFont(None, 40)

STATE_INSTRUCTIONS = "instructions"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"

def reset_game():
    """Return a fresh set of game variables."""
    return {
        "score": 0,
        "mole_position": None,
        "last_mole_time": 0,
        "start_time": None,
        "elapsed_before_pause": 0,
        "state": STATE_INSTRUCTIONS,
    }

def main():
    game = reset_game()
    running = True

    while running:
        current_time = time.time()

        # Event handling 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and game["state"] == STATE_INSTRUCTIONS:
                    game["state"] = STATE_PLAYING
                    game["score"] = 0
                    game["start_time"] = time.time()
                    game["elapsed_before_pause"] = 0
                    game["mole_position"] = None

                elif event.key == pygame.K_p:
                    if game["state"] == STATE_PLAYING:
                        game["state"] = STATE_PAUSED
                        # Record how much time has already elapsed
                        game["elapsed_before_pause"] += (
                            time.time() - game["start_time"]
                        )
                    elif game["state"] == STATE_PAUSED:
                        game["state"] = STATE_PLAYING
                        game["start_time"] = time.time()

                elif game["state"] == STATE_GAME_OVER:
                    if event.key == pygame.K_r:
                        game = reset_game()          # Play again
                    elif event.key == pygame.K_q:
                        running = False               # Quit

            # Click to whack a mole
            elif (event.type == pygame.MOUSEBUTTONDOWN
                  and game["state"] == STATE_PLAYING):
                pos = pygame.mouse.get_pos()
                game["mole_position"], game["score"] = check_hit(
                    pos, game["mole_position"],
                    hit_sound, miss_sound, game["score"],
                    WIDTH, HEIGHT, MOLE_SIZE, GRID_SIZE,
                )

        if game["state"] == STATE_PLAYING:
            # Calculate total elapsed time (accounts for pauses)
            total_elapsed = (
                game["elapsed_before_pause"]
                + (time.time() - game["start_time"])
            )

            # Check for game over
            if total_elapsed >= TIMER_DURATION:
                game["state"] = STATE_GAME_OVER
            else:
                # Spawn moles
                game["mole_position"], game["last_mole_time"] = random_mole(
                    GRID_SIZE,
                    game["mole_position"],
                    game["last_mole_time"],
                    current_time,
                    MOLE_INTERVAL,
                )

        if game["state"] == STATE_INSTRUCTIONS:
            draw_instructions(screen, WIDTH, HEIGHT)

        elif game["state"] in (STATE_PLAYING, STATE_PAUSED):
            screen.fill(BG_COLOUR)
            draw_grid(screen, GRID_SIZE, WIDTH, HEIGHT)
            draw_mole(
                game["mole_position"], screen,
                WIDTH, HEIGHT, MOLE_SIZE, GRID_SIZE,
            )
            draw_score(game["score"], font, screen)

            effective_start = time.time() - game["elapsed_before_pause"]
            if game["state"] == STATE_PLAYING:
                effective_start -= (time.time() - game["start_time"])
                # Re-derive: effective_start such that elapsed = now - effective_start
                effective_start = time.time() - (
                    game["elapsed_before_pause"]
                    + (time.time() - game["start_time"])
                )
            else:
                effective_start = time.time() - game["elapsed_before_pause"]

            draw_timer(
                effective_start, True,
                TIMER_DURATION, font, screen, WIDTH, HEIGHT,
            )

            if game["state"] == STATE_PAUSED:
                # Show paused overlay
                pause_font = pygame.font.SysFont(None, 56)
                pause_text = pause_font.render("Paused", True, (255, 215, 0))
                screen.blit(
                    pause_text,
                    (WIDTH // 2 - pause_text.get_width() // 2,
                     HEIGHT // 2 - pause_text.get_height() // 2),
                )

        elif game["state"] == STATE_GAME_OVER:
            screen.fill(BG_COLOUR)
            draw_grid(screen, GRID_SIZE, WIDTH, HEIGHT)
            draw_game_over(screen, WIDTH, HEIGHT, game["score"])

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()