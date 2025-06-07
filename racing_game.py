import pygame
import sys
import math
import random
import os
import numpy

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize sound mixer

# Create a directory for sound files if it doesn't exist
sound_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds")
os.makedirs(sound_dir, exist_ok=True)

def play_sound(sound, volume=1.0):
    """Play a sound if sound is enabled"""
    if sound_enabled:
        sound.set_volume(volume)
        sound.play()

def update_engine_sound():
    """Update engine sound based on car speed"""
    if sound_enabled:
        # Adjust volume based on speed
        volume = min(1.0, abs(car_speed) / car_max_speed)
        engine_sound.set_volume(volume)
        
        # Play engine sound if not already playing
        if not pygame.mixer.get_busy():
            engine_sound.play(-1)  # Loop indefinitely

def draw_background():
    """Draw a dynamic background based on the selected background mode"""
    if background_mode == 0:  # Day
        # Sky gradient
        for y in range(SCREEN_HEIGHT):
            # Create gradient from light blue to darker blue
            color_value = max(100, 235 - int(y * 0.3))
            sky_color = (135, color_value, 235)
            pygame.draw.line(screen, sky_color, (0, y), (SCREEN_WIDTH, y))
        
        # Draw distant mountains
        mountain_height = 150
        for x in range(0, SCREEN_WIDTH, 100):
            offset = random.randint(-30, 30)
            points = [
                (x, SCREEN_HEIGHT//2 - mountain_height + offset),
                (x + 50, SCREEN_HEIGHT//2 - mountain_height - 30 + offset),
                (x + 100, SCREEN_HEIGHT//2 - mountain_height + offset)
            ]
            pygame.draw.polygon(screen, MOUNTAIN_BROWN, points)
        
        # Draw grass on sides of road
        pygame.draw.rect(screen, GRASS_GREEN, (0, SCREEN_HEIGHT, road_x, SCREEN_HEIGHT))
        pygame.draw.rect(screen, GRASS_GREEN, (road_x + road_width, SCREEN_HEIGHT, SCREEN_WIDTH - road_x - road_width, SCREEN_HEIGHT))
        
    elif background_mode == 1:  # Sunset
        # Sky gradient from orange to dark blue
        for y in range(SCREEN_HEIGHT):
            # Create sunset gradient
            if y < SCREEN_HEIGHT // 3:
                # Top third: orange to yellow
                r = 255
                g = min(255, 99 + int(y * 0.8))
                b = 71
            else:
                # Bottom two-thirds: yellow to dark blue
                r = max(25, 255 - int((y - SCREEN_HEIGHT // 3) * 0.8))
                g = max(25, 180 - int((y - SCREEN_HEIGHT // 3) * 0.6))
                b = min(112, 71 + int((y - SCREEN_HEIGHT // 3) * 0.2))
            
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Draw sun
        pygame.draw.circle(screen, YELLOW, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4), 50)
        
        # Draw distant mountains (silhouettes)
        mountain_height = 150
        for x in range(0, SCREEN_WIDTH, 100):
            offset = random.randint(-30, 30)
            points = [
                (x, SCREEN_HEIGHT//2 - mountain_height + offset),
                (x + 50, SCREEN_HEIGHT//2 - mountain_height - 30 + offset),
                (x + 100, SCREEN_HEIGHT//2 - mountain_height + offset)
            ]
            pygame.draw.polygon(screen, (50, 50, 50), points)
        
        # Draw darker grass on sides of road
        pygame.draw.rect(screen, (20, 80, 20), (0, SCREEN_HEIGHT, road_x, SCREEN_HEIGHT))
        pygame.draw.rect(screen, (20, 80, 20), (road_x + road_width, SCREEN_HEIGHT, SCREEN_WIDTH - road_x - road_width, SCREEN_HEIGHT))
        
    else:  # Night
        # Dark sky with stars
        screen.fill(NIGHT_BLUE)
        
        # Draw stars
        for _ in range(100):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT // 2)
            size = random.randint(1, 3)
            brightness = random.randint(150, 255)
            pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), size)
        
        # Draw moon
        pygame.draw.circle(screen, WHITE, (SCREEN_WIDTH - 100, 100), 40)
        pygame.draw.circle(screen, NIGHT_BLUE, (SCREEN_WIDTH - 85, 90), 40)
        
        # Draw distant mountains (dark silhouettes)
        mountain_height = 150
        for x in range(0, SCREEN_WIDTH, 100):
            offset = random.randint(-30, 30)
            points = [
                (x, SCREEN_HEIGHT//2 - mountain_height + offset),
                (x + 50, SCREEN_HEIGHT//2 - mountain_height - 30 + offset),
                (x + 100, SCREEN_HEIGHT//2 - mountain_height + offset)
            ]
            pygame.draw.polygon(screen, (20, 20, 40), points)
        
        # Draw very dark grass on sides of road
        pygame.draw.rect(screen, (10, 30, 10), (0, SCREEN_HEIGHT, road_x, SCREEN_HEIGHT))
        pygame.draw.rect(screen, (10, 30, 10), (road_x + road_width, SCREEN_HEIGHT, SCREEN_WIDTH - road_x - road_width, SCREEN_HEIGHT))

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Racing Game")

# Get actual screen dimensions for fullscreen backgrounds
info = pygame.display.Info()
FULL_SCREEN_WIDTH = info.current_w
FULL_SCREEN_HEIGHT = info.current_h

# Try to load sounds
try:
    engine_sound = pygame.mixer.Sound(os.path.join(sound_dir, "engine.wav"))
    crash_sound = pygame.mixer.Sound(os.path.join(sound_dir, "crash.wav"))
    gear_shift_sound = pygame.mixer.Sound(os.path.join(sound_dir, "gear_shift.wav"))
    menu_select_sound = pygame.mixer.Sound(os.path.join(sound_dir, "menu_select.wav"))
except Exception as e:
    print(f"Error loading sounds: {e}")
    # Create simple sounds using pygame
    try:
        # Create simple beep sounds
        sample_rate = 44100
        duration = 0.5  # seconds
        
        # Engine sound (low hum)
        buffer = numpy.sin(2 * numpy.pi * numpy.arange(sample_rate * duration) * 100 / sample_rate).astype(numpy.float32)
        engine_sound = pygame.mixer.Sound(buffer)
        
        # Crash sound (noise)
        buffer = numpy.random.rand(int(sample_rate * duration)).astype(numpy.float32)
        crash_sound = pygame.mixer.Sound(buffer)
        
        # Gear shift sound (short beep)
        buffer = numpy.sin(2 * numpy.pi * numpy.arange(sample_rate * 0.1) * 440 / sample_rate).astype(numpy.float32)
        gear_shift_sound = pygame.mixer.Sound(buffer)
        
        # Menu select sound (higher beep)
        buffer = numpy.sin(2 * numpy.pi * numpy.arange(sample_rate * 0.1) * 880 / sample_rate).astype(numpy.float32)
        menu_select_sound = pygame.mixer.Sound(buffer)
    except:
        # If sound creation fails, create dummy sound objects
        class DummySound:
            def play(self, loops=0): pass
            def stop(self): pass
            def set_volume(self, vol): pass
        
        engine_sound = DummySound()
        crash_sound = DummySound()
        gear_shift_sound = DummySound()
        menu_select_sound = DummySound()

# Set up icon
try:
    icon = pygame.Surface((32, 32))
    icon.fill((255, 0, 0))
    pygame.draw.rect(icon, (0, 0, 255), (5, 5, 22, 22))
    pygame.display.set_icon(icon)
except:
    pass

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
SKY_BLUE = (135, 206, 235)
GRASS_GREEN = (34, 139, 34)
MOUNTAIN_BROWN = (139, 69, 19)
SUNSET_ORANGE = (255, 99, 71)
NIGHT_BLUE = (25, 25, 112)

# Game states
MENU = 0
CAR_SELECT = 1
COLOR_SELECT = 2
SETTINGS = 3
GAME = 4
GAME_OVER = 5

# Current game state
game_state = MENU

# Font
font_large = pygame.font.SysFont(None, 60)
font_medium = pygame.font.SysFont(None, 40)
font_small = pygame.font.SysFont(None, 30)

# Car options
car_types = [
    {"name": "Sedan", "width": 40, "height": 70, "acceleration": 0.1, "max_speed": 20, "handling": 3},
    {"name": "Sports", "width": 40, "height": 65, "acceleration": 0.15, "max_speed": 25, "handling": 4},
    {"name": "SUV", "width": 45, "height": 80, "acceleration": 0.08, "max_speed": 18, "handling": 2}
]
selected_car_index = 0

# Car colors
car_colors = [RED, BLUE, GREEN, YELLOW, ORANGE, PURPLE]
selected_color_index = 0

# Game settings
fullscreen = False
sound_enabled = True
difficulty = 1  # 1=easy, 2=medium, 3=hard
background_mode = 0  # 0=day, 1=sunset, 2=night

# Game variables
score = 0
high_score = 0
game_time = 0

# Car properties
car_width = car_types[selected_car_index]["width"]
car_height = car_types[selected_car_index]["height"]
car_x = SCREEN_WIDTH // 2 - car_width // 2
# Position the car vertically between center and bottom (about 3/4 down the screen)
car_y = SCREEN_HEIGHT * 3 // 4 - car_height // 2
car_speed = 0
car_acceleration = car_types[selected_car_index]["acceleration"]
car_max_speed = car_types[selected_car_index]["max_speed"]
car_rotation = 0
car_rotation_speed = car_types[selected_car_index]["handling"]
car_friction = 0.05
car_color = car_colors[selected_color_index]

# Gear system
current_gear = 1
max_gear = 5
gear_speeds = {
    1: 5,
    2: 8,
    3: 12,
    4: 16,
    5: 20
}

# Road properties
road_width = 400
road_x = (SCREEN_WIDTH - road_width) // 2
road_line_width = 10
road_line_height = 50
road_line_gap = 30
road_lines = []
for i in range(-1, SCREEN_HEIGHT // (road_line_height + road_line_gap) + 2):
    road_lines.append(i * (road_line_height + road_line_gap))

# Traffic cars
traffic_cars = []
traffic_spawn_timer = 0
traffic_spawn_delay = 120  # frames between spawns

# Trees
trees = []
tree_spawn_timer = 0

# Game loop
clock = pygame.time.Clock()
running = True

# Button class for menus
class Button:
    def __init__(self, x, y, width, height, text, color=LIGHT_GRAY, hover_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 3, border_radius=10)
        
        text_surface = font_medium.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
        
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

# Create menu buttons
play_button = Button(SCREEN_WIDTH//2 - 100, 200, 200, 50, "Play Game")
car_select_button = Button(SCREEN_WIDTH//2 - 100, 270, 200, 50, "Select Car")
settings_button = Button(SCREEN_WIDTH//2 - 100, 340, 200, 50, "Settings")
quit_button = Button(SCREEN_WIDTH//2 - 100, 410, 200, 50, "Quit")

# Back button for sub-menus
back_button = Button(50, SCREEN_HEIGHT - 70, 100, 40, "Back")

# Settings buttons
fullscreen_button = Button(SCREEN_WIDTH//2 - 150, 150, 300, 50, "Fullscreen: Off")
sound_button = Button(SCREEN_WIDTH//2 - 150, 220, 300, 50, "Sound: On")
difficulty_button = Button(SCREEN_WIDTH//2 - 150, 290, 300, 50, "Difficulty: Easy")
background_button = Button(SCREEN_WIDTH//2 - 150, 360, 300, 50, "Background: Day")

# Car selection buttons
prev_car_button = Button(SCREEN_WIDTH//4 - 50, SCREEN_HEIGHT//2, 100, 40, "Previous")
next_car_button = Button(3*SCREEN_WIDTH//4 - 50, SCREEN_HEIGHT//2, 100, 40, "Next")
select_car_button = Button(SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT - 100, 120, 40, "Select")

# Color selection buttons
prev_color_button = Button(SCREEN_WIDTH//4 - 50, SCREEN_HEIGHT//2, 100, 40, "Previous")
next_color_button = Button(3*SCREEN_WIDTH//4 - 50, SCREEN_HEIGHT//2, 100, 40, "Next")
select_color_button = Button(SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT - 100, 120, 40, "Select")

# Game over buttons
play_again_button = Button(SCREEN_WIDTH//2 - 100, 300, 200, 50, "Play Again")
menu_button = Button(SCREEN_WIDTH//2 - 100, 370, 200, 50, "Main Menu")

def draw_car(x, y, rotation, car_type, color):
    # Create a surface for the car
    car_surface = pygame.Surface((car_type["width"], car_type["height"]), pygame.SRCALPHA)
    
    # Draw car body
    pygame.draw.rect(car_surface, color, (0, 0, car_type["width"], car_type["height"]), border_radius=5)
    
    # Draw windows
    pygame.draw.rect(car_surface, BLUE, (5, 10, car_type["width"] - 10, 15))
    pygame.draw.rect(car_surface, BLUE, (5, car_type["height"] - 30, car_type["width"] - 10, 15))
    
    # Draw wheels
    pygame.draw.rect(car_surface, BLACK, (-5, 10, 10, 20), border_radius=5)
    pygame.draw.rect(car_surface, BLACK, (car_type["width"] - 5, 10, 10, 20), border_radius=5)
    pygame.draw.rect(car_surface, BLACK, (-5, car_type["height"] - 30, 10, 20), border_radius=5)
    pygame.draw.rect(car_surface, BLACK, (car_type["width"] - 5, car_type["height"] - 30, 10, 20), border_radius=5)
    
    # Add headlights
    pygame.draw.circle(car_surface, YELLOW, (5, 5), 3)
    pygame.draw.circle(car_surface, YELLOW, (car_type["width"] - 5, 5), 3)
    
    # Add taillights
    pygame.draw.circle(car_surface, RED, (5, car_type["height"] - 5), 3)
    pygame.draw.circle(car_surface, RED, (car_type["width"] - 5, car_type["height"] - 5), 3)
    
    # Rotate the car
    rotated_car = pygame.transform.rotate(car_surface, rotation)
    new_rect = rotated_car.get_rect(center=(x + car_type["width"] // 2, y + car_type["height"] // 2))
    
    # Draw the rotated car
    screen.blit(rotated_car, new_rect.topleft)
    
    return new_rect  # Return the rectangle for collision detection

def draw_traffic_car(car):
    # Draw a traffic car
    car_surface = pygame.Surface((car["width"], car["height"]), pygame.SRCALPHA)
    pygame.draw.rect(car_surface, car["color"], (0, 0, car["width"], car["height"]), border_radius=5)
    pygame.draw.rect(car_surface, BLUE, (5, 10, car["width"] - 10, 15))
    pygame.draw.rect(car_surface, BLUE, (5, car["height"] - 30, car["width"] - 10, 15))
    pygame.draw.rect(car_surface, BLACK, (-5, 10, 10, 20), border_radius=5)
    pygame.draw.rect(car_surface, BLACK, (car["width"] - 5, 10, 10, 20), border_radius=5)
    pygame.draw.rect(car_surface, BLACK, (-5, car["height"] - 30, 10, 20), border_radius=5)
    pygame.draw.rect(car_surface, BLACK, (car["width"] - 5, car["height"] - 30, 10, 20), border_radius=5)
    
    # Add headlights and taillights
    if car["direction"] == "down":
        # Taillights (red) at the top
        pygame.draw.circle(car_surface, RED, (5, 5), 3)
        pygame.draw.circle(car_surface, RED, (car["width"] - 5, 5), 3)
        # Headlights (yellow) at the bottom
        pygame.draw.circle(car_surface, YELLOW, (5, car["height"] - 5), 3)
        pygame.draw.circle(car_surface, YELLOW, (car["width"] - 5, car["height"] - 5), 3)
    else:
        # Headlights (yellow) at the top
        pygame.draw.circle(car_surface, YELLOW, (5, 5), 3)
        pygame.draw.circle(car_surface, YELLOW, (car["width"] - 5, 5), 3)
        # Taillights (red) at the bottom
        pygame.draw.circle(car_surface, RED, (5, car["height"] - 5), 3)
        pygame.draw.circle(car_surface, RED, (car["width"] - 5, car["height"] - 5), 3)
    
    screen.blit(car_surface, (car["x"], car["y"]))
    
    return pygame.Rect(car["x"], car["y"], car["width"], car["height"])

def draw_tree(tree):
    # Draw a tree
    trunk_width = 10
    trunk_height = 30
    trunk_x = tree["x"]
    trunk_y = tree["y"]
    
    # Adjust tree appearance based on background mode
    if background_mode == 0:  # Day
        # Draw trunk
        pygame.draw.rect(screen, (139, 69, 19), (trunk_x, trunk_y, trunk_width, trunk_height))
        # Draw foliage
        pygame.draw.circle(screen, (0, 100, 0), (trunk_x + trunk_width//2, trunk_y - 15), 25)
    elif background_mode == 1:  # Sunset
        # Draw trunk
        pygame.draw.rect(screen, (100, 50, 10), (trunk_x, trunk_y, trunk_width, trunk_height))
        # Draw foliage with sunset lighting
        pygame.draw.circle(screen, (0, 80, 0), (trunk_x + trunk_width//2, trunk_y - 15), 25)
        pygame.draw.circle(screen, (255, 165, 0), (trunk_x + trunk_width//2, trunk_y - 25), 10, 2)
    else:  # Night
        # Draw trunk
        pygame.draw.rect(screen, (60, 30, 10), (trunk_x, trunk_y, trunk_width, trunk_height))
        # Draw foliage
        pygame.draw.circle(screen, (0, 40, 0), (trunk_x + trunk_width//2, trunk_y - 15), 25)

def draw_road():
    # Draw road
    pygame.draw.rect(screen, DARK_GRAY, (road_x, 0, road_width, SCREEN_HEIGHT))

    # Draw only center line
    for y in road_lines:
        # Adjust line color based on background mode
        line_color = WHITE
        if background_mode == 2:  # Night mode - make lines glow
            line_color = (255, 255, 200)  # Slightly yellow to simulate reflection

        # Draw center line only
        pygame.draw.rect(screen, line_color, (SCREEN_WIDTH // 2 - road_line_width // 2, y, road_line_width, road_line_height))

    # Add road edges
    edge_width = 5
    pygame.draw.rect(screen, YELLOW, (road_x, 0, edge_width, SCREEN_HEIGHT))
    pygame.draw.rect(screen, YELLOW, (road_x + road_width - edge_width, 0, edge_width, SCREEN_HEIGHT))

def draw_hud():
    # Draw speed
    speed_text = f"Speed: {abs(int(car_speed * 10))} km/h"
    speed_surface = font_small.render(speed_text, True, WHITE)
    screen.blit(speed_surface, (20, 20))
    
    # Draw gear
    gear_text = f"Gear: {current_gear}"
    gear_surface = font_small.render(gear_text, True, WHITE)
    screen.blit(gear_surface, (20, 50))
    
    # Draw score
    score_text = f"Score: {score}"
    score_surface = font_small.render(score_text, True, WHITE)
    screen.blit(score_surface, (SCREEN_WIDTH - 150, 20))
    
    # Draw high score
    high_score_text = f"High Score: {high_score}"
    high_score_surface = font_small.render(high_score_text, True, WHITE)
    screen.blit(high_score_surface, (SCREEN_WIDTH - 200, 50))
    
    # Draw car type
    car_type_text = f"Car: {car_types[selected_car_index]['name']}"
    car_type_surface = font_small.render(car_type_text, True, WHITE)
    screen.blit(car_type_surface, (20, 80))
    
    # Draw difficulty
    difficulty_names = ["Easy", "Medium", "Hard"]
    difficulty_text = f"Difficulty: {difficulty_names[difficulty-1]}"
    difficulty_surface = font_small.render(difficulty_text, True, WHITE)
    screen.blit(difficulty_surface, (SCREEN_WIDTH - 200, 80))
    
    # Draw background mode
    background_names = ["Day", "Sunset", "Night"]
    bg_text = f"Background: {background_names[background_mode]} (Press B to change)"
    bg_surface = font_small.render(bg_text, True, WHITE)
    screen.blit(bg_surface, (SCREEN_WIDTH // 2 - bg_surface.get_width() // 2, 20))

def draw_menu():
    # Draw title
    title_text = font_large.render("CAR RACING GAME", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))
    
    # Draw buttons
    play_button.draw()
    car_select_button.draw()
    settings_button.draw()
    quit_button.draw()

def draw_car_selection():
    # Draw title
    title_text = font_large.render("SELECT YOUR CAR", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
    
    # Draw car preview
    car_type = car_types[selected_car_index]
    draw_car(SCREEN_WIDTH//2 - car_type["width"]//2, SCREEN_HEIGHT//2 - car_type["height"]//2, 
             0, car_type, car_colors[selected_color_index])
    
    # Draw car info
    info_text = [
        f"Car: {car_type['name']}",
        f"Acceleration: {car_type['acceleration']}",
        f"Max Speed: {car_type['max_speed']}",
        f"Handling: {car_type['handling']}"
    ]
    
    y_pos = SCREEN_HEIGHT//2 + 100
    for text in info_text:
        text_surface = font_small.render(text, True, WHITE)
        screen.blit(text_surface, (SCREEN_WIDTH//2 - text_surface.get_width()//2, y_pos))
        y_pos += 30
    
    # Draw buttons
    prev_car_button.draw()
    next_car_button.draw()
    select_car_button.draw()
    back_button.draw()

def draw_color_selection():
    # Draw title
    title_text = font_large.render("SELECT CAR COLOR", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
    
    # Draw car preview with selected color
    car_type = car_types[selected_car_index]
    draw_car(SCREEN_WIDTH//2 - car_type["width"]//2, SCREEN_HEIGHT//2 - car_type["height"]//2, 
             0, car_type, car_colors[selected_color_index])
    
    # Draw color name
    color_names = ["Red", "Blue", "Green", "Yellow", "Orange", "Purple"]
    color_text = font_medium.render(color_names[selected_color_index], True, WHITE)
    screen.blit(color_text, (SCREEN_WIDTH//2 - color_text.get_width()//2, SCREEN_HEIGHT//2 + 100))
    
    # Draw buttons
    prev_color_button.draw()
    next_color_button.draw()
    select_color_button.draw()
    back_button.draw()

def draw_settings():
    # Draw title
    title_text = font_large.render("SETTINGS", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 80))
    
    # Update button texts based on settings
    fullscreen_button.text = f"Fullscreen: {'On' if fullscreen else 'Off'}"
    sound_button.text = f"Sound: {'On' if sound_enabled else 'Off'}"
    
    difficulty_names = ["Easy", "Medium", "Hard"]
    difficulty_button.text = f"Difficulty: {difficulty_names[difficulty-1]}"
    
    background_names = ["Day", "Sunset", "Night"]
    background_button.text = f"Background: {background_names[background_mode]}"
    
    # Draw buttons
    fullscreen_button.draw()
    sound_button.draw()
    difficulty_button.draw()
    background_button.draw()
    back_button.draw()

def draw_game_over():
    # Draw game over text
    game_over_text = font_large.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 100))
    
    # Draw score
    score_text = font_medium.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 180))
    
    # Draw high score
    if score > high_score:
        new_high_score_text = font_medium.render("NEW HIGH SCORE!", True, YELLOW)
        screen.blit(new_high_score_text, (SCREEN_WIDTH//2 - new_high_score_text.get_width()//2, 220))
    else:
        high_score_text = font_medium.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(high_score_text, (SCREEN_WIDTH//2 - high_score_text.get_width()//2, 220))
    
    # Draw buttons
    play_again_button.draw()
    menu_button.draw()

def spawn_traffic():
    # Spawn a traffic car
    lane_width = road_width / 2  # Divide road into 2 lanes

    # Determine direction and lane based on direction (50/50 chance)
    direction = "down" if random.random() < 0.5 else "up"

    # Cars going down use left lane, cars going up use right lane
    lane = 0 if direction == "down" else 1
    lane_x = road_x + lane * lane_width + lane_width/2 - 20

    traffic_colors = [RED, BLUE, GREEN, YELLOW, PURPLE]
    car_color = random.choice(traffic_colors)

    # Set starting position based on direction
    y_pos = -100 if direction == "down" else SCREEN_HEIGHT + 100

    traffic_car = {
        "x": lane_x,
        "y": y_pos,
        "width": 40,
        "height": 70,
        "speed": random.uniform(1, 3) * (1 if direction == "down" else -1),
        "color": car_color,
        "direction": direction
    }

    traffic_cars.append(traffic_car)

def spawn_tree():
    # Spawn trees on either side of the road
    side = random.choice(["left", "right"])
    if side == "left":
        x = random.randint(50, road_x - 50)
    else:
        x = random.randint(road_x + road_width + 20, SCREEN_WIDTH - 50)
    
    tree = {
        "x": x,
        "y": -50,
        "speed": 2
    }
    
    trees.append(tree)

def reset_game():
    global car_x, car_y, car_speed, car_rotation, current_gear
    global traffic_cars, trees, score, game_time
    
    car_x = SCREEN_WIDTH // 2 - car_width // 2
    car_y = SCREEN_HEIGHT * 3 // 4 - car_height // 2  # Position car between center and bottom
    car_speed = 0
    car_rotation = 0
    current_gear = 1
    traffic_cars = []
    trees = []
    score = 0
    game_time = 0
    
    # Stop any playing sounds
    engine_sound.stop()

# Main game loop
while running:
    # Handle events
    mouse_click = False
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == GAME:
                if event.key == pygame.K_q:  # Shift up
                    if current_gear < max_gear:
                        current_gear += 1
                        play_sound(gear_shift_sound)
                elif event.key == pygame.K_z:  # Shift down
                    if current_gear > 1:
                        current_gear -= 1
                        play_sound(gear_shift_sound)
                elif event.key == pygame.K_b:  # Change background during gameplay
                    background_mode = (background_mode + 1) % 3
                    play_sound(menu_select_sound)
                elif event.key == pygame.K_ESCAPE:  # Return to menu
                    game_state = MENU
                    engine_sound.stop()
            elif event.key == pygame.K_F11:  # Toggle fullscreen
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = True
    
    # Fill background
    screen.fill(BLACK)
    
    # Handle different game states
    if game_state == MENU:
        draw_menu()
        
        # Check button interactions
        play_button.check_hover(mouse_pos)
        car_select_button.check_hover(mouse_pos)
        settings_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)
        
        if play_button.is_clicked(mouse_pos, mouse_click):
            game_state = COLOR_SELECT
            play_sound(menu_select_sound)
        elif car_select_button.is_clicked(mouse_pos, mouse_click):
            game_state = CAR_SELECT
            play_sound(menu_select_sound)
        elif settings_button.is_clicked(mouse_pos, mouse_click):
            game_state = SETTINGS
            play_sound(menu_select_sound)
        elif quit_button.is_clicked(mouse_pos, mouse_click):
            running = False
    
    elif game_state == CAR_SELECT:
        draw_car_selection()
        
        # Check button interactions
        prev_car_button.check_hover(mouse_pos)
        next_car_button.check_hover(mouse_pos)
        select_car_button.check_hover(mouse_pos)
        back_button.check_hover(mouse_pos)
        
        if prev_car_button.is_clicked(mouse_pos, mouse_click):
            selected_car_index = (selected_car_index - 1) % len(car_types)
        elif next_car_button.is_clicked(mouse_pos, mouse_click):
            selected_car_index = (selected_car_index + 1) % len(car_types)
        elif select_car_button.is_clicked(mouse_pos, mouse_click):
            # Update car properties based on selection
            car_width = car_types[selected_car_index]["width"]
            car_height = car_types[selected_car_index]["height"]
            car_acceleration = car_types[selected_car_index]["acceleration"]
            car_max_speed = car_types[selected_car_index]["max_speed"]
            car_rotation_speed = car_types[selected_car_index]["handling"]
            game_state = COLOR_SELECT
        elif back_button.is_clicked(mouse_pos, mouse_click):
            game_state = MENU
    
    elif game_state == COLOR_SELECT:
        draw_color_selection()
        
        # Check button interactions
        prev_color_button.check_hover(mouse_pos)
        next_color_button.check_hover(mouse_pos)
        select_color_button.check_hover(mouse_pos)
        back_button.check_hover(mouse_pos)
        
        if prev_color_button.is_clicked(mouse_pos, mouse_click):
            selected_color_index = (selected_color_index - 1) % len(car_colors)
        elif next_color_button.is_clicked(mouse_pos, mouse_click):
            selected_color_index = (selected_color_index + 1) % len(car_colors)
        elif select_color_button.is_clicked(mouse_pos, mouse_click):
            car_color = car_colors[selected_color_index]
            reset_game()
            game_state = GAME
        elif back_button.is_clicked(mouse_pos, mouse_click):
            game_state = CAR_SELECT
    
    elif game_state == SETTINGS:
        draw_settings()
        
        # Check button interactions
        fullscreen_button.check_hover(mouse_pos)
        sound_button.check_hover(mouse_pos)
        difficulty_button.check_hover(mouse_pos)
        back_button.check_hover(mouse_pos)
        
        if fullscreen_button.is_clicked(mouse_pos, mouse_click):
            fullscreen = not fullscreen
            if fullscreen:
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
            else:
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        elif sound_button.is_clicked(mouse_pos, mouse_click):
            sound_enabled = not sound_enabled
        elif difficulty_button.is_clicked(mouse_pos, mouse_click):
            difficulty = (difficulty % 3) + 1
        elif background_button.is_clicked(mouse_pos, mouse_click):
            background_mode = (background_mode + 1) % 3
        elif back_button.is_clicked(mouse_pos, mouse_click):
            game_state = MENU
    
    elif game_state == GAME:
        # Get pressed keys
        keys = pygame.key.get_pressed()
        
        # Handle car controls
        if keys[pygame.K_UP]:
            car_speed += car_acceleration
        elif keys[pygame.K_DOWN]:
            car_speed -= car_acceleration
        else:
            # Apply friction to slow down
            if car_speed > 0:
                car_speed -= car_friction
            elif car_speed < 0:
                car_speed += car_friction
            
            # Stop completely if speed is very low
            if abs(car_speed) < car_friction:
                car_speed = 0
        
        # Apply gear limits
        max_speed_in_gear = min(gear_speeds[current_gear], car_max_speed)
        if abs(car_speed) > max_speed_in_gear:
            if car_speed > 0:
                car_speed = max_speed_in_gear
            else:
                car_speed = -max_speed_in_gear
        
        # Handle steering
        if car_speed != 0:  # Only allow steering when moving
            if keys[pygame.K_LEFT]:
                car_rotation += car_rotation_speed
            if keys[pygame.K_RIGHT]:
                car_rotation -= car_rotation_speed
        
        # Update engine sound
        update_engine_sound()
        
        # Calculate movement based on rotation and speed
        angle_rad = math.radians(car_rotation)
        car_x += -math.sin(angle_rad) * car_speed
        
        # Instead of moving the car vertically, move the road and obstacles
        # Keep the car at a fixed vertical position
        fixed_car_y = SCREEN_HEIGHT * 3 // 4 - car_height // 2
        
        # Calculate how much the car would have moved vertically
        # Reverse the sign to fix the direction (positive car_speed should move road downward)
        vertical_movement = math.cos(angle_rad) * car_speed
        
        # Apply the vertical movement to road lines, traffic, and trees instead of the car
        for i in range(len(road_lines)):
            road_lines[i] += vertical_movement
            if road_lines[i] > SCREEN_HEIGHT:
                road_lines[i] = -road_line_height
            elif road_lines[i] < -road_line_height:
                road_lines[i] = SCREEN_HEIGHT
        
        # Keep car within road boundaries (but allow full road access)
        car_x = max(road_x, min(car_x, road_x + road_width - car_width))
        car_y = fixed_car_y  # Keep car at fixed vertical position
        
        # Spawn traffic cars
        traffic_spawn_timer += 1
        if traffic_spawn_timer >= traffic_spawn_delay:
            spawn_traffic()
            traffic_spawn_timer = 0
            # Adjust spawn rate based on difficulty
            traffic_spawn_delay = 120 // difficulty
        
        # Spawn trees
        tree_spawn_timer += 1
        if tree_spawn_timer >= 60:  # Spawn trees every 60 frames
            spawn_tree()
            tree_spawn_timer = 0
        
        # Update traffic cars
        for car in traffic_cars[:]:
            car["y"] += car["speed"] + vertical_movement
            # Remove cars that are off screen
            if car["direction"] == "down" and car["y"] > SCREEN_HEIGHT:
                traffic_cars.remove(car)
                score += 10  # Score for passing a car
            elif car["direction"] == "up" and car["y"] < -car["height"]:
                traffic_cars.remove(car)
                score += 10  # Score for passing a car
        
        # Update trees
        for tree in trees[:]:
            tree["y"] += vertical_movement
            if tree["y"] > SCREEN_HEIGHT:
                trees.remove(tree)
        
        # Draw everything
        draw_background()  # Draw the dynamic background
        
        # Draw trees behind the road
        for tree in trees:
            draw_tree(tree)
        
        draw_road()
        
        # Draw traffic cars
        traffic_rects = []
        for car in traffic_cars:
            traffic_rect = draw_traffic_car(car)
            traffic_rects.append(traffic_rect)
        
        # Draw player car
        player_car_rect = draw_car(car_x, car_y, car_rotation, 
                                  car_types[selected_car_index], car_color)
        
        # Check for collisions
        for rect in traffic_rects:
            if player_car_rect.colliderect(rect):
                play_sound(crash_sound)
                if score > high_score:
                    high_score = score
                game_state = GAME_OVER
                engine_sound.stop()
        
        # Draw HUD
        draw_hud()
        
        # Increase score based on speed
        if car_speed > 0:
            score += int(car_speed / 10)
        
        # Increase game time
        game_time += 1
    
    elif game_state == GAME_OVER:
        draw_game_over()
        
        # Check button interactions
        play_again_button.check_hover(mouse_pos)
        menu_button.check_hover(mouse_pos)
        
        if play_again_button.is_clicked(mouse_pos, mouse_click):
            reset_game()
            game_state = GAME
        elif menu_button.is_clicked(mouse_pos, mouse_click):
            game_state = MENU
    
    # Update display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()

def play_sound(sound, volume=1.0):
    """Play a sound if sound is enabled"""
    if sound_enabled:
        sound.set_volume(volume)
        sound.play()

def update_engine_sound():
    """Update engine sound based on car speed"""
    if sound_enabled:
        # Adjust volume based on speed
        volume = min(1.0, abs(car_speed) / car_max_speed)
        engine_sound.set_volume(volume)
        
        # Play engine sound if not already playing
        if not pygame.mixer.get_busy():
            engine_sound.play(-1)  # Loop indefinitely
