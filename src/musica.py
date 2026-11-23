# Musica de fundo integrada com assistencia de IA (ChatGPT).
# A trilha e original, instrumental e reproduzida somente durante a partida.

import os
import pygame


# Volume da música de fundo
VOLUME_MUSICA=0.16


class Musica:

    def __init__(self):
        self.carregada=False

        if pygame.mixer.get_init() is None:
            return

        caminho=os.path.join(
            os.path.dirname(__file__),
            "..",
            "assets",
            "music",
            "musica_arcade.wav"
        )

        try:
            pygame.mixer.music.load(caminho)
            pygame.mixer.music.set_volume(VOLUME_MUSICA)
            self.carregada=True

        except (pygame.error,OSError) as erro:
            print(f"Nao foi possivel carregar a musica: {erro}")


    # Inicia a música desde o começo e mantém em repetição
    def iniciar(self):
        if self.carregada:
            pygame.mixer.music.set_volume(VOLUME_MUSICA)
            pygame.mixer.music.play(
                loops=-1,
                fade_ms=350
            )


    # Interrompe a música
    def parar(self):
        if self.carregada:
            pygame.mixer.music.stop()