# Musica de fundo integrada com assistencia de IA (ChatGPT).
# A trilha e original, instrumental e reproduzida somente durante a partida.

# os permite localizar o arquivo em qualquer pasta de instalacao do jogo.
import os

# O canal music reproduz a trilha separadamente dos efeitos de corte e explosao.
import pygame


# Volume entre 0.0 e 1.0; baixo para manter os efeitos sonoros em destaque.
VOLUME_MUSICA = 0.16


# Centraliza o carregamento e o controle da trilha, sem mudar os sons existentes.
class Musica:
    # Carrega a trilha uma unica vez, depois de pygame.init().
    def __init__(self):
        # Caso o computador nao tenha audio disponivel, a partida continua normal.
        self.carregada = False
        if pygame.mixer.get_init() is None:
            return

        # O caminho depende deste modulo, e nao da pasta em que o terminal abriu.
        caminho = os.path.join(
            os.path.dirname(__file__), "..", "assets", "music", "musica_arcade.wav"
        )

        # O mixer mantem um unico canal de musica, independente dos canais dos efeitos.
        try:
            pygame.mixer.music.load(caminho)
            pygame.mixer.music.set_volume(VOLUME_MUSICA)
            self.carregada = True
        except (pygame.error, OSError) as erro:
            # Uma trilha ausente nao deve impedir o funcionamento do restante do jogo.
            print(f"Nao foi possivel carregar a musica: {erro}")

    # Comeca a trilha do inicio a cada nova partida, repetindo-a automaticamente.
    def iniciar(self):
        """Inicia a trilha em repeticao, com volume baixo e entrada gradual."""
        if self.carregada:
            # A entrada de 350 ms suaviza o comeco sem interromper o loop do jogo.
            pygame.mixer.music.set_volume(VOLUME_MUSICA)
            pygame.mixer.music.play(loops=-1, fade_ms=350)

    # Abre espaco para os efeitos de explosao e derrota ao encerrar a partida.
    def parar(self):
        """Interrompe a musica imediatamente, preservando os efeitos sonoros."""
        if self.carregada:
            # stop nao adiciona uma espera ao processamento da explosao ou do game over.
            pygame.mixer.music.stop()
