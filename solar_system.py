import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Accelerating Solar System - CGD Test")

# Clock for managing frame rate
clock = pygame.time.Clock()

# Sun properties
sun_x = 0
sun_y = 80
sun_speed = 5  # Initial speed in pixels per frame
sun_image = None
sun_rect = None

# Load sun image
try:
    sun_image_normal = pygame.image.load("imgs/bright-golden-cartoon-sun-rays.png").convert_alpha()
    sun_width = 100
    sun_height = 105
    sun_image_normal = pygame.transform.scale(sun_image_normal, (sun_width, sun_height))
    sun_image = sun_image_normal.copy()
    sun_rect = sun_image.get_rect()
    print("[OK] Sun image loaded successfully!")
except Exception as e:
    print(f"[ERROR] Could not load sun image: {e}")
    sun_image = None

# Timer properties
SPEED_INCREASE_INTERVAL = 3000  # 3000ms = 3 seconds
last_speed_increase_time = pygame.time.get_ticks()
timer_paused = False

# Font for displaying info
font = pygame.font.Font(None, 28)


def colorize_image(image, color):
    """Create a colorized version of the image"""
    size = image.get_size()
    colored = pygame.Surface(size, pygame.SRCALPHA)

    for x in range(size[0]):
        for y in range(size[1]):
            pixel = image.get_at((x, y))
            if pixel.a > 0:  # If not transparent
                colored.set_at((x, y), (*color, pixel.a))

    return colored


def reset_timer():
    """Reset the speed increase timer"""
    global last_speed_increase_time, timer_paused
    last_speed_increase_time = pygame.time.get_ticks()
    timer_paused = False


def main():
    global sun_x, sun_speed, sun_rect, last_speed_increase_time, timer_paused

    # Create tinted versions of the sun image
    sun_image_normal = None
    sun_image_flare = None

    try:
        sun_image_normal = pygame.image.load("imgs/bright-golden-cartoon-sun-rays.png").convert_alpha()
        sun_image_normal = pygame.transform.scale(sun_image_normal, (100, 105))

        # Create red-tinted version for solar flare
        sun_image_flare = colorize_image(sun_image_normal, RED)
    except Exception as e:
        print(f"[ERROR] Could not create tinted images: {e}")

    running = True

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Check if spacebar is held down
        keys = pygame.key.get_pressed()
        spacebar_held = keys[pygame.K_SPACE]

        # Get current time
        current_time = pygame.time.get_ticks()

        # Handle solar flare effect
        if spacebar_held:
            if not timer_paused:
                timer_paused = True
                print(f"[SOLAR FLARE] Timer paused at speed: {sun_speed:.2f}")
        else:
            # Handle timer restart after flare ends
            if timer_paused:
                reset_timer()
                print(f"[FLARE END] Timer resumed, speed is now: {sun_speed:.2f}")

            # Check if 3000ms has passed for speed increase
            if current_time - last_speed_increase_time >= SPEED_INCREASE_INTERVAL:
                old_speed = sun_speed
                sun_speed *= 1.10  # Increase by 10%
                last_speed_increase_time = current_time

                # Print new speed to console
                print(f"[SPEED INCREASE] {old_speed:.2f} -> {sun_speed:.2f} (+10%)")

        # Update sun position (move horizontally)
        sun_x += sun_speed

        # Wrap around when sun hits right edge
        if sun_x > SCREEN_WIDTH + 100:
            sun_x = -100
            print(f"[WRAP] Sun wrapped to left edge at speed: {sun_speed:.2f}")

        # Clear screen
        screen.fill(BLACK)

        # Draw starfield background
        for i in range(50):
            star_x = (i * 97) % SCREEN_WIDTH
            star_y = (i * 53) % SCREEN_HEIGHT
            pygame.draw.circle(screen, WHITE, (star_x, star_y), 1)

        # Draw the sun image
        if sun_image_normal:
            if spacebar_held and sun_image_flare:
                screen.blit(sun_image_flare, (int(sun_x), sun_y))
            else:
                screen.blit(sun_image_normal, (int(sun_x), sun_y))
        else:
            # Fallback: draw a simple circle
            pygame.draw.circle(screen, YELLOW if not spacebar_held else RED, (int(sun_x) + 50, sun_y + 50), 40)

        # Draw UI information
        info_text = font.render(f"Speed: {sun_speed:.2f} px/frame", True, WHITE)
        screen.blit(info_text, (20, SCREEN_HEIGHT - 50))

        # Instructions
        instruction_text = font.render("Hold SPACEBAR for Solar Flare | ESC to quit", True, (150, 150, 150))
        screen.blit(instruction_text, (SCREEN_WIDTH//2 - instruction_text.get_width()//2, SCREEN_HEIGHT - 30))

        # Update display
        pygame.display.flip()

        # Frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    print("=" * 60)
    print("THE ACCELERATING SOLAR SYSTEM - CGD Test")
    print("=" * 60)
    print("\nInstructions:")
    print("- Sun moves horizontally and wraps at right edge")
    print("- Speed increases by 10% every 3 seconds (when spacebar NOT held)")
    print("- Hold SPACEBAR to trigger Solar Flare (sun turns red, timer pauses)")
    print("- Press ESC to quit")
    print("\nConsole will show speed changes and timer status.")
    print("=" * 60)
    main()