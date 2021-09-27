import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))

running = True

herbe = pygame.image.load('herbe.png')
centre = pygame.image.load('centre.png')

carte = [[0] * 500 for _ in range(500)]  # 50 pixels par case
x, y = 6000, 15000
xCase, yCase = 120, 300
carte[124][305] = 1

yBoolM, yBoolP, xBoolM, xBoolP, = False, False, False, False,

while running:

    screen.fill((0, 0, 0))

    screen.blit(herbe, (100, 200))
    screen.blit(herbe, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                yBoolM = True
            if event.key == pygame.K_z:
                yBoolP = True
            if event.key == pygame.K_d:
                xBoolM = True
            if event.key == pygame.K_q:
                xBoolP = True
            if event.key == pygame.K_SPACE:
                x, y = 6000, 15000
                yCase = y//50
                xCase = x//50

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                yBoolM = False
            if event.key == pygame.K_z:
                yBoolP = False
            if event.key == pygame.K_d:
                xBoolM = False
            if event.key == pygame.K_q:
                xBoolP = False

    if yBoolM and y > 0:
        y -= 1
        yCase = y//50
    if yBoolP and y < 25000:
        y += 1
        yCase = y//50
    if xBoolM and x > 0:
        x -= 1
        xCase = x//50
    if xBoolP and x < 25000:
        x += 1
        xCase = x//50

    for i in range(192):
        if carte[xCase + int(i % 16)][yCase + int(i / 16)] == 1:
            screen.blit(centre, (int(i % 16) * 50 +(xCase*50-x), int(i / 16) * 50 +(yCase*50-y)))

    pygame.display.flip()
