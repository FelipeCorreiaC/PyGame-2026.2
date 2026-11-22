# Classe responsável por controlar o estado geral da partida.
class Jogo:
    def __init__(self):
        self.reiniciar()

    # Restaura os valores iniciais da partida
    def reiniciar(self):
        self.pontuacao=0
        self.vidas=3
        self.game_over=False

    def adicionar_pontos(self, pontos):
        if not self.game_over:
            self.pontuacao += pontos

    def perder_vida(self):
        if not self.game_over and self.vidas > 0:
            self.vidas -= 1
            if self.vidas == 0:
                self.game_over = True
