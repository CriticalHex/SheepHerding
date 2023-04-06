import pygame
import random
import copy

SCREEN_W = 800
SCREEN_H = 800


class Sheep:
    sheep_image = pygame.image.load("sheep.jpg")

    def __init__(self) -> None:
        self.rect = pygame.Rect(
            random.randrange(SCREEN_W), random.randrange(SCREEN_H), 35, 35
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


def main():
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), vsync=1)
    pygame.display.set_caption("Sheepies")
    running = True
    clock = pygame.time.Clock()
    done = False
    player = Player("PLAYER")
    pspeed = 5

    sheep: list[Sheep] = []
    for _ in range(100):
        sheep.append(Sheep())

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL]:
            running = False
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
        sheep = copy.copy(cloned_sheep)

        screen.fill((0, 0, 0))

        for shoop in sheep:
            shoop.move()
            shoop.draw(screen)

        player.draw(screen)

        pygame.display.flip()


main()
