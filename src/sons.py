# Efeitos sonoros criados com assistência de IA (ChatGPT) para este projeto.
# Este arquivo carrega e reproduz apenas efeitos; não utiliza música de fundo.

import os
import pygame


# Centraliza os sons para que nenhum objeto precise reler os arquivos de áudio.
class Sons:

    # Carrega os efeitos uma única vez, depois que pygame.init() foi chamado.
    def __init__(self):
        self.efeitos={}

        # Sem dispositivo de áudio, o jogo continua funcionando normalmente.
        self.ativo=pygame.mixer.get_init() is not None

        if not self.ativo:
            print("Áudio indisponível: o jogo continuará sem efeitos sonoros.")
            return

        # Reserva canais específicos para efeitos importantes
        pygame.mixer.set_reserved(3)

        self.canal_explosao=pygame.mixer.Channel(0)
        self.canal_fim=pygame.mixer.Channel(1)
        self.canal_pavio=pygame.mixer.Channel(2)

        # Localiza a pasta de sons
        caminho_sons=os.path.join(
            os.path.dirname(__file__),
            "..",
            "assets",
            "sounds"
        )

        # Arquivos e seus respectivos volumes
        arquivos={
            "corte": ("corte.wav",0.50),
            "explosao": ("explosao.wav",0.65),
            "fim_de_jogo": ("fim_de_jogo.wav",0.55),
            "pavio": ("pavio_queimando.wav",0.40)
        }

        # Carrega os efeitos
        for nome,(arquivo,volume) in arquivos.items():

            try:
                efeito=pygame.mixer.Sound(
                    os.path.join(caminho_sons,arquivo)
                )

                efeito.set_volume(volume)
                self.efeitos[nome]=efeito

            except (pygame.error,OSError) as erro:
                print(
                    f"Não foi possível carregar o som '{nome}': {erro}"
                )


    # Reproduz um efeito já carregado
    def tocar(self,nome):
        efeito=self.efeitos.get(nome)

        if efeito is None:
            return

        if nome=="explosao":
            self.parar_pavio()
            pygame.mixer.stop()
            self.canal_explosao.play(efeito)

        elif nome=="fim_de_jogo":
            self.canal_fim.play(efeito)

        else:
            efeito.play()


    # Mantém o pavio tocando enquanto houver bomba na tela
    def iniciar_pavio(self):
        efeito=self.efeitos.get("pavio")

        if efeito is None:
            return

        if not self.canal_pavio.get_busy():
            self.canal_pavio.play(
                efeito,
                loops=-1
            )


    # Interrompe o som do pavio
    def parar_pavio(self):
        if self.ativo:
            self.canal_pavio.stop()


    # Interrompe todos os efeitos
    def parar(self):
        if self.ativo:
            pygame.mixer.stop()