import sys
import random
import pygame

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wizardy_Kitty_VS_The_World")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 192, 203)
RED = (220, 20, 60)
PURPLE = (172, 79, 198)

# Load the character images with a specific size
character_size = (60, 70)
character_image_up = pygame.image.load("catwalkingup.png")
character_image_up_animated = pygame.image.load("catwalkingup2.png")

character_image_left = pygame.image.load("catwalkingleft.png")
character_image_left_animated = pygame.image.load("catwalkingleft2.png")

character_image_right = pygame.image.load("sidewalkingright.png")
character_image_right_animated = pygame.image.load("sidewalkingright2.png")

character_image_down = pygame.image.load("maincharactercat.png")
character_image_down_animated = pygame.image.load("maincharacter2.png")

# Set the initial character image and animation timer
character_images = {
    "up": [pygame.transform.scale(character_image_up, character_size), pygame.transform.scale(character_image_up_animated, character_size)],
    "left": [pygame.transform.scale(character_image_left, character_size), pygame.transform.scale(character_image_left_animated, character_size)],
    "right": [pygame.transform.scale(character_image_right, character_size), pygame.transform.scale(character_image_right_animated, character_size)],
    "down": [pygame.transform.scale(character_image_down, character_size), pygame.transform.scale(character_image_down_animated, character_size)]
}

character_index = 0  # Added initialization
current_direction = "down"  # Default direction
character_image = character_images[current_direction][0]
animation_timer = pygame.time.get_ticks()

# Set character initial position
character_rect = character_image.get_rect()
character_rect.x = WIDTH // 2 - character_rect.width // 2
character_rect.y = HEIGHT - character_rect.height - 20

# Set up clock
clock = pygame.time.Clock()

# Set up game variables
enemy_speed = 3  # Slightly faster enemies
enemy_frequency = 20  # Adjusted frequency
enemies = []

# Set up lasers
lasers = []
laser_speed = 7  # Slightly faster lasers
laser_cooldown = 500  # Cooldown in milliseconds
last_laser_time = pygame.time.get_ticks()  # Record the time of the last fired laser

# Load the monster image with a specific size
monster_image = pygame.image.load("ugly_monster.png")
monster_size = (40, 40)
monster_image = pygame.transform.scale(monster_image, monster_size)

# Load the heart image with a specific size
heart_image = pygame.image.load("heartgame.png")
heart_size = (20, 20)
heart_image = pygame.transform.scale(heart_image, heart_size)

# Load the fire images for lasers with a specific size
fire_images = [
    pygame.image.load("fire1.png"),
    pygame.image.load("fire2.png"),
    pygame.image.load("fire3.png"),
    pygame.image.load("fire4.png")
]

fire_size = (20, 40)
fire_images = [pygame.transform.scale(image, fire_size) for image in fire_images]
current_fire_index = 0

# Create a pixelated font
pixel_font = pygame.font.Font(None, 20)

# Create stars for the animated background
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)) for _ in range(100)]

# Set up lives and score
lives = 3
score = 0
life_images = [heart_image for _ in range(lives)]

# Load the game over and game won images
game_over_image = pygame.image.load("gameovercat.png")
game_over_image = pygame.transform.scale(game_over_image, (400, 300))
you_win_text = pixel_font.render("You Win!", True, WHITE)  # "You Win" text

