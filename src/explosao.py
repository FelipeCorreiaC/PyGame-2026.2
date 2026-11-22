import pygame
import os
import random

# Caminho para a spritesheet da explosão
CAMINHO_IMAGES=os.path.join(
    os.path.dirname(__file__),
    "..",
    "assets",
    "images",
    "sprite_explosão"
)

class Explosao:
    def __init__(self, x, y):
        self.x=x
        self.y=y

        # Carrega a spritesheet
        caminho_sprite=os.path.join(
            CAMINHO_IMAGES,
            "explosion.png"
        )

        spritesheet=pygame.image.load(
            caminho_sprite
        ).convert_alpha()

        self.frames=[]

        # Quantidade de frames da spritesheet
        quantidade_frames=12

        largura_frame=spritesheet.get_width()//quantidade_frames
        altura_frame=spritesheet.get_height()

        # Define um tamanho aleatório para a explosão
        self.tamanho=random.randint(180,250)

        # Separa a spritesheet em frames
        for frame_numero in range(quantidade_frames):

            frame=spritesheet.subsurface(
                frame_numero*largura_frame,
                0,
                largura_frame,
                altura_frame
            )

            frame=pygame.transform.scale(
                frame,
                (self.tamanho,self.tamanho)
            )

            self.frames.append(frame)

        # Controle da animação
        self.frame_atual=0
        self.tempo_ultimo_frame=pygame.time.get_ticks()
        self.tempo_frame=50
        self.finalizada=False

    def atualizar(self):
        agora=pygame.time.get_ticks()

        if agora-self.tempo_ultimo_frame >= self.tempo_frame:

            self.frame_atual+=1
            self.tempo_ultimo_frame=agora

            if self.frame_atual >= len(self.frames):
                self.finalizada=True

    def desenhar(self, tela):
        if not self.finalizada:

            frame=self.frames[self.frame_atual]

            retangulo=frame.get_rect(
                center=(int(self.x),int(self.y))
            )

            tela.blit(frame,retangulo)