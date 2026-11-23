import pygame
import os
import random

# Reaproveita a spritesheet e os quadros preparados para cada tamanho de explosão.
from imagens import quadros_explosao

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

        # Localiza a spritesheet que será reaproveitada pelo módulo de imagens.
        caminho_sprite=os.path.join(
            CAMINHO_IMAGES,
            "explosion.png"
        )

        # Quantidade de frames da spritesheet
        quantidade_frames=12

        # Define um tamanho aleatório para a explosão
        self.tamanho=random.randint(180,250)

        # Explosões do mesmo tamanho compartilham os quadros já preparados.
        # Apenas consultamos as imagens, sem alterar a sequência ou suas superfícies.
        self.frames=quadros_explosao(
            caminho_sprite,
            quantidade_frames,
            self.tamanho
        )

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
