import pygame

# Test Mateo
# Test Adam
# Test Fabien
# Test Mathieu PENE le bg

pygame.init()

screen = pygame.display.set_mode((800, 600))

running = True

herbe = pygame.image.load('herbe.png')
centre = pygame.image.load('centre.png')

carte = [[0] * 5000 for _ in range(5000)]  # 50 pixels par case
x, y = 120, 300
carte[124][305] = 1

yBoolM,yBoolP,xBoolM,xBoolP, = False,False,False,False,

while running:

    screen.fill((0, 0, 0))

    screen.blit(herbe, (100, 200))

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
                x,y = 100, 280

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
    if yBoolP and y < 5000:
        y += 1
    if xBoolM and x > 0:
        x -= 1
    if xBoolP and x < 5000:
        x += 1

    for i in range(4800):
        if carte[x + int(i % 80)][y + int(i / 80)] == 0:
            screen.blit(herbe, (int(i % 80) * 10, int(i / 80) * 10))
    for i in range(4800):
        if carte[x + int(i % 80)][y + int(i / 80)] == 1:
            screen.blit(centre, (int(i % 80) * 10, int(i / 80) * 10))

    pygame.display.flip()
