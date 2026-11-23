# IMPORTAÇÃO DAS BIBLIOTECAS
import pygame
import random
import os

# Reaproveita imagens já carregadas e redimensionadas entre as frutas.
from imagens import imagem_redimensionada

# Caminho para a pasta de imagens
CAMINHO_IMAGES=os.path.join(os.path.dirname(__file__), "..", "assets", "images", "sprites_frutas")

# Lista com os sprites das frutas
SPRITES_FRUTAS=[
    ("green_pear.png", "green_pear_splited.png"),
    ("lemon_slice.png", "limon_slice_splited.png"),
    ("pineapple.png", "pineapple_splited.png"),
    ("watermelon.png", "watermelon_splited.png")
]

# CLASSE FRUTA
class Fruta:
    def __init__(self, x, y):
        # Define a posição inicial da fruta
        self.x=x
        self.y=y

        # Define o tamanho e a gravidade
        self.raio=random.randint(50, 60)
        self.gravidade=0.5

        # Escolhe aleatoriamente o sprite da fruta
        sprite, sprite_cortado=random.choice(SPRITES_FRUTAS)

        caminho_sprite=os.path.join(CAMINHO_IMAGES, sprite)
        caminho_sprite_cortado=os.path.join(CAMINHO_IMAGES, sprite_cortado)

        # Imagens do mesmo arquivo e tamanho são compartilhadas entre objetos.
        # Não alteramos essas superfícies; a rotação cria uma nova imagem ao desenhar.
        self.imagem=imagem_redimensionada(
            caminho_sprite,
            self.raio*2,
            self.raio*2
        )

        # Reaproveita também a versão cortada, mantendo seu tamanho original no jogo.
        self.imagem_cortada=imagem_redimensionada(
            caminho_sprite_cortado,
            int(self.raio*2.4),
            int(self.raio*2.4)
        )

        # Define a rotação da fruta
        self.angulo=0
        self.velocidade_rotacao=random.uniform(-4,4)

        # Evita rotações muito lentas
        while -1 < self.velocidade_rotacao < 1:
            self.velocidade_rotacao=random.uniform(-4,4)
        
        # Controla se a fruta já foi cortada
        self.cortada=False

        # Velocidade vertical aleatória
        self.velocidade_y=random.uniform(-23, -19)

        # Escolhe aleatoriamente o tipo de movimento
        self.movimento=random.choice(["vertical", "parabolico"])

        if self.movimento=="vertical":
            # Sem deslocamento horizontal
            self.velocidade_x = 0
        else:
            # Movimento horizontal aleatório
            self.velocidade_x=random.uniform(-5, 5)

            # Evita movimentos quase verticais
            while -2 < self.velocidade_x < 2:
                self.velocidade_x=random.uniform(-5, 5)

    # Atualiza a posição da fruta a cada frame
    def atualizar(self):
        self.x+=self.velocidade_x
        self.y+=self.velocidade_y

        # Aplica a gravidade à velocidade vertical
        self.velocidade_y+=self.gravidade

        self.angulo+=self.velocidade_rotacao

    # Verifica se o mouse está sobre a fruta
    def verificar_corte(self, pos_mouse):
        mouse_x, mouse_y = pos_mouse

        distancia=((mouse_x-self.x)**2+(mouse_y-self.y)**2)

        return distancia <= self.raio**2

    # Altera a fruta para o estado cortado
    def cortar(self):
        self.cortada=True

    # Desenha a fruta na tela
    def desenhar(self, tela):
        if self.cortada:
            imagem=self.imagem_cortada
        else:
            imagem=self.imagem

        # Rotaciona a imagem
        imagem_rotacionada=pygame.transform.rotate(
            imagem,
            self.angulo
        )

        retangulo=imagem_rotacionada.get_rect(
            center=(int(self.x),int(self.y))
        )

        tela.blit(imagem_rotacionada,retangulo)
