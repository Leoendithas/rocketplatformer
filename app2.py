import pygame
import random
import math
import sys
import os
import base64
from io import BytesIO

# Try to initialize with audio, fall back to no audio if needed
try:
    pygame.mixer.init()
    audio_available = True
except pygame.error:
    # We're likely on a server with no audio device
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    audio_available = False

# Initialize the rest of pygame
pygame.init()

# Later in your code, when playing sounds:
def play_sound(sound_file):
    if audio_available:
        try:
            sound = pygame.mixer.Sound(sound_file)
            sound.play()
        except:
            pass  # Silently fail if sound still doesn't work

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLANE_WIDTH = 60
PLANE_HEIGHT = 30
GRAVITY = 0.2
FLIGHT_POWER = 0.5
ASTEROID_SIZE = 40
FUEL_SIZE = 30
STAR_SIZE = 25
INITIAL_SCROLL_SPEED = 2
MAX_BATTERY = 100
BATTERY_DRAIN_RATE = 1      # Battery drain per second
BATTERY_RECHARGE = 30
COLLISION_COOLDOWN = 1000   # milliseconds
SCORE_PER_SECOND = 10
SCORE_PER_STAR = 100
FPS = 60
LEVEL_COUNT = 5             # Total levels

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 31, 84)
BLUE = (0, 87, 150)
LIGHT_BLUE = (100, 151, 177)
RED = (244, 67, 54)
GREEN = (76, 175, 80)
YELLOW = (255, 215, 0)
ORANGE = (255, 102, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sky Navigator")
clock = pygame.time.Clock()

# Load fonts
font_small = pygame.font.SysFont("Arial", 14)
font_medium = pygame.font.SysFont("Arial", 24)
font_large = pygame.font.SysFont("Arial", 48)

# Function to create embedded images (for standalone file)
def create_image_from_base64(base64_string, size=None):
    try:
        image_data = base64.b64decode(base64_string)
        image_file = BytesIO(image_data)
        image = pygame.image.load(image_file)
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except Exception as e:
        print(f"Error loading image: {e}")
        surf = pygame.Surface(size if size else (30, 30))
        surf.fill(YELLOW)
        return surf

# Base64 encoded images
plane_base64 = """
PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2MCAzMCI+PHBhdGggZD0iTTYwLDE1YzAtMi43LTYuMy01LTE1LTVIMzBMMCwzMGgzMGwxNSw5LDYtMTJjNS43LTAuMyw5LTIuMSw5LTUuNiIgZmlsbD0iI2ZmZiIvPjxwYXRoIGQ9Ik0zMCwzMGgxNWw2LTEyYzAtMS0xLTItMy0zSDMwbC02LDEyIiBmaWxsPSIjZmZkNzAwIi8+PHBhdGggZD0iTTYwLDE1YzAtMi43LTYuMy01LTE1LTVIMzBMMCwzMGgzMGwxNSw5LDYtMTJjNS43LTAuMyw5LTIuMSw5LTUuNiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDAwIiBzdHJva2Utd2lkdGg9IjEuNSIvPjxlbGxpcHNlIGN4PSI0MyIgY3k9IjE1IiByeD0iMyIgcnk9IjIiIGZpbGw9IiMzMzMiLz48L3N2Zz4=
"""

asteroid_base64 = """
PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0MCA0MCI+PHBhdGggZD0iTTIwLDBjMyw1IDgsMyAxMCw1czIsOCA1LDEwLTMsOC01LDEwLTgsMi0xMCw1LTgsLTMtMTAsLTUtMi04LTUtMTAsMy04IDUtMTBDMTIsMiAxNyw1IDIwLDAiIGZpbGw9IiM4MDgwODAiIHN0cm9rZT0iIzMzMyIgc3Ryb2tlLXdpZHRoPSIxLjUiLz48Y2lyY2xlIGN4PSIxNSIgY3k9IjE1IiByPSIzIiBmaWxsPSIjNjY2Ii8+PGNpcmNsZSBjeD0iMjgiIGN5PSIyMCIgcj0iNCIgZmlsbD0iIzY2NiIvPjxjaXJjbGUgY3g9IjIwIiBjeT0iMjgiIHI9IjIiIGZpbGw9IiM2NjYiLz48L3N2Zz4=
"""

fuel_base64 = """
PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMCAzMCI+PHJlY3QgeD0iNSIgeT0iNSIgd2lkdGg9IjIwIiBoZWlnaHQ9IjI1IiByeD0iMyIgcnk9IjMiIGZpbGw9IiNkZGQiIHN0cm9rZT0iIzMzMyIgc3Ryb2tlLXdpZHRoPSIxLjUiLz48cmVjdCB4PSI4IiB5PSI4IiB3aWR0aD0iMTQiIGhlaWdodD0iMTYiIGZpbGw9IiM0Y2FmNTAiLz48cmVjdCB4PSIxMiIgeT0iMCIgd2lkdGg9IjYiIGhlaWdodD0iNSIgZmlsbD0iIzY2NiIvPjwvc3ZnPg==
"""

star_base64 = """
PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNSAyNSI+PHBhdGggZD0iTTEyLjUsMWw0LDgsOCwxLTYsNiwxLjUsOEwxMi41LDIwLDUsMjRsMS41LTgtNi02LDgtMVoiIGZpbGw9IiNmZmQ3MDAiIHN0cm9rZT0iI2ZmODYwMCIgc3Ryb2tlLXdpZHRoPSIxIi8+PC9zdmc+
"""

finish_base64 = """
PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2MCAzMDAiPjxyZWN0IHdpZHRoPSI2MCIgaGVpZ2h0PSIzMDAiIGZpbGw9IiMzMzMiLz48cGF0aCBkPSJNMCwwaDYwdjMwSDBWMzBoNjB2MzBIMFY2MGg2MHYzMEgwVjkwaDYwdjMwSDBWMTIwaDYwdjMwSDBWMTUwaDYwdjMwSDBWMTgwaDYwdjMwSDBWMjEwaDYwdjMwSDBWMjQwaDYwdjMwSDBWMjcwaDYwdjMwSDBWMzAwWiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjZmZmIiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlLWRhc2hhcnJheT0iMzAsMzAiLz48dGV4dCB4PSI1IiB5PSIxNTAiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIyMCIgZmlsbD0iI2ZmZiIgdHJhbnNmb3JtPSJyb3RhdGUoOTAsMzAsMTUwKSI+RklOSVNIPC90ZXh0Pjwvc3ZnPg==
"""

# Load images
plane_img = create_image_from_base64(plane_base64, (PLANE_WIDTH, PLANE_HEIGHT))
asteroid_img = create_image_from_base64(asteroid_base64, (ASTEROID_SIZE, ASTEROID_SIZE))
fuel_img = create_image_from_base64(fuel_base64, (FUEL_SIZE, FUEL_SIZE))
star_img = create_image_from_base64(star_base64, (STAR_SIZE, STAR_SIZE))
finish_img = create_image_from_base64(finish_base64, (60, SCREEN_HEIGHT))

# Game classes
class Plane:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLANE_WIDTH
        self.height = PLANE_HEIGHT
        self.velocity_y = 0
        self.velocity_x = 0
        self.max_velocity_x = 5
        self.min_velocity_x = -2
        self.rect = pygame.Rect(x, y, PLANE_WIDTH, PLANE_HEIGHT)
    
    def update(self, keys):
        # Apply gravity
        self.velocity_y += GRAVITY
        
        # Apply player input
        if keys[pygame.K_UP]:
            self.velocity_y -= FLIGHT_POWER
        if keys[pygame.K_DOWN]:
            self.velocity_y += FLIGHT_POWER / 2
        if keys[pygame.K_RIGHT]:
            self.velocity_x += 0.1
            if self.velocity_x > self.max_velocity_x:
                self.velocity_x = self.max_velocity_x
        elif keys[pygame.K_LEFT]:
            self.velocity_x -= 0.1
            if self.velocity_x < self.min_velocity_x:
                self.velocity_x = self.min_velocity_x
        else:
            # Gradually return to normal speed
            if self.velocity_x > 0:
                self.velocity_x -= 0.05
            elif self.velocity_x < 0:
                self.velocity_x += 0.05
            if abs(self.velocity_x) < 0.1:
                self.velocity_x = 0
        
        # Update position
        self.y += self.velocity_y
        
        # Keep plane within top bound only; touching the bottom will trigger a crash
        if self.y < 0:
            self.y = 0
            self.velocity_y = 0
        
        # Update rect for collision detection
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, surface, is_colliding):
        # Draw thrust effect if accelerating
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            points = [
                (self.x, self.y + self.height / 2),
                (self.x - 15, self.y + self.height / 2 - 10),
                (self.x - 25, self.y + self.height / 2),
                (self.x - 15, self.y + self.height / 2 + 10),
            ]
            pygame.draw.polygon(surface, ORANGE, points)
        # Flash if colliding
        if is_colliding:
            if pygame.time.get_ticks() % 200 < 100:
                surface.blit(plane_img, (self.x, self.y))
        else:
            surface.blit(plane_img, (self.x, self.y))