# Load the background image
background_image = pygame.image.load("snow.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Set initial background position
bg_y = 0

# Flag to track whether the game is running
game_running = True

# Game loop
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    keys = pygame.key.get_pressed()
    character_speed = 5  # Slightly faster character

    # Move character based on key presses
    if keys[pygame.K_LEFT] and character_rect.x > 0:
        character_rect.x -= character_speed
        current_direction = "left"
    if keys[pygame.K_RIGHT] and character_rect.x < WIDTH - character_rect.width:
        character_rect.x += character_speed
        current_direction = "right"
    if keys[pygame.K_UP] and character_rect.y > 0:
        character_rect.y -= character_speed
        current_direction = "up"
    if keys[pygame.K_DOWN] and character_rect.y < HEIGHT - character_rect.height:
        character_rect.y += character_speed
        current_direction = "down"

    # Switch between animated and non-animated images every 200 milliseconds
    current_time = pygame.time.get_ticks()
    if current_time - animation_timer > 200:
        animation_timer = current_time
        character_index = 1 if character_index == 0 else 0  # Toggle between 0 and 1
        character_image = character_images[current_direction][character_index]

    # Shoot lasers on SPACE key press with a cooldown
    if keys[pygame.K_SPACE] and current_time - last_laser_time > laser_cooldown:
        last_laser_time = current_time
        laser = pygame.Rect(character_rect.x + character_rect.width // 2 - 10, character_rect.y, 20, 40)
        lasers.append({"rect": laser, "fire_index": current_fire_index})
        current_fire_index = (current_fire_index + 1) % len(fire_images)

    # Move lasers
    lasers_to_remove = []
    for laser in lasers:
        laser["rect"].y -= laser_speed
        if laser["rect"].y < 0:
            lasers_to_remove.append(laser)

    # Spawn enemies
    if random.randint(1, enemy_frequency) == 1:
        enemy_size = random.randint(20, 40)
        enemy = pygame.Rect(random.randint(0, WIDTH - enemy_size), 0, enemy_size, enemy_size)
        enemies.append(enemy)

    # Move enemies
    enemies_to_remove = []
    for enemy in enemies:
        enemy.y += enemy_speed
        if enemy.y > HEIGHT:
            enemies_to_remove.append(enemy)

    # Remove off-screen enemies
    for enemy in enemies_to_remove:
        enemies.remove(enemy)

    # Collision detection for lasers and enemies
    for laser in lasers:
        for enemy in enemies:
            if laser["rect"].colliderect(enemy):
                lasers_to_remove.append(laser)
                enemies_to_remove.append(enemy)
                score += 5  # Increase score by 5 when a monster is hit

    # Remove collided lasers and enemies

    # Collision detection for character and enemies
    for enemy in enemies:
        if character_rect.colliderect(enemy):
            print("Collision detected with enemy!")
            enemies_to_remove.append(enemy)
            lives -= 1  # Decrement lives when the character is hit

            # Update the heart images based on remaining lives
            life_images = [heart_image for _ in range(lives)]

    # Remove enemies that collided with the character
    for enemy in enemies_to_remove:
        if enemy in enemies:
            enemies.remove(enemy)

    # Game over logic outside the loop
    if lives <= 0:
        screen.blit(game_over_image, (WIDTH // 2 - 200, HEIGHT // 2 - 150))
        pygame.display.flip()
        pygame.time.delay(3000)
        character_rect.x = WIDTH // 2 - character_rect.width // 2
        character_rect.y = HEIGHT - character_rect.height - 20
        enemies.clear()
        lasers.clear()
        lives = 3
        score = 0

    # Winning condition
    if score >= 100:
        screen.blit(you_win_text, (WIDTH // 2 - 50, HEIGHT // 2 - 25))
        pygame.display.flip()
        pygame.time.delay(3000)
        game_running = False

    # Draw background with scrolling effect
    screen.blit(background_image, (0, bg_y))
    screen.blit(background_image, (0, bg_y - HEIGHT))

    # Draw stars
    for star in stars:
        pygame.draw.circle(screen, WHITE, (star[0], star[1]), star[2])

    # Draw lives and score
    for i, life_image in enumerate(life_images):
        screen.blit(life_image, (10 + i * 25, 10))

    score_text = pixel_font.render("Score: " + str(score), True, PURPLE)
    screen.blit(score_text, (WIDTH - 100, 10))

    screen.blit(character_image, character_rect)

    # Draw monsters
    for enemy in enemies:
        screen.blit(monster_image, enemy)

    # Draw lasers
    for laser in lasers:
        fire_index = laser["fire_index"]
        screen.blit(fire_images[fire_index], laser["rect"])

    pygame.display.flip()

    # Update star positions for the animated background
    stars = [(x, (y + 1) % HEIGHT, size) for x, y, size in stars]

    # Set frame rate
    clock.tick(30)  # Adjusted frame rate

pygame.quit()
sys.exit()
