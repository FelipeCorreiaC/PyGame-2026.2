import pygame
import random

class Bomba:
    def __init__(self, x, y):
        self.x=x
        self.y=y

        self.raio=30
        self.gravidade=0.5

        # Velocidade vertical
        self.velocidade_y=random.uniform(-23, -19)

        # Escolhe o movimento
        self.movimento=random.choice(["vertical", "parabolico"])

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

    def desenhar(self, tela):
        # Bomba representada temporariamente por um círculo preto
        pygame.draw.circle(tela,(0, 0, 0),(int(self.x), int(self.y)),self.raio)

        # Contorno branco para enxergarmos no fundo escuro
        pygame.draw.circle(tela,(255, 255, 255),(int(self.x), int(self.y)),self.raio,2)

    def verificar_colisao(self, pos_mouse):
        mouse_x, mouse_y=pos_mouse

        distancia=((mouse_x - self.x) ** 2 +(mouse_y - self.y) ** 2)

        return distancia <= self.raio ** 2