import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Paddle dimensions and speed
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 5

# Ball dimensions and speed
BALL_SIZE = 10
BALL_SPEED_X, BALL_SPEED_Y = 4, 4

# Font
font = pygame.font.Font(None, 36)

# Create game objects
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
    
    def move(self, dy):
        self.rect.y += dy
        self.rect.clamp_ip(screen.get_rect())

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.dx, self.dy = BALL_SPEED_X, BALL_SPEED_Y
    
    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

# Initialize game objects
player_paddle = Paddle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2)
opponent_paddle = Paddle(WIDTH - 60, HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball()

# Score
player_score = 0
opponent_score = 0

# Game states
MENU, PLAYING, GAME_OVER = 0, 1, 2
state = MENU

# Game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if state == MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state = PLAYING
                    player_score = opponent_score = 0
                    ball.rect.center = (WIDTH // 2, HEIGHT // 2)
                    ball.dx = random.choice([-1, 1]) * BALL_SPEED_X
                    ball.dy = random.choice([-1, 1]) * BALL_SPEED_Y

    if state == MENU:
        screen.fill(BLACK)
        title = font.render("Pong", True, WHITE)
        start = font.render("Press SPACE to start", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(start, (WIDTH // 2 - start.get_width() // 2, HEIGHT // 2 + 50))
    elif state == PLAYING:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_paddle.move(-PADDLE_SPEED)
        if keys[pygame.K_DOWN]:
            player_paddle.move(PADDLE_SPEED)

        # Opponent movement (simple AI)
        if opponent_paddle.rect.centery < ball.rect.centery:
            opponent_paddle.move(PADDLE_SPEED)
        elif opponent_paddle.rect.centery > ball.rect.centery:
            opponent_paddle.move(-PADDLE_SPEED)

        # Ball movement
        ball.move()

        # Ball collision with top and bottom walls
        if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
            ball.dy *= -1

        # Ball collision with paddles
        if ball.rect.colliderect(player_paddle.rect) or ball.rect.colliderect(opponent_paddle.rect):
            ball.dx *= -1

        # Ball out of bounds
        if ball.rect.left <= 0:
            opponent_score += 1
            ball.rect.center = (WIDTH // 2, HEIGHT // 2)
            ball.dx = random.choice([-1, 1]) * BALL_SPEED_X
            ball.dy = random.choice([-1, 1]) * BALL_SPEED_Y
        elif ball.rect.right >= WIDTH:
            player_score += 1
            ball.rect.center = (WIDTH // 2, HEIGHT // 2)
            ball.dx = random.choice([-1, 1]) * BALL_SPEED_X
            ball.dy = random.choice([-1, 1]) * BALL_SPEED_Y

        # Check for game over
        if player_score >= 10 or opponent_score >= 10:
            state = GAME_OVER

        # Clear screen
        screen.fill(BLACK)

        # Draw elements
        pygame.draw.rect(screen, WHITE, player_paddle.rect)
        pygame.draw.rect(screen, WHITE, opponent_paddle.rect)
        pygame.draw.ellipse(screen, WHITE, ball.rect)

        # Draw score
        player_text = font.render(f"Player: {player_score}", True, WHITE)
        opponent_text = font.render(f"Opponent: {opponent_score}", True, WHITE)
        screen.blit(player_text, (10, 10))
        screen.blit(opponent_text, (WIDTH - opponent_text.get_width() - 10, 10))

    elif state == GAME_OVER:
        screen.fill(BLACK)
        game_over = font.render("Game Over", True, WHITE)
        winner = font.render(f"{'Player' if player_score > opponent_score else 'Opponent'} Wins!", True, WHITE)
        restart = font.render("Press SPACE to restart", True, WHITE)
        screen.blit(game_over, (WIDTH // 2 - game_over.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(winner, (WIDTH // 2 - winner.get_width() // 2, HEIGHT // 2))
        screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 50))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                state = MENU

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
