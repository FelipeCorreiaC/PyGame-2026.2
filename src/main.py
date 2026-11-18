# IMPORTAÇÃO DAS BIBLIOTECAS
import pygame
import random

# Importa as classes
from fruta import Fruta
from jogo import Jogo

# Inicializa os módulos do Pygame
pygame.init()
# Objeto que representa o estado da partida
jogo = Jogo()

# Define as dimensões da janela
LARGURA=1280
ALTURA=720

# LISTA DE FRUTAS
# Armazena todas as frutas ativas na tela
frutas=[]

# CONFIGURAÇÃO DO TEMPORIZADOR
# Controla a geração aleatória das frutas.
# Evento personalizado para gerar frutas
EVENTO_FRUTA=pygame.USEREVENT+1

# Intervalo mínimo e máximo (milissegundos)
TEMPO_MIN=500
TEMPO_MAX=1800

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

        # DETECÇÃO DE CORTE COM O MOUSE
        if evento.type == pygame.MOUSEMOTION and not jogo.game_over:
            # Verifica se o mouse passou sobre alguma fruta
            for fruta in frutas:
                if fruta.verificar_corte(evento.pos):
                    frutas.remove(fruta)

                    # Adiciona 10 pontos pela fruta cortada
                    jogo.adicionar_pontos(1)

                    if not jogo.game_over:

                        for fruta in frutas:
                            fruta.atualizar()
                            fruta.desenhar(tela)

                            if fruta.y - fruta.raio > ALTURA:
                                frutas.remove(fruta)
                                jogo.perder_vida()

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

    # ATUALIZAÇÃO E DESENHO DAS FRUTAS
    for fruta in frutas:
        # Atualiza o movimento
        fruta.atualizar()

        # Desenha a fruta
        fruta.desenhar(tela)

        # Remove frutas que saíram pela parte inferior
        if fruta.y-fruta.raio > ALTURA:
            frutas.remove(fruta)
            jogo.perder_vida()

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
