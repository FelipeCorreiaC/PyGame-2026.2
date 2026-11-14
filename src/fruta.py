# IMPORTAÇÃO DAS BIBLIOTECAS
import pygame
import random

# CLASSE FRUTA
class Fruta:
    def __init__(self, x, y):
        # Define a posição inicial da fruta
        self.x=x
        self.y=y

        # Define o tamanho e a gravidade
        self.raio=30
        self.gravidade=0.5

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

    # Desenha a fruta na tela
    def desenhar(self, tela):
        pygame.draw.circle(tela,(255, 0, 0),(int(self.x), int(self.y)),self.raio)