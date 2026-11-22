# IMPORTAÇÃO DAS BIBLIOTECAS
import pygame
import random

# Importa as classes
from fruta import Fruta
from jogo import Jogo
from bomba import Bomba

# Inicializa os módulos do Pygame
pygame.init()
# Objeto que representa o estado da partida
jogo = Jogo()

# Define as dimensões da janela
LARGURA=1280
ALTURA=720

# LISTA DE FRUTAS
# Armazena todas as frutas ou bombas ativas na tela
frutas=[]
bombas=[]

# CONFIGURAÇÃO DO TEMPORIZADOR
# Controla a geração aleatória das frutas e bombas.
# Evento personalizado para gerar frutas e bombas.
EVENTO_FRUTA=pygame.USEREVENT+1
EVENTO_BOMBA = pygame.USEREVENT + 2

# Intervalo mínimo e máximo (milissegundos) (frutas)
TEMPO_MIN=500
TEMPO_MAX=1800

# Intervalo mínimo e máximo (milissegundos) (bombas)
TEMPO_BOMBA_MIN = 3000
TEMPO_BOMBA_MAX = 6000

# Agenda a primeira bomba
pygame.time.set_timer(EVENTO_BOMBA,random.randint(TEMPO_BOMBA_MIN, TEMPO_BOMBA_MAX),loops=1)

# Agenda a primeira fruta
pygame.time.set_timer(EVENTO_FRUTA,random.randint(TEMPO_MIN, TEMPO_MAX),loops=1)

# CONFIGURAÇÃO DA JANELA
# Cria a janela do jogo
tela=pygame.display.set_mode((LARGURA, ALTURA))

# Define o título
pygame.display.set_caption("NOME DO JOGO")

# Controla a taxa de atualização
clock=pygame.time.Clock()

# Mantém o jogo em execução
rodando=True

# LOOP PRINCIPAL DO JOGO
while rodando:
    # PROCESSAMENTO DE EVENTOS
    for evento in pygame.event.get():
        # Fecha o jogo
        if evento.type==pygame.QUIT:
            rodando=False

        if evento.type == EVENTO_BOMBA and not jogo.game_over:
            x = random.randint(200, LARGURA - 200)

            bomba = Bomba(x, ALTURA + 30)
            bombas.append(bomba)

            proximo_tempo = random.randint(TEMPO_BOMBA_MIN,TEMPO_BOMBA_MAX)

            pygame.time.set_timer(EVENTO_BOMBA,proximo_tempo,loops=1)

        # DETECÇÃO DE CORTE COM O MOUSE
        if evento.type == pygame.MOUSEMOTION and not jogo.game_over:
            # Verifica se o mouse passou sobre alguma fruta
            for fruta in frutas[:]:
                if fruta.verificar_corte(evento.pos):
                    frutas.remove(fruta)

                    # Adiciona 1 ponto pela fruta cortada
                    jogo.adicionar_pontos(1)

            # Verifica as bombas
            for bomba in bombas[:]:
                if bomba.verificar_colisao(evento.pos):
                    bombas.remove(bomba)
                    jogo.game_over = True
                    break

        # Gera uma nova fruta
        if evento.type==EVENTO_FRUTA and not jogo.game_over:

            # Sorteia a posição horizontal
            x=random.randint(200, LARGURA - 200)

            # Cria uma fruta abaixo da tela
            fruta=Fruta(x, ALTURA + 30)

            # Adiciona à lista de frutas
            frutas.append(fruta)

            # Sorteia o intervalo até a próxima fruta
            proximo_tempo=random.randint(TEMPO_MIN, TEMPO_MAX)

            # Agenda a próxima geração
            pygame.time.set_timer(EVENTO_FRUTA,proximo_tempo,loops=1)

    # LIMPEZA DA TELA
    tela.fill((30, 30, 30))

    # ATUALIZAÇÃO DOS OBJETOS
    if not jogo.game_over:
        # Percorre uma cópia para remover frutas com segurança
        for fruta in frutas[:]:
            fruta.atualizar()

            if fruta.y - fruta.raio > ALTURA:
                frutas.remove(fruta)
                jogo.perder_vida()

                # Interrompe o laço se esta era a última vida
                if jogo.game_over:
                    break

        # A partida pode ter terminado durante a atualização das frutas
        if not jogo.game_over:
            for bomba in bombas[:]:
                bomba.atualizar()

                # Se a bomba cair, apenas remove
                if bomba.y - bomba.raio > ALTURA:
                    bombas.remove(bomba)

    # DESENHO DOS OBJETOS
    # Continua desenhando após o game over para manter a cena parada
    for fruta in frutas:
        fruta.desenhar(tela)

    for bomba in bombas:
        bomba.desenhar(tela)

    # Fonte usada na interface
    fonte = pygame.font.SysFont("Arial", 36)

    if not jogo.game_over:
        # EXIBIÇÃO DA PONTUAÇÃO
        texto_pontos = fonte.render(f"fruta.png: {jogo.pontuacao}",True,(255, 255, 255))
        tela.blit(texto_pontos, (30, 60))

        # EXIBIÇÃO DAS VIDAS
        texto_vidas = fonte.render(f"vidas.png: {jogo.vidas}",True,(255, 255, 255))
        tela.blit(texto_vidas, (1090, 60))
    else:
        # Exibe apenas as informações de Game Over
        texto_game_over = fonte.render("GAME OVER",True,(255, 255, 255))
        texto_final = fonte.render(f"Pontuação final: {jogo.pontuacao}",True,(255, 255, 255))

        tela.blit(texto_game_over,texto_game_over.get_rect(center=(LARGURA // 2, ALTURA // 2)))
        tela.blit(texto_final,texto_final.get_rect(center=(LARGURA // 2, ALTURA // 2 + 50)))

    # ATUALIZAÇÃO DA JANELA
    pygame.display.flip()

    # Limita a aproximadamente 60 FPS
    clock.tick(60)

# ENCERRAMENTO
pygame.quit()
