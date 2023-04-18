import pygame
import random
import copy

pygame.init()

SCREEN_W = 800
SCREEN_H = 800
FONT_SIZE = 64


def read_scores():
    with open("scores.txt", "r") as scores_file:
        data = scores_file.read()
    pairs = data.split("\n")
    scores: list[tuple[str, str]] = []
    for pair in pairs:
        if pair:
            name, score = pair.split(":")
            scores.append((name, score))
    return scores


def scores_to_rendertext(scores: list[tuple[str, str]]):
    text_scores: list[Text] = []
    scores.sort(key=lambda x: int(x[1]), reverse=True)
    for n, pair in enumerate(scores):
        name, score = pair
        box = Text(
            pygame.Vector2(0, n * FONT_SIZE),
            pygame.Vector2((len(name) + len(score)) * FONT_SIZE, FONT_SIZE / 5),
            pygame.Color(0, 0, 255),
        )
        box.update_text(f"{n+1}. {name}: {score}")
        text_scores.append(box)
    return text_scores


class Text:
    def __init__(
        self, pos: pygame.Vector2, size: pygame.Vector2, color: tuple[int, int, int]
    ) -> None:
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.text: str = ""
        self.text_box = pygame.Rect(pos, size)
        self.text_color = pygame.Color(color)
        self.text_surface = self.font.render(self.text, True, self.text_color)

    def update_text(self, text: str):
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.text_color)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.text_surface, self.text_box)


class Sheep:
    sheep_image = pygame.image.load("sheep.jpg")

    def __init__(self) -> None:
        SHEEP_SIZE = 35
        self.rect = pygame.Rect(
            random.randrange(SHEEP_SIZE, SCREEN_W - SHEEP_SIZE),
            random.randrange(SHEEP_SIZE, SCREEN_H - SHEEP_SIZE),
            SHEEP_SIZE,
            SHEEP_SIZE,
        )

    def move(self):
        direction = pygame.Vector2(
            random.randrange(-5, 6, 5), random.randrange(-5, 6, 5)
        )
        if self.in_bounds(direction):
            self.rect.move_ip(direction)

    def draw(self, screen: pygame.Surface):
        screen.blit(Sheep.sheep_image, self.rect)

    def in_bounds(self, direction: pygame.Vector2):
        new_pos = pygame.Vector2(*self.rect.topleft) + direction
        return (
            new_pos.x >= 0
            and new_pos.x + self.rect.w <= SCREEN_W
            and new_pos.y >= 0
            and new_pos.y + self.rect.h <= SCREEN_H
        )


class Player:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.rect = pygame.Rect(400, 400, 50, 50)
        self.score = 0
        self.score_text = Text(
            pygame.Vector2(), pygame.Vector2(200, FONT_SIZE), (0, 0, 255)
        )

    def move(self, direction: pygame.Vector2):
        if self.in_bounds(direction):
            self.rect.move_ip(direction)

    def in_bounds(self, direction: pygame.Vector2):
        new_pos = pygame.Vector2(*self.rect.topleft) + direction
        return (
            new_pos.x >= 0
            and new_pos.x + self.rect.w <= SCREEN_W
            and new_pos.y >= 0
            and new_pos.y + self.rect.h <= SCREEN_H
        )

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, pygame.Color("green"), self.rect)
        self.score_text.update_text(f"Score: {self.score}")
        self.score_text.draw(screen)

    def save_score(self):
        with open("scores.txt", "a") as scores_file:
            scores_file.write(f"{self.name}:{self.score}\n")


def main():
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), vsync=1)
    pygame.display.set_caption("Sheepies")
    running = True
    clock = pygame.time.Clock()
    playing = True
    player = Player("PLAYER")
    pspeed = 5
    text_scores = scores_to_rendertext(read_scores())
    sheep: list[Sheep] = []
    for _ in range(100):
        sheep.append(Sheep())

    while running:
        while playing:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL]:
                playing = False
                running = False
            if keys[pygame.K_ESCAPE]:
                playing = False
                player.save_score()
                text_scores = scores_to_rendertext(read_scores())
            if keys[pygame.K_w]:
                player.move(pygame.Vector2(0, -pspeed))
            if keys[pygame.K_s]:
                player.move(pygame.Vector2(0, pspeed))
            if keys[pygame.K_a]:
                player.move(pygame.Vector2(-pspeed, 0))
            if keys[pygame.K_d]:
                player.move(pygame.Vector2(pspeed, 0))

            cloned_sheep = copy.copy(sheep)
            for shoop in sheep:
                if shoop.rect.colliderect(player.rect):
                    cloned_sheep.remove(shoop)
                    player.score += 1
            sheep = copy.copy(cloned_sheep)
            if len(sheep) == 0:
                playing = False
                player.save_score()
                text_scores = scores_to_rendertext(read_scores())

            screen.fill((0, 0, 0))

            for shoop in sheep:
                shoop.move()
                shoop.draw(screen)

            player.draw(screen)

            pygame.display.flip()

        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL]:
            running = False

        screen.fill((0, 0, 0))

        for score in text_scores:
            score.draw(screen)

        pygame.display.flip()


main()
