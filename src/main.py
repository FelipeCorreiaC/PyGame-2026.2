# IMPORTAÇÃO DAS BIBLIOTECAS
import pygame
import random
import os

# Importa as classes do jogo
from fruta import Fruta
from jogo import Jogo
from bomba import Bomba
from explosao import Explosao

# INICIALIZAÇÃO DO PYGAME E CONFIGURAÇÕES GERAIS
pygame.init()

# Objeto responsável pelo estado da partida
jogo=Jogo()

# TREMIDA DA TELA
tremendo=False
inicio_tremida=0
DURACAO_TREMIDA=200
INTENSIDADE_TREMIDA=8
CHANCE_TREMIDA=0.30
DURACAO_TREMIDA_BOMBA=800
INTENSIDADE_TREMIDA_BOMBA=15

# Dimensões da janela
LARGURA=1280
ALTURA=720

# Nome exibido na janela e na tela inicial
NOME_DO_JOGO="Jogo das Frutas"

# LISTAS E ESTADOS DOS OBJETOS
# Objetos ativos durante a partida
frutas=[]
bombas=[]
explosoes=[]

# Controla o estado intermediário entre atingir uma bomba
# e chegar à tela de Game Over
bomba_explodiu=False

# Feedbacks "+1" exibidos quando uma fruta é cortada
feedbacks_pontos=[]

# Momento em que a bomba foi atingida
momento_explosao=0

# Tempo máximo permitido para a animação antes do Game Over
DURACAO_MAX_EXPLOSAO=2000

# EVENTOS E TEMPORIZADORES
# Eventos personalizados responsáveis pelos lançamentos
EVENTO_FRUTA=pygame.USEREVENT+1
EVENTO_BOMBA=pygame.USEREVENT+2

# Intervalo inicial entre frutas (milissegundos)
TEMPO_MIN=300
TEMPO_MAX=1500

# Intervalo entre bombas (milissegundos)
TEMPO_BOMBA_MIN=3000
TEMPO_BOMBA_MAX=6000

# Os primeiros lançamentos são agendados somente
# quando o jogador inicia a partida com ENTER

# CONFIGURAÇÃO DA JANELA
tela=pygame.display.set_mode((LARGURA,ALTURA))
pygame.display.set_caption(NOME_DO_JOGO)

# Controla a taxa de atualização do jogo
clock=pygame.time.Clock()

# CARREGAMENTO DAS FONTES
CAMINHO_FONTE=os.path.join(
    os.path.dirname(__file__),
    "..",
    "assets",
    "fonts",
    "game_over.ttf"
)

# Fontes utilizadas na interface
fonte=pygame.font.SysFont("Arial",46)
fonte_game_over_borda=pygame.font.Font(CAMINHO_FONTE,310)
fonte_game_over=pygame.font.Font(CAMINHO_FONTE,300)
fonte_titulo=pygame.font.Font(CAMINHO_FONTE,200)
fonte_pontuacao_final=pygame.font.Font(CAMINHO_FONTE,100)
fonte_feedback=pygame.font.SysFont("Arial",30)

# CARREGAMENTO DO FUNDO
CAMINHO_FUNDO=os.path.join(
    os.path.dirname(__file__),
    "..",
    "assets",
    "images",
    "fundo.jpg"
)

fundo=pygame.image.load(CAMINHO_FUNDO).convert()

# Ajusta o fundo para preencher toda a janela
fundo=pygame.transform.scale(fundo,(LARGURA,ALTURA))

# IMAGEM DE FUNDO DO GAME OVER
CAMINHO_FUNDO2=os.path.join(
    os.path.dirname(__file__),
    "..",
    "assets",
    "images",
    "fundo2.jpg"
)

fundo2=pygame.image.load(CAMINHO_FUNDO2).convert()

# Ajusta a imagem para o tamanho da janela
fundo2=pygame.transform.scale(fundo2,(LARGURA,ALTURA))

# CARREGAMENTO DOS CORAÇÕES
CAMINHO_CORACAO=os.path.join(
    os.path.dirname(__file__),
    "..",
    "assets",
    "images",
    "sprite_coração"
)

coracao_cheio=pygame.image.load(
    os.path.join(CAMINHO_CORACAO,"Heart_Full_64.png")
).convert_alpha()

coracao_vazio=pygame.image.load(
    os.path.join(CAMINHO_CORACAO,"Heart_Empty_64.png")
).convert_alpha()

# CONTEÚDO DA TELA INICIAL
instrucoes=[
    "Passe o mouse sobre as frutas para cortá-las.",
    "Cada fruta cortada vale 1 ponto.",
    "Voce tem 3 vidas: perde uma a cada fruta que cair.",
    "Evite as bombas: tocar nelas encerra a partida."
]

# ESTADO GERAL DO PROGRAMA
# Mantém a janela e o loop principal em execução
rodando=True

# Controla se o jogador ainda está na tela de instruções
tela_inicial=True

# RASTRO DO MOUSE
# Armazena posição e momento dos últimos movimentos do mouse
rastro_mouse=[]

# Tempo que cada trecho do rastro permanece visível (ms)
DURACAO_RASTRO=300

# LOOP PRINCIPAL DO JOGO
while rodando:

    # Guarda o pedido de início ou reinício até terminar
    # o processamento dos eventos deste quadro
    iniciar_solicitado=False

    # PROCESSAMENTO DE EVENTOS
    for evento in pygame.event.get():

        # Fecha o jogo
        if evento.type==pygame.QUIT:
            rodando=False

        # ENTER inicia a primeira partida
        # R inicia uma nova partida após o Game Over
        if evento.type==pygame.KEYDOWN:

            if tela_inicial and evento.key==pygame.K_RETURN:
                iniciar_solicitado=True

            elif not tela_inicial and jogo.game_over and evento.key==pygame.K_r:
                iniciar_solicitado=True

        # GERAÇÃO DAS BOMBAS
        # Não gera bombas na tela inicial, após o Game Over
        # ou durante a sequência de explosão
        if evento.type==EVENTO_BOMBA and not tela_inicial and not jogo.game_over and not bomba_explodiu:

            x=random.randint(200,LARGURA-200)

            bomba=Bomba(x,ALTURA+30)
            bombas.append(bomba)

            # Sorteia quando a próxima bomba será lançada
            proximo_tempo=random.randint(
                TEMPO_BOMBA_MIN,
                TEMPO_BOMBA_MAX
            )

            pygame.time.set_timer(
                EVENTO_BOMBA,
                proximo_tempo,
                loops=1
            )

        # MOVIMENTO DO MOUSE E DETECÇÃO DE CORTE

        # O mouse deixa de interagir com objetos durante
        # a tela inicial, Game Over ou sequência de explosão
        if evento.type==pygame.MOUSEMOTION and not tela_inicial and not jogo.game_over and not bomba_explodiu:

            # Guarda posição e momento para formar o rastro
            rastro_mouse.append(
                (evento.pos,pygame.time.get_ticks())
            )

            # COLISÃO COM FRUTAS
            for fruta in frutas[:]:

                # Uma fruta só pode ser cortada uma vez
                if fruta.verificar_corte(evento.pos) and not fruta.cortada:

                    fruta.cortar()

                    # Cada fruta cortada vale 1 ponto
                    jogo.adicionar_pontos(1)

                    # Cria o "+1" na posição da fruta
                    feedbacks_pontos.append({
                        "x": fruta.x,
                        "y": fruta.y,
                        "inicio": pygame.time.get_ticks()
                    })

                    # Chance de causar uma tremida ao cortar a fruta
                    if random.random() < CHANCE_TREMIDA:
                        tremendo=True
                        inicio_tremida=pygame.time.get_ticks()

                        intensidade_atual=INTENSIDADE_TREMIDA
                        duracao_atual=DURACAO_TREMIDA

            # COLISÃO COM BOMBAS
            for bomba in bombas[:]:

                if bomba.verificar_colisao(evento.pos):

                    # Tremida forte causada pela explosão
                    tremendo=True
                    inicio_tremida=pygame.time.get_ticks()

                    intensidade_atual=INTENSIDADE_TREMIDA_BOMBA
                    duracao_atual=DURACAO_TREMIDA_BOMBA

                    # Inicia o estado de explosão
                    bomba_explodiu=True
                    momento_explosao=pygame.time.get_ticks()

                    # Explosão principal na posição da bomba
                    explosao=Explosao(bomba.x,bomba.y)
                    explosoes.append(explosao)

                    # Explosões adicionais espalhadas pela tela
                    for i in range(15):

                        x=random.randint(100,LARGURA-100)
                        y=random.randint(100,ALTURA-100)

                        explosao=Explosao(x,y)
                        explosoes.append(explosao)

                    # Remove a bomba atingida
                    bombas.remove(bomba)

                    break

        # GERAÇÃO DAS FRUTAS

        # Não gera frutas na tela inicial, após o Game Over
        # ou durante a sequência de explosão
        if evento.type==EVENTO_FRUTA and not tela_inicial and not jogo.game_over and not bomba_explodiu:

            # Sorteia a posição horizontal
            x=random.randint(200,LARGURA-200)

            # Cria a fruta abaixo da tela
            fruta=Fruta(x,ALTURA+30)

            # Adiciona a fruta à partida
            frutas.append(fruta)

            # DIFICULDADE PROGRESSIVA

            # Reduz o intervalo máximo entre frutas
            # conforme a pontuação aumenta
            if jogo.pontuacao>50:
                tempo_max_fruta=400

            elif jogo.pontuacao>=50:
                tempo_max_fruta=700

            elif jogo.pontuacao>=30:
                tempo_max_fruta=800

            elif jogo.pontuacao>=20:
                tempo_max_fruta=1000

            elif jogo.pontuacao>=10:
                tempo_max_fruta=1200

            else:
                tempo_max_fruta=TEMPO_MAX

            # Sorteia o intervalo até a próxima fruta
            proximo_tempo=random.randint(
                TEMPO_MIN,
                tempo_max_fruta
            )

            # Agenda o próximo lançamento
            pygame.time.set_timer(
                EVENTO_FRUTA,
                proximo_tempo,
                loops=1
            )

    # INÍCIO OU REINÍCIO DA PARTIDA
    if iniciar_solicitado and rodando:

        # Cancela os temporizadores da partida anterior
        pygame.time.set_timer(EVENTO_FRUTA,0)
        pygame.time.set_timer(EVENTO_BOMBA,0)

        # Remove eventos antigos que ainda estejam na fila
        pygame.event.clear([
            EVENTO_FRUTA,
            EVENTO_BOMBA
        ])

        # Limpa os objetos da partida anterior
        frutas.clear()
        bombas.clear()
        explosoes.clear()
        feedbacks_pontos.clear()

        # Restaura o estado da explosão
        bomba_explodiu=False
        momento_explosao=0

        # Restaura pontuação, vidas e Game Over
        jogo.reiniciar()

        # Sai da tela inicial
        tela_inicial=False

        # Agenda o primeiro lançamento de fruta
        pygame.time.set_timer(
            EVENTO_FRUTA,
            random.randint(TEMPO_MIN,TEMPO_MAX),
            loops=1
        )

        # Agenda o primeiro lançamento de bomba
        pygame.time.set_timer(
            EVENTO_BOMBA,
            random.randint(TEMPO_BOMBA_MIN,TEMPO_BOMBA_MAX),
            loops=1
        )

    # ATUALIZAÇÃO DA TREMIDA
    offset_x=0
    offset_y=0

    if tremendo:
        tempo_tremida=pygame.time.get_ticks()-inicio_tremida

        if tempo_tremida < duracao_atual:
            offset_x=random.randint(-intensidade_atual,intensidade_atual)
            offset_y=random.randint(-intensidade_atual,intensidade_atual)

        else:
            tremendo=False

    # ATUALIZAÇÃO DO RASTRO DO MOUSE
    agora=pygame.time.get_ticks()

    # Mantém somente os pontos que ainda estão dentro
    # do tempo de duração do rastro
    rastro_mouse=[
        ponto for ponto in rastro_mouse
        if agora-ponto[1] < DURACAO_RASTRO
    ]

    # DESENHO DO FUNDO
    if jogo.game_over:
        tela.blit(fundo2,(0,0))
    else:
        tela.blit(fundo,(offset_x,offset_y))

    # DESENHO DO RASTRO DO MOUSE
    if len(rastro_mouse)>1 and not tela_inicial and not jogo.game_over:

        for i in range(1,len(rastro_mouse)):

            posicao_anterior=rastro_mouse[i-1][0]
            posicao_atual=rastro_mouse[i][0]

            idade=agora-rastro_mouse[i][1]

            # O trecho fica mais escuro conforme envelhece
            intensidade=max(
                0,
                255-int(255*(idade/DURACAO_RASTRO))
            )

            # O início do rastro é fino e a ponta mais grossa
            espessura=max(
                2,
                int(12*(i/len(rastro_mouse)))
            )

            pygame.draw.line(
                tela,
                (intensidade,intensidade,intensidade),
                posicao_anterior,
                posicao_atual,
                espessura
            )

    # FEEDBACK VISUAL DA PONTUAÇÃO
    agora=pygame.time.get_ticks()

    for feedback in feedbacks_pontos[:]:

        tempo_passado=agora-feedback["inicio"]

        # Remove o "+1" após 700 ms
        if tempo_passado>=700:
            feedbacks_pontos.remove(feedback)
            continue

        # Faz o "+1" subir gradualmente
        y=feedback["y"]-(tempo_passado*0.05)

        texto_feedback=fonte_feedback.render(
            "+1",
            True,
            (255,255,255)
        )

        tela.blit(
            texto_feedback,
            texto_feedback.get_rect(
                center=(int(feedback["x"]),int(y))
            )
        )

    # ATUALIZAÇÃO DOS OBJETOS
    if not tela_inicial and not jogo.game_over:

        # Durante a explosão, frutas e bombas ficam congeladas
        if not bomba_explodiu:

            # ATUALIZAÇÃO DAS FRUTAS
            for fruta in frutas[:]:

                fruta.atualizar()

                # Remove a fruta quando ela sai pela parte inferior
                if fruta.y-fruta.raio > ALTURA:

                    frutas.remove(fruta)

                    # Frutas não cortadas retiram uma vida
                    if not fruta.cortada:
                        jogo.perder_vida()

                    # Interrompe caso a última vida tenha sido perdida
                    if jogo.game_over:
                        break

            # ATUALIZAÇÃO DAS BOMBAS
            if not jogo.game_over:

                for bomba in bombas[:]:

                    bomba.atualizar()

                    # Bombas que saem da tela apenas desaparecem
                    if bomba.y-bomba.raio > ALTURA:
                        bombas.remove(bomba)

        # ATUALIZAÇÃO DAS EXPLOSÕES

        # As explosões continuam animando enquanto
        # frutas e bombas permanecem congeladas
        for explosao in explosoes[:]:

            explosao.atualizar()

            if explosao.finalizada:
                explosoes.remove(explosao)

        # GAME OVER APÓS EXPLOSÃO
        if bomba_explodiu:

            tempo_passado=pygame.time.get_ticks()-momento_explosao

            # Finaliza quando todas as explosões terminam
            # ou quando o tempo máximo é atingido
            if len(explosoes)==0 or tempo_passado>=DURACAO_MAX_EXPLOSAO:

                explosoes.clear()
                rastro_mouse.clear()
                jogo.game_over=True

    # DESENHO DOS OBJETOS

    # Mantém os objetos visíveis após o Game Over,
    # deixando a última cena congelada
    if not tela_inicial:

        for fruta in frutas:
            fruta.desenhar(tela)

        for bomba in bombas:
            bomba.desenhar(tela)

        for explosao in explosoes:
            explosao.desenhar(tela)

    # TELA INICIAL
    if tela_inicial:

        # Painel escuro para facilitar a leitura
        pygame.draw.rect(
            tela,
            (30,30,30),
            (140,110,1000,480)
        )

        # Título
        texto_titulo=fonte_titulo.render(
            NOME_DO_JOGO,
            True,
            (255,255,255)
        )

        tela.blit(
            texto_titulo,
            texto_titulo.get_rect(
                center=(LARGURA//2,180)
            )
        )

        # Instruções
        y_instrucao=290

        for instrucao in instrucoes:

            texto_instrucao=fonte_pontuacao_final.render(
                instrucao,
                True,
                (255,255,255)
            )

            tela.blit(
                texto_instrucao,
                texto_instrucao.get_rect(
                    center=(LARGURA//2,y_instrucao)
                )
            )

            y_instrucao+=45

        # Comando para iniciar
        texto_iniciar=fonte_pontuacao_final.render(
            "Pressione ENTER para jogar",
            True,
            (120,230,120)
        )

        tela.blit(
            texto_iniciar,
            texto_iniciar.get_rect(
                center=(LARGURA//2,520)
            )
        )

    # INTERFACE DURANTE A PARTIDA
    elif not jogo.game_over:

        # Pontuação
        texto_pontos=fonte.render(
            f"{jogo.pontuacao}",
            True,
            (255,255,255)
        )

        tela.blit(
            texto_pontos,
            (100,60)
        )

        # Vidas
        for i in range(3):

            x=1040+(i*70)
            y=50

            if i < jogo.vidas:
                tela.blit(coracao_cheio,(x,y))

            else:
                tela.blit(coracao_vazio,(x,y))

    # TELA DE GAME OVER
    else:

        # Texto maior usado como borda
        texto_game_over_borda=fonte_game_over_borda.render(
            "GAME OVER",
            True,
            (0,0,0)
        )

        # Texto principal
        texto_game_over=fonte_game_over.render(
            "GAME OVER",
            True,
            (255,0,0)
        )

        # Pontuação final
        texto_final=fonte_pontuacao_final.render(
            f"PONTUAÇAO FINAL: {jogo.pontuacao}",
            True,
            (255,255,255)
        )

        # Comando para reiniciar
        texto_reiniciar=fonte_pontuacao_final.render(
            "Pressione R para jogar novamente",
            True,
            (255,255,255)
        )

        # Desenha primeiro a borda
        tela.blit(
            texto_game_over_borda,
            texto_game_over_borda.get_rect(
                center=(LARGURA//2,250)
            )
        )

        tela.blit(
            texto_game_over,
            texto_game_over.get_rect(
                center=(LARGURA//2,250)
            )
        )

        tela.blit(
            texto_final,
            texto_final.get_rect(
                center=(LARGURA//2,350)
            )
        )

        tela.blit(
            texto_reiniciar,
            texto_reiniciar.get_rect(
                center=(LARGURA//2,650)
            )
        )

    # ATUALIZAÇÃO DA JANELA
    pygame.display.flip()

    # Limita o jogo a aproximadamente 60 FPS
    clock.tick(60)

# ENCERRAMENTO
pygame.quit()
