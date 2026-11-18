
# Classe responsável por controlar o estado geral da partida.
class Jogo:
    def __init__(self):
        # Pontuação inicial
        self.pontuacao = 0

    def adicionar_pontos(self, pontos):
        self.pontuacao += pontos