import pygame
import sys
from random import randint

pygame.init()
WIDTH = 800
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (12, 89, 36)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
font = pygame.font.SysFont("Verdana", 60)


class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.height = height

        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

    def move_up(self, shift_size):
        self.rect.y -= shift_size
        if self.rect.y <= 0:
            self.rect.y = 0

    def move_down(self, shift_size, screen_height):
        self.rect.y += shift_size
        if self.rect.y >= screen_height - self.height:
            self.rect.y = screen_height - self.height


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.velocity = [randint(3, 12), randint(-10, 10)]
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def reverse(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8, 8)


player_one = Player(WHITE, 10, 100)
player_one.rect.x = 0
player_one.rect.y = (HEIGHT / 2) - 50

player_two = Player(WHITE, 10, 100)
player_two.rect.x = WIDTH - 10
player_two.rect.y = (HEIGHT / 2) - 50

ball = Ball(WHITE, 10, 10)
ball.rect.x = WIDTH / 2
ball.rect.y = HEIGHT / 2

all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(player_one)
all_sprites_list.add(player_two)
all_sprites_list.add(ball)

clock = pygame.time.Clock()

player_one_score = 0
player_two_score = 0
topScore = 10


def close():
    pygame.quit()
    sys.exit()


def game_over():
    player_number = ""
    if player_one_score == topScore or player_two_score == topScore:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        close()
            if player_one_score == topScore:
                player_number = "PLAYER ONE"
            elif player_two_score == topScore:
                player_number = "PLAYER TWO"

            winner = font.render(player_number, True, WHITE)
            message = font.render("IS THE WINNER", True, WHITE)
            screen.blit(winner, (WIDTH / 2 - 300, HEIGHT / 2 - 50))
            screen.blit(message, (WIDTH / 2 - 300, HEIGHT / 2))
            pygame.display.update()


def game():
    global player_one_score, player_two_score, topScore
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    close()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_one.move_up(5)
        if keys[pygame.K_s]:
            player_one.move_down(5, HEIGHT)
        if keys[pygame.K_UP]:
            player_two.move_up(5)
        if keys[pygame.K_DOWN]:
            player_two.move_down(5, HEIGHT)

        all_sprites_list.update()

        if ball.rect.x >= WIDTH - 1:
            player_one_score += 1
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.x <= 0:
            player_two_score += 1
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.y > HEIGHT - 1:
            ball.velocity[1] = -ball.velocity[1]
        if ball.rect.y < 0:
            ball.velocity[1] = -ball.velocity[1]

        if pygame.sprite.collide_mask(ball, player_one) or pygame.sprite.collide_mask(ball, player_two):
            ball.reverse()

        screen.fill(BACKGROUND)
        pygame.draw.line(screen, WHITE, [WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 5)
        all_sprites_list.draw(screen)

        font = pygame.font.SysFont("Verdana", 60)
        text = font.render(str(player_one_score), 1, WHITE)
        screen.blit(text, (WIDTH / 4, 10))
        text = font.render(str(player_two_score), 1, WHITE)
        screen.blit(text, (WIDTH / 1.4, 10))
        pygame.display.flip()

        game_over()

        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    game()
