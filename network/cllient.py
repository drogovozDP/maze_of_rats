import pygame
from network import Network

width, height, FPS = 500, 500, 60

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0


class Player:
    def __init__(self, x, y, color, width=34, height=34):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.vel = 5
        self.rect = (self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]: self.y -= self.vel
        if keys[pygame.K_DOWN]: self.y += self.vel
        if keys[pygame.K_LEFT]: self.x -= self.vel
        if keys[pygame.K_RIGHT]: self.x += self.vel
        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


def read_pos(pos):
    pos = pos.split(",")
    return int(pos[0]), int(pos[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def redraw_window(screen):
    screen.fill((255, 255, 255))
    for player in players:
        player.draw(screen)
    pygame.display.update()


players = []


def main():
    run = True
    clock = pygame.time.Clock()

    net = Network('127.0.0.1', 8000)
    startPos = read_pos(net.getPos())
    players.append(Player(startPos[0], startPos[1], (0, 255, 0)))
    players.append(Player(0, 0, (255, 0, 0)))

    while run:
        clock.tick(FPS)

        p_2_pos = read_pos(net.send(make_pos((players[0].x, players[0].y))))
        players[1].x = p_2_pos[0]
        players[1].y = p_2_pos[1]
        players[1].update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                # pygame.quit()
                # return # говнокод, иначе ошибка при попытке отрисовки в пустой переменной

        players[0].move()
        redraw_window(screen)


main()