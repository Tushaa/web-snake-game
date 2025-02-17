import os
import pygame
import sys
from game.snake import Snake
from game.food import Food
from game.obstacle import Obstacle

# Set the working directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize the game
pygame.init()

# Set up display
width, height = 600, 400
border_thickness = 10
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Eat Game')

# Set up game variables
snake = Snake()
food = Food(width - 2 * border_thickness, height - 2 * border_thickness)  # Pass adjusted width and height to Food constructor
obstacles = [Obstacle(width - 2 * border_thickness, height - 2 * border_thickness, color=(255, 255, 0)) for _ in range(5)]  # Add 5 obstacles with yellow color
clock = pygame.time.Clock()
score = 0
font = pygame.font.Font(None, 35)  # Use the default font

def draw_score(surface, score):
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    surface.blit(score_text, (10, 10))

def game_over(surface, score):
    game_over_text = font.render(f'Game Over! Final Score: {score}', True, (255, 0, 0))
    surface.blit(game_over_text, (width // 4, height // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

def draw_border(surface):
    border_color = (211, 211, 211)  # Light grey color
    pygame.draw.rect(surface, border_color, pygame.Rect(0, 0, width, border_thickness))  # Top border
    pygame.draw.rect(surface, border_color, pygame.Rect(0, 0, border_thickness, height))  # Left border
    pygame.draw.rect(surface, border_color, pygame.Rect(0, height - border_thickness, width, border_thickness))  # Bottom border
    pygame.draw.rect(surface, border_color, pygame.Rect(width - border_thickness, 0, border_thickness, height))  # Right border

def draw_start_screen(surface):
    surface.fill((0, 0, 0))
    start_text = font.render('Press any key to start', True, (255, 255, 255))
    surface.blit(start_text, (width // 4, height // 2))
    pygame.display.flip()

def draw_end_screen(surface, score):
    surface.fill((0, 0, 0))
    game_over_text = font.render(f'Game Over! Final Score: {score}', True, (255, 0, 0))
    play_again_text = font.render('Press any key to play again', True, (255, 255, 255))
    surface.blit(game_over_text, (width // 4, height // 2 - 20))
    surface.blit(play_again_text, (width // 4, height // 2 + 20))
    pygame.display.flip()

def game_loop():
    global score
    running = True
    game_state = 'start'
    speed = 10

    while running:
        if game_state == 'start':
            draw_start_screen(window)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    game_state = 'playing'
                    snake.__init__()  # Reset snake
                    food.position = food.spawn()  # Reset food
                    score = 0  # Reset score
                    speed = 10  # Reset speed
                    for obstacle in obstacles:
                        obstacle.position = obstacle.spawn()  # Reset obstacles

        elif game_state == 'playing':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                snake.handle_input(event)

            snake.move(width - 2 * border_thickness, height - 2 * border_thickness)
            
            if snake.get_position() == food.get_position():
                snake.grow()
                food.position = food.spawn()
                score += 1  # Increase score
                speed += 1  # Increase speed

            # Check for collision with itself
            if snake.get_position() in snake.body[1:]:
                game_state = 'end'

            # Check for collision with obstacles
            for obstacle in obstacles:
                if snake.get_position() == obstacle.position:
                    game_state = 'end'

            window.fill((0, 0, 0))  # Clear the screen
            draw_border(window)  # Draw the border
            snake.draw(window)
            food.draw(window)
            for obstacle in obstacles:
                obstacle.draw(window)
            draw_score(window, score)  # Draw the score
            
            pygame.display.flip()
            clock.tick(speed)  # Control the game speed

        elif game_state == 'end':
            game_over(window, score)
            draw_end_screen(window, score)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    game_state = 'start'

if __name__ == "__main__":
    game_loop()