# Classe responsável por controlar o estado geral da partida.
class Jogo:
    def __init__(self):
        # Pontuação inicial
        self.pontuacao=0
        self.vidas = 3

    def adicionar_pontos(self, pontos):
        self.pontuacao += pontos

    def perder_vida(self):
        self.vidas -= 1