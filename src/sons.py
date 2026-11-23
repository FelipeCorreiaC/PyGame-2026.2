# Efeitos sonoros criados com assistência de IA (ChatGPT) para este projeto.
# Este arquivo carrega e reproduz apenas efeitos; não utiliza música de fundo.

# os monta os caminhos dos arquivos em Windows, Linux e macOS.
import os

# pygame oferece o mixer, responsável por carregar e tocar os arquivos WAV.
import pygame


# Centraliza os sons para que nenhum objeto precise reler os arquivos de áudio.
class Sons:

    # Carrega os efeitos uma única vez, depois que pygame.init() foi chamado.
    def __init__(self):

        # Guarda os efeitos disponíveis, identificados pelo nome de cada ação.
        self.efeitos={}

        # Sem dispositivo de áudio, permite que o jogo continue funcionando.
        self.ativo=pygame.mixer.get_init() is not None

        if not self.ativo:
            print("Áudio indisponível: o jogo continuará sem efeitos sonoros.")
            return

        # Reserva três canais importantes:
        # 0 = explosão
        # 1 = fim de jogo
        # 2 = pavio da bomba
        pygame.mixer.set_reserved(3)

        self.canal_explosao=pygame.mixer.Channel(0)
        self.canal_fim=pygame.mixer.Channel(1)
        self.canal_pavio=pygame.mixer.Channel(2)

        # Localiza a pasta de sons a partir deste arquivo.
        caminho_sons=os.path.join(
            os.path.dirname(__file__),
            "..",
            "assets",
            "sounds"
        )

        # Cada entrada informa o arquivo e o volume.
        arquivos={
            "corte": ("corte.wav",0.50),
            "explosao": ("explosao.wav",0.65),
            "fim_de_jogo": ("fim_de_jogo.wav",0.55),
            "pavio": ("pavio_queimando.wav",0.40)
        }

        # Carrega todos os efeitos.
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


    # Reproduz um efeito já carregado.
    def tocar(self,nome):

        efeito=self.efeitos.get(nome)

        if efeito is None:
            return

        if nome=="explosao":

            # Para o pavio antes da explosão.
            self.parar_pavio()

            # Interrompe os outros efeitos.
            pygame.mixer.stop()

            self.canal_explosao.play(efeito)

        elif nome=="fim_de_jogo":

            self.canal_fim.play(efeito)

        else:

            efeito.play()


    # Inicia o pavio em loop enquanto houver bomba na tela.
    def iniciar_pavio(self):

        efeito=self.efeitos.get("pavio")

        if efeito is None:
            return

        # Não reinicia o áudio caso ele já esteja tocando.
        if not self.canal_pavio.get_busy():
            self.canal_pavio.play(
                efeito,
                loops=-1
            )


    # Interrompe o som do pavio.
    def parar_pavio(self):

        if self.ativo:
            self.canal_pavio.stop()


    # Encerra todos os efeitos da partida anterior.
    def parar(self):

        if self.ativo:
            pygame.mixer.stop()