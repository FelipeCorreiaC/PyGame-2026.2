import pygame

pygame.init()

LARGURA=1280
ALTURA=720

tela=pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("NOME DO JOGO")

clock=pygame.time.Clock()
rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type==pygame.QUIT:
            rodando=False

    tela.fill((30, 30, 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()