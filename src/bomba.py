import pygame
import random
import os

# Reaproveita imagens já carregadas e redimensionadas entre as bombas.
from imagens import imagem_redimensionada

# Caminho para a pasta de imagens
CAMINHO_IMAGES=os.path.join(os.path.dirname(__file__), "..", "assets", "images", "sprites_bombas")

# Lista com as variações de bombas
SPRITES_BOMBAS=[
    os.path.join("fire", "frame_1.png"),
    os.path.join("iron", "frame_1.png"),
    os.path.join("lightning", "frame_1.png"),
    os.path.join("shadow", "frame_1.png")
]

class Bomba:
    def __init__(self, x, y):
        self.x=x
        self.y=y

        self.raio=random.randint(50, 60)
        self.gravidade=0.5

        # Escolhe aleatoriamente o sprite da bomba
        sprite=random.choice(SPRITES_BOMBAS)
        caminho_sprite=os.path.join(CAMINHO_IMAGES, sprite)

        # Bombas com o mesmo sprite e tamanho compartilham a imagem preparada.
        # Não alteramos essa superfície; a rotação cria uma nova imagem ao desenhar.
        self.imagem=imagem_redimensionada(
            caminho_sprite,
            self.raio*2,
            self.raio*2
        )

        # Velocidade vertical
        self.velocidade_y=random.uniform(-23, -19)

        # Escolhe o movimento
        self.movimento=random.choice(["vertical", "parabolico"])

        # Define a rotação da bomba
        self.angulo=0
        self.velocidade_rotacao=random.uniform(-4,4)

        # Evita rotações muito lentas
        while -1 < self.velocidade_rotacao < 1:
            self.velocidade_rotacao=random.uniform(-4,4)

        if self.movimento == "vertical":
            self.velocidade_x=0
        else:
            self.velocidade_x=random.uniform(-5, 5)

            while -2 < self.velocidade_x < 2:
                self.velocidade_x=random.uniform(-5, 5)

    def atualizar(self):
        self.x+=self.velocidade_x
        self.y+=self.velocidade_y

        self.velocidade_y+=self.gravidade

        # Atualiza a rotação
        self.angulo+=self.velocidade_rotacao

    def desenhar(self, tela):
        imagem_rotacionada=pygame.transform.rotate(
            self.imagem,
            self.angulo
        )

        retangulo=imagem_rotacionada.get_rect(
            center=(int(self.x),int(self.y))
        )

        tela.blit(imagem_rotacionada,retangulo)

    def verificar_colisao(self, pos_mouse):
        mouse_x, mouse_y=pos_mouse

        distancia=((mouse_x - self.x) ** 2 +(mouse_y - self.y) ** 2)

        return distancia <= self.raio ** 2