class GameObject:
    def __init__(self, x, y, width, height, obj_type, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = obj_type
        self.image = image
        self.active = True
        self.rect = pygame.Rect(x, y, width, height)
        # For moving asteroids (set later if needed)
        self.moving = False

    def update(self, level_position):
        # If this is a moving asteroid, add an oscillating offset
        if self.type == 'asteroid' and self.moving:
            # Calculate oscillation offset using time elapsed since spawn
            t = (pygame.time.get_ticks() - self.spawn_time) / 1000.0
            offset = self.oscillation_amplitude * math.sin(t * self.oscillation_speed)
            current_x = self.x + offset
            self.rect.x = current_x - level_position
        else:
            self.rect.x = self.x - level_position
        self.rect.y = self.y
    
    def draw(self, surface, level_position):
        if self.active:
            screen_x = self.x - level_position
            # For moving asteroids, recalc using oscillation offset
            if self.type == 'asteroid' and self.moving:
                t = (pygame.time.get_ticks() - self.spawn_time) / 1000.0
                offset = self.oscillation_amplitude * math.sin(t * self.oscillation_speed)
                screen_x = (self.x + offset) - level_position
            if -self.width <= screen_x <= SCREEN_WIDTH:
                surface.blit(self.image, (screen_x, self.y))
                
    def check_collision(self, other_rect):
        return self.active and self.rect.colliderect(other_rect)

class Game:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.plane = Plane(150, SCREEN_HEIGHT / 2)
        self.level = 1
        self.score = 0
        self.battery_level = MAX_BATTERY
        self.scroll_speed = INITIAL_SCROLL_SPEED
        self.game_active = False
        self.game_over = False
        self.level_complete = False
        self.level_position = 0
        self.game_objects = []
        self.is_colliding = False
        self.last_collision_time = 0
        self.start_time = 0
        self.win = False  # Indicates completion of level 5
    
    def start_game(self):
        self.reset()
        self.game_active = True
        self.init_level(self.level)
        self.start_time = pygame.time.get_ticks()
    
    def next_level(self):
        if self.level < LEVEL_COUNT:
            self.level += 1
            self.plane = Plane(150, SCREEN_HEIGHT / 2)
            self.battery_level = MAX_BATTERY
            self.scroll_speed = INITIAL_SCROLL_SPEED + (self.level * 0.5)
            self.game_active = True
            self.level_complete = False
            self.init_level(self.level)
        else:
            # Already at final level: mark win (this state is set when finish line is reached)
            self.win = True

    def init_level(self, level_num):
        self.game_objects = []
        self.level_position = 0
        level_length = 5000
        
        # Create asteroids (obstacles)
        asteroid_count = 20 + (level_num * 5)
        for i in range(asteroid_count):
            x = random.random() * (level_length - 500) + 500  # Clear first 500px
            y = random.random() * (SCREEN_HEIGHT - ASTEROID_SIZE)
            asteroid = GameObject(x, y, ASTEROID_SIZE, ASTEROID_SIZE, 'asteroid', asteroid_img)
            # For levels 3 and above, asteroids start moving
            if level_num >= 3:
                asteroid.moving = True
                asteroid.oscillation_speed = random.uniform(1, 3)
                asteroid.oscillation_amplitude = random.randint(10, 30)
                asteroid.spawn_time = pygame.time.get_ticks()
            self.game_objects.append(asteroid)
        
        # Create fuel canisters
        fuel_count = 10 + level_num
        for i in range(fuel_count):
            x = random.random() * (level_length - 500) + 500
            y = random.random() * (SCREEN_HEIGHT - FUEL_SIZE)
            self.game_objects.append(GameObject(x, y, FUEL_SIZE, FUEL_SIZE, 'fuel', fuel_img))
        
        # Create stars (bonus points)
        star_count = 15 + (level_num * 2)
        for i in range(star_count):
            x = random.random() * (level_length - 500) + 500
            y = random.random() * (SCREEN_HEIGHT - STAR_SIZE)
            self.game_objects.append(GameObject(x, y, STAR_SIZE, STAR_SIZE, 'star', star_img))
        
        # Create a finish line object at the end of the level
        finish_line = GameObject(level_length + 200, 0, 60, SCREEN_HEIGHT, 'finish', finish_img)
        self.game_objects.append(finish_line)
    
    def update(self):
        if not self.game_active:
            return
        
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.start_time) / 1000  # seconds
        self.start_time = current_time
        
        # Update score based on time
        self.score += math.floor(SCORE_PER_SECOND * delta_time)
        
        keys = pygame.key.get_pressed()
        self.plane.update(keys)
        
        # Crash if the plane touches the bottom of the screen
        if self.plane.y + self.plane.height >= SCREEN_HEIGHT:
            self.game_active = False
            self.game_over = True
            return
        
        # Scroll the level
        self.level_position += self.scroll_speed + self.plane.velocity_x
        
        # Update game objects
        for obj in self.game_objects:
            obj.update(self.level_position)
        
        self.check_collisions()
        
        # Drain battery over time
        self.battery_level -= BATTERY_DRAIN_RATE * delta_time
        if self.battery_level <= 0:
            self.battery_level = 0
            self.game_active = False
            self.game_over = True

    def check_collisions(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_collision_time < COLLISION_COOLDOWN:
            self.is_colliding = False
            return
        
        for obj in self.game_objects:
            if obj.check_collision(self.plane.rect):
                if obj.type == 'asteroid':
                    if not self.is_colliding:
                        self.is_colliding = True
                        self.last_collision_time = current_time
                        self.battery_level -= 20
                        if self.battery_level < 0:
                            self.battery_level = 0
                        obj.active = False
                elif obj.type == 'fuel':
                    self.battery_level += BATTERY_RECHARGE
                    if self.battery_level > MAX_BATTERY:
                        self.battery_level = MAX_BATTERY
                    obj.active = False
                elif obj.type == 'star':
                    self.score += SCORE_PER_STAR
                    obj.active = False
                elif obj.type == 'finish':
                    self.game_active = False
                    if self.level < LEVEL_COUNT:
                        self.level_complete = True
                    else:
                        self.win = True

    def draw_background(self):
        screen.fill(DARK_BLUE)
        self.draw_clouds(0.5, LIGHT_BLUE, 30)
        self.draw_clouds(1, BLUE, 20)

    def draw_clouds(self, depth, color, size):
        offset = (self.level_position * depth) % (SCREEN_WIDTH * 2)
        for i in range(10):
            x = ((i * 200) - offset) % (SCREEN_WIDTH * 2) - 100
            y = (math.sin(i * 0.5) * 100) + (SCREEN_HEIGHT / 2)
            pygame.draw.circle(screen, color, (int(x), int(y)), size)
            pygame.draw.circle(screen, color, (int(x + size), int(y - size / 2)), int(size * 0.8))
            pygame.draw.circle(screen, color, (int(x - size), int(y - size / 2)), int(size * 0.7))
            pygame.draw.circle(screen, color, (int(x + size / 2), int(y + size / 2)), int(size * 0.6))
            pygame.draw.circle(screen, color, (int(x - size / 2), int(y + size / 2)), int(size * 0.6))
    
    def draw_ui(self):
        score_text = font_medium.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        battery_bar_width = 200
        battery_bar_height = 20
        pygame.draw.rect(screen, WHITE, (10, 50, battery_bar_width, battery_bar_height), 2)
        fill_width = (self.battery_level / MAX_BATTERY) * battery_bar_width
        pygame.draw.rect(screen, GREEN, (10, 50, fill_width, battery_bar_height))
    
    def draw(self):
        self.draw_background()
        for obj in self.game_objects:
            obj.draw(screen, self.level_position)
        self.plane.draw(screen, self.is_colliding)
        self.draw_ui()
        
        # Draw start, game over, level complete, or win screens
        if not self.game_active and not self.game_over and not self.level_complete and not self.win:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 31, 84, 230))
            screen.blit(overlay, (0, 0))
            title_text = font_large.render("SKY NAVIGATOR", True, YELLOW)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 150))
            screen.blit(title_text, title_rect)
            instructions = [
                "Navigate your plane through a dangerous asteroid field!",
                "",
                "CONTROLS:",
                "↑ - Move Up",
                "↓ - Move Down",
                "← - Slow Down",
                "→ - Speed Up",
                "",
                "Collect fuel to recharge your battery and stars for bonus points!",
                "Reach the finish line to complete the level.",
                "",
                "Press SPACE to start"
            ]
            y = 220
            for line in instructions:
                instruction_text = font_small.render(line, True, WHITE)
                instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, y))
                screen.blit(instruction_text, instruction_rect)
                y += 25
        elif self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))
            gameover_text = font_large.render("GAME OVER", True, RED)
            gameover_rect = gameover_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            screen.blit(gameover_text, gameover_rect)
            score_text = font_medium.render(f"Final Score: {self.score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(score_text, score_rect)
            restart_text = font_small.render("Press SPACE to try again", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            screen.blit(restart_text, restart_rect)
        elif self.level_complete:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))
            complete_text = font_large.render("LEVEL COMPLETE!", True, GREEN)
            complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            screen.blit(complete_text, complete_rect)
            score_text = font_medium.render(f"Score: {self.score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(score_text, score_rect)
            next_text = font_small.render("Press SPACE to continue to the next level", True, WHITE)
            next_rect = next_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            screen.blit(next_text, next_rect)
        elif self.win:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 220))
            screen.blit(overlay, (0, 0))
            win_text = font_large.render("YOU WIN!", True, GREEN)
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            screen.blit(win_text, win_rect)
            final_score = font_medium.render(f"Final Score: {self.score}", True, WHITE)
            score_rect = final_score.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(final_score, score_rect)
            restart_text = font_small.render("Press SPACE to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            screen.blit(restart_text, restart_rect)

# Main game loop function (defined outside the Game class)
def main():
    game = Game()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # If game has not started, start it.
                    if not game.game_active and not game.game_over and not game.level_complete and not game.win:
                        game.start_game()
                    # If level is complete (and not the final win), go to next level.
                    elif game.level_complete:
                        game.next_level()
                    # If game over or win, reset and start again.
                    elif game.game_over or game.win:
                        game.reset()
                        game.start_game()
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
