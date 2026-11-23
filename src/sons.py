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
        self.efeitos = {}

        # Sem dispositivo de áudio, permite que o jogo continue funcionando.
        self.ativo = pygame.mixer.get_init() is not None
        if not self.ativo:
            # O aviso aparece no terminal uma única vez, durante a preparação.
            print("Áudio indisponível: o jogo continuará sem efeitos sonoros.")
            return

        # Reserva dois canais para a explosão e o fim de jogo.
        # Assim, vários cortes simultâneos não impedem os avisos importantes.
        pygame.mixer.set_reserved(2)
        self.canal_explosao = pygame.mixer.Channel(0)
        self.canal_fim = pygame.mixer.Channel(1)

        # Localiza a pasta de sons a partir deste arquivo, não da pasta do terminal.
        caminho_sons = os.path.join(
            os.path.dirname(__file__), "..", "assets", "sounds"
        )

        # Cada entrada informa o arquivo e o volume, entre 0.0 e 1.0.
        # O corte fica discreto porque pode acontecer várias vezes por segundo.
        arquivos = {
            "corte": ("corte.wav", 0.50),
            "explosao": ("explosao.wav", 0.65),
            "fim_de_jogo": ("fim_de_jogo.wav", 0.55),
        }

        # Prepara todos os sons agora para apenas reproduzi-los durante a partida.
        for nome, (arquivo, volume) in arquivos.items():
            # Um arquivo ausente não deve impedir a abertura do jogo inteiro.
            try:
                # Lê o WAV, ajusta o volume e guarda o som para reutilização.
                efeito = pygame.mixer.Sound(os.path.join(caminho_sons, arquivo))
                efeito.set_volume(volume)
                self.efeitos[nome] = efeito
            except (pygame.error, OSError) as erro:
                # Identifica no terminal qual efeito não pôde ser carregado.
                print(f"Não foi possível carregar o som '{nome}': {erro}")

    # Reproduz um efeito já carregado, sem interromper o loop do jogo.
    def tocar(self, nome):
        # get() devolve None se aquele arquivo não estava disponível.
        efeito = self.efeitos.get(nome)
        if efeito is None:
            # Nesse caso, o restante da partida continua normalmente.
            return

        # A explosão interrompe cortes anteriores para destacar o impacto.
        if nome == "explosao":
            pygame.mixer.stop()
            self.canal_explosao.play(efeito)
        elif nome == "fim_de_jogo":
            # O canal separado preserva o final do som da explosão, se ainda tocar.
            self.canal_fim.play(efeito)
        else:
            # Os cortes usam os demais canais e podem se sobrepor brevemente.
            efeito.play()

    # Encerra os efeitos da partida anterior antes de iniciar uma nova.
    def parar(self):
        # Só utiliza o mixer se o áudio foi inicializado corretamente.
        if self.ativo:
            pygame.mixer.stop()
