import random
import pygame

pygame.init()

x = 1620
y = 1000

screen = pygame.display.set_mode((x,y))
pygame.display.set_caption('subquest')

back = pygame.image.load('oceano.png').convert_alpha()
back = pygame.transform.scale(back,(x,y))

bomba = pygame.image.load('bomba-ok.png').convert_alpha()
bomba = pygame.transform.scale(bomba,(90,90))

player = pygame.image.load('sub-ok.png').convert_alpha()
player = pygame.transform.scale(player,(150,130))

missil = pygame.image.load('missil-ok.png').convert_alpha()
missil = pygame.transform.scale(missil,(35,35))

pos_bomba_x = 1000
pos_bomba_y = 500

pos_player_x = 400
pos_player_y = 500

vel_missil_x = 0
pos_missil_x = 500
pos_missil_y = 570

pontos = -1

triggered =  False
pause = False
game_over = False

rodando = True

#tranformando em objetos
player_rect = player.get_rect()
bomba_rect = bomba.get_rect()
missil_rect = missil.get_rect()

font = pygame.font.SysFont("fonts/PixelGameFont.ttf",50)
pausado = pygame.font.SysFont('fonts/PixelGameFont.ttf', 90)
gameover = pygame.font.SysFont('fonts/PixelgameFont.ttf', 300)

#respawn da bomba

def respawn():
    x = 1690
    y = random.randint(400,880)
    return [x,y]

#respawn do missil
def respawn_missil():
    triggered = False
    respwan_missil_x = pos_player_x + 80
    respawn_missil_y = pos_player_y + 50
    vel_missil_x = 0
    return [respwan_missil_x,respawn_missil_y,triggered,vel_missil_x]

def colisao():
    global pontos
    if missil_rect.colliderect(bomba_rect):
        pontos += 1
        return True
    else:
        return False

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    screen.blit(back,(0,0))

    #criando o background
    rel_x = x % back.get_rect().width
    screen.blit(back,(rel_x - back.get_rect().width,0))
    if rel_x < 1620:
        screen.blit(back,(rel_x,0))

    #comandos
    comando = pygame.key.get_pressed()
    if comando[pygame.K_UP] and pos_player_y > 400:
        pos_player_y -= 1.2

        if not triggered:
            pos_missil_y -= 1.2
    if comando[pygame.K_DOWN] and pos_player_y < 880:
        pos_player_y += 1.2

        if not triggered:
            pos_missil_y += 1.2

    # comando pra pause
    if comando[pygame.K_p]:
        pause = True
    if comando[pygame.K_o]:
        pause = False
    if comando[pygame.K_q]:
        rodando = False

    #missil
    if comando[pygame.K_SPACE]:
        triggered = True
        vel_missil_x = 4


    #posição da bomba
    if pos_bomba_x == -40 or colisao():
        pos_bomba_x = respawn()[0]
        pos_bomba_y = respawn()[1]

    if pos_missil_x == 1000:
        pos_missil_x, pos_missil_y, triggered, vel_missil_x = respawn_missil()


    #posição do rect
    player_rect.y = pos_player_y
    player_rect.x = pos_player_x

    missil_rect.y = pos_missil_y
    missil_rect.x = pos_missil_x

    bomba_rect.y = pos_bomba_y
    bomba_rect.x = pos_bomba_x

    if pause == True:
        pauses = pausado.render('pausado!', True,(0,0,0), (255,255,255))
        screen.blit(pauses,(50,50))
        pygame.display.flip()
        continue

    if player_rect.colliderect(bomba_rect):
        acabou = gameover.render('game-over!', True, (0, 0, 0), (255, 255, 255))
        screen.blit(acabou, (250, 400))
        pygame.display.flip()
        continue

    #movimento
    x -= 2
    pos_bomba_x -= 2

    pos_missil_x += vel_missil_x



    #transformando imagens em objeto objetos
    #pygame.draw.rect(screen, (255,0,0), player_rect, 3)
    #pygame.draw.rect(screen, (255, 0, 0), missil_rect, 3)
    #pygame.draw.rect(screen, (255, 0, 0), bomba_rect, 3)

    score = font.render(f'Pontos: {int(pontos)}', True, (0, 0, 0))
    screen.blit(score, (50, 50))

    #adcionando imagens
    screen.blit(bomba,(pos_bomba_x,pos_bomba_y))
    screen.blit(missil,(pos_missil_x,pos_missil_y))
    screen.blit(player,(pos_player_x,pos_player_y))




    pygame.display.update()


