# ============================================================
# IMPORTAÇÃO DAS BIBLIOTECAS
# ============================================================

import pygame
import random
import os

# Importa as classes do jogo
from fruta import Fruta
from jogo import Jogo
from bomba import Bomba
from explosao import Explosao

# Sons e música
from sons import Sons
from musica import Musica

# Ranking
from ranking import salvar_pontuacao


# ============================================================
# CONFIGURAÇÃO E INICIALIZAÇÃO
# ============================================================

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()

sons=Sons()
musica=Musica()
jogo=Jogo()


# ============================================================
# CONFIGURAÇÕES DA JANELA
# ============================================================

LARGURA=1280
ALTURA=720
NOME_DO_JOGO="Jogo das Frutas"

tela=pygame.display.set_mode((LARGURA,ALTURA))
pygame.display.set_caption(NOME_DO_JOGO)

# Controla o modo de exibição
tela_cheia=False

clock=pygame.time.Clock()


# ============================================================
# TREMIDA DA TELA
# ============================================================

tremendo=False
inicio_tremida=0

DURACAO_TREMIDA=200
INTENSIDADE_TREMIDA=8
CHANCE_TREMIDA=0.30

DURACAO_TREMIDA_BOMBA=800
INTENSIDADE_TREMIDA_BOMBA=15

intensidade_atual=INTENSIDADE_TREMIDA
duracao_atual=DURACAO_TREMIDA


# ============================================================
# OBJETOS DO JOGO
# ============================================================

frutas=[]
bombas=[]
explosoes=[]
feedbacks_pontos=[]

bomba_explodiu=False

momento_explosao=0
DURACAO_MAX_EXPLOSAO=2000


# ============================================================
# EVENTOS E TEMPORIZADORES
# ============================================================

EVENTO_FRUTA=pygame.USEREVENT+1
EVENTO_BOMBA=pygame.USEREVENT+2

TEMPO_MIN=300
TEMPO_MAX=1500

TEMPO_BOMBA_MIN=3000
TEMPO_BOMBA_MAX=6000


# ============================================================
# FONTES
# ============================================================

CAMINHO_FONTE=os.path.join(
    os.path.dirname(__file__),
    "..",
    "assets",
    "fonts",
    "game_over.ttf"
)

# Todos os textos utilizam a mesma fonte
fonte=pygame.font.Font(CAMINHO_FONTE,80)
fonte_game_over_borda=pygame.font.Font(CAMINHO_FONTE,310)
fonte_game_over=pygame.font.Font(CAMINHO_FONTE,300)
fonte_titulo=pygame.font.Font(CAMINHO_FONTE,200)
fonte_pontuacao_final=pygame.font.Font(CAMINHO_FONTE,100)
fonte_feedback=pygame.font.Font(CAMINHO_FONTE,55)
fonte_nome=pygame.font.Font(CAMINHO_FONTE,100)
fonte_instrucoes=pygame.font.Font(CAMINHO_FONTE,65)


# ============================================================
# FUNDOS
# ============================================================

CAMINHO_FUNDO=os.path.join(
    os.path.dirname(__file__),
    "..",
    "assets",
    "images",
    "fundo.jpg"
)

fundo=pygame.image.load(CAMINHO_FUNDO).convert()
fundo=pygame.transform.scale(
    fundo,
    (LARGURA,ALTURA)
)

CAMINHO_FUNDO2=os.path.join(
    os.path.dirname(__file__),
    "..",
    "assets",
    "images",
    "fundo2.jpg"
)

fundo2=pygame.image.load(CAMINHO_FUNDO2).convert()
fundo2=pygame.transform.scale(
    fundo2,
    (LARGURA,ALTURA)
)


# ============================================================
# CORAÇÕES
# ============================================================

CAMINHO_CORACAO=os.path.join(
    os.path.dirname(__file__),
    "..",
    "assets",
    "images",
    "sprite_coração"
)

coracao_cheio=pygame.image.load(
    os.path.join(
        CAMINHO_CORACAO,
        "Heart_Full_64.png"
    )
).convert_alpha()

coracao_vazio=pygame.image.load(
    os.path.join(
        CAMINHO_CORACAO,
        "Heart_Empty_64.png"
    )
).convert_alpha()


# ============================================================
# TELA INICIAL
# ============================================================

instrucoes=[
    "Passe o mouse sobre as frutas para corta-las.",
    "Cada fruta cortada vale 1 ponto.",
    "Voce tem 3 vidas: perde uma a cada fruta que cair.",
    "Evite as bombas: tocar nelas encerra a partida."
]


# ============================================================
# ESTADOS DO PROGRAMA
# ============================================================

rodando=True

# Começa no menu
tela_inicial=True

# Tela utilizada para digitar o nome
tela_nome=False

# Jogador atual
nome_jogador=""
nome_digitado=""


# ============================================================
# RASTRO DO MOUSE
# ============================================================

rastro_mouse=[]
DURACAO_RASTRO=300


# ============================================================
# LOOP PRINCIPAL
# ============================================================

while rodando:

    iniciar_solicitado=False

    # Guarda o estado anterior para detectar o momento
    # exato em que ocorre o Game Over
    game_over_anterior=jogo.game_over


    # ========================================================
    # PROCESSAMENTO DE EVENTOS
    # ========================================================

    for evento in pygame.event.get():

        # Fecha a janela
        if evento.type==pygame.QUIT:
            rodando=False


        # ====================================================
        # TECLADO
        # ====================================================

        if evento.type==pygame.KEYDOWN:

            # ------------------------------------------------
            # TELA CHEIA
            # ------------------------------------------------

            # F11 alterna entre tela cheia e modo janela
            if evento.key==pygame.K_F11:

                tela_cheia=not tela_cheia

                if tela_cheia:

                    tela=pygame.display.set_mode(
                        (LARGURA,ALTURA),
                        pygame.FULLSCREEN
                    )

                else:

                    tela=pygame.display.set_mode(
                        (LARGURA,ALTURA)
                    )


            # ------------------------------------------------
            # MENU
            # ------------------------------------------------

            elif tela_inicial:

                # ENTER abre a tela de escolha do nome
                if evento.key==pygame.K_RETURN:

                    tela_inicial=False
                    tela_nome=True

                    # Sempre começa vazio para permitir
                    # escolher outro jogador
                    nome_digitado=""


            # ------------------------------------------------
            # ESCOLHA DO NOME
            # ------------------------------------------------

            elif tela_nome:

                # ENTER confirma o nome
                if evento.key==pygame.K_RETURN:

                    if nome_digitado.strip()!="":

                        nome_jogador=nome_digitado.strip()

                        tela_nome=False
                        iniciar_solicitado=True

                # ESC volta ao menu
                elif evento.key==pygame.K_ESCAPE:

                    tela_nome=False
                    tela_inicial=True
                    nome_digitado=""

                # BACKSPACE apaga o último caractere
                elif evento.key==pygame.K_BACKSPACE:

                    nome_digitado=nome_digitado[:-1]

                # Adiciona os caracteres digitados
                else:

                    if len(nome_digitado)<15:
                        nome_digitado+=evento.unicode


            # ------------------------------------------------
            # GAME OVER
            # ------------------------------------------------

            elif jogo.game_over:

                # R começa outra partida com o mesmo jogador
                if evento.key==pygame.K_r:

                    iniciar_solicitado=True

                # ESC volta para o menu
                elif evento.key==pygame.K_ESCAPE:

                    sons.parar()
                    musica.parar()

                    pygame.time.set_timer(
                        EVENTO_FRUTA,
                        0
                    )

                    pygame.time.set_timer(
                        EVENTO_BOMBA,
                        0
                    )

                    pygame.event.clear([
                        EVENTO_FRUTA,
                        EVENTO_BOMBA
                    ])

                    frutas.clear()
                    bombas.clear()
                    explosoes.clear()
                    feedbacks_pontos.clear()
                    rastro_mouse.clear()

                    tremendo=False
                    inicio_tremida=0

                    bomba_explodiu=False
                    momento_explosao=0

                    jogo.reiniciar()

                    tela_inicial=True
                    tela_nome=False


        # ====================================================
        # GERAÇÃO DAS BOMBAS
        # ====================================================

        if (
            evento.type==EVENTO_BOMBA
            and not tela_inicial
            and not tela_nome
            and not jogo.game_over
            and not bomba_explodiu
        ):

            x=random.randint(
                200,
                LARGURA-200
            )

            bomba=Bomba(
                x,
                ALTURA+30
            )

            bombas.append(bomba)

            # Inicia o pavio
            sons.iniciar_pavio()

            proximo_tempo=random.randint(
                TEMPO_BOMBA_MIN,
                TEMPO_BOMBA_MAX
            )

            pygame.time.set_timer(
                EVENTO_BOMBA,
                proximo_tempo,
                loops=1
            )


        # ====================================================
        # MOVIMENTO DO MOUSE
        # ====================================================

        if (
            evento.type==pygame.MOUSEMOTION
            and not tela_inicial
            and not tela_nome
            and not jogo.game_over
            and not bomba_explodiu
        ):

            # Guarda o movimento para formar o rastro
            rastro_mouse.append(
                (
                    evento.pos,
                    pygame.time.get_ticks()
                )
            )


            # ------------------------------------------------
            # FRUTAS
            # ------------------------------------------------

            for fruta in frutas[:]:

                if (
                    fruta.verificar_corte(evento.pos)
                    and not fruta.cortada
                ):

                    fruta.cortar()

                    jogo.adicionar_pontos(1)

                    sons.tocar("corte")

                    # Feedback "+1"
                    feedbacks_pontos.append({
                        "x": fruta.x,
                        "y": fruta.y,
                        "inicio": pygame.time.get_ticks()
                    })

                    # Chance de tremida
                    if random.random()<CHANCE_TREMIDA:

                        tremendo=True

                        inicio_tremida=pygame.time.get_ticks()

                        intensidade_atual=INTENSIDADE_TREMIDA
                        duracao_atual=DURACAO_TREMIDA


            # ------------------------------------------------
            # BOMBAS
            # ------------------------------------------------

            for bomba in bombas[:]:

                if bomba.verificar_colisao(evento.pos):

                    # Tremida forte
                    tremendo=True

                    inicio_tremida=pygame.time.get_ticks()

                    intensidade_atual=INTENSIDADE_TREMIDA_BOMBA
                    duracao_atual=DURACAO_TREMIDA_BOMBA

                    # Inicia a sequência de explosão
                    bomba_explodiu=True

                    momento_explosao=pygame.time.get_ticks()

                    musica.parar()
                    sons.parar_pavio()
                    sons.tocar("explosao")

                    # Explosão principal
                    explosao=Explosao(
                        bomba.x,
                        bomba.y
                    )

                    explosoes.append(explosao)

                    # Explosões adicionais
                    for i in range(15):

                        x=random.randint(
                            100,
                            LARGURA-100
                        )

                        y=random.randint(
                            100,
                            ALTURA-100
                        )

                        explosao=Explosao(x,y)
                        explosoes.append(explosao)

                    bombas.remove(bomba)

                    break


        # ====================================================
        # GERAÇÃO DAS FRUTAS
        # ====================================================

        if (
            evento.type==EVENTO_FRUTA
            and not tela_inicial
            and not tela_nome
            and not jogo.game_over
            and not bomba_explodiu
        ):

            x=random.randint(
                200,
                LARGURA-200
            )

            fruta=Fruta(
                x,
                ALTURA+30
            )

            frutas.append(fruta)


            # ------------------------------------------------
            # DIFICULDADE PROGRESSIVA
            # ------------------------------------------------

            if jogo.pontuacao>=100:
                tempo_max_fruta=350

            elif jogo.pontuacao>=80:
                tempo_max_fruta=400

            elif jogo.pontuacao>=60:
                tempo_max_fruta=500

            elif jogo.pontuacao>=50:
                tempo_max_fruta=600

            elif jogo.pontuacao>=40:
                tempo_max_fruta=700

            elif jogo.pontuacao>=30:
                tempo_max_fruta=800

            elif jogo.pontuacao>=20:
                tempo_max_fruta=1000

            elif jogo.pontuacao>=10:
                tempo_max_fruta=1200

            else:
                tempo_max_fruta=TEMPO_MAX


            proximo_tempo=random.randint(
                TEMPO_MIN,
                tempo_max_fruta
            )

            pygame.time.set_timer(
                EVENTO_FRUTA,
                proximo_tempo,
                loops=1
            )


    # ========================================================
    # INÍCIO OU REINÍCIO DA PARTIDA
    # ========================================================

    if iniciar_solicitado and rodando:

        # Interrompe efeitos anteriores
        sons.parar()

        # Inicia a música novamente
        musica.iniciar()

        # Cancela timers antigos
        pygame.time.set_timer(
            EVENTO_FRUTA,
            0
        )

        pygame.time.set_timer(
            EVENTO_BOMBA,
            0
        )

        pygame.event.clear([
            EVENTO_FRUTA,
            EVENTO_BOMBA
        ])

        # Limpa a partida anterior
        frutas.clear()
        bombas.clear()
        explosoes.clear()
        feedbacks_pontos.clear()
        rastro_mouse.clear()

        tremendo=False
        inicio_tremida=0

        bomba_explodiu=False
        momento_explosao=0

        # Reseta pontuação, vidas e Game Over
        jogo.reiniciar()

        # Garante que estamos dentro da partida
        tela_inicial=False
        tela_nome=False

        # Agenda primeira fruta
        pygame.time.set_timer(
            EVENTO_FRUTA,
            random.randint(
                TEMPO_MIN,
                TEMPO_MAX
            ),
            loops=1
        )

        # Agenda primeira bomba
        pygame.time.set_timer(
            EVENTO_BOMBA,
            random.randint(
                TEMPO_BOMBA_MIN,
                TEMPO_BOMBA_MAX
            ),
            loops=1
        )


    # ========================================================
    # TREMIDA DA TELA
    # ========================================================

    offset_x=0
    offset_y=0

    if tremendo:

        tempo_tremida=(
            pygame.time.get_ticks()
            -inicio_tremida
        )

        if tempo_tremida<duracao_atual:

            offset_x=random.randint(
                -intensidade_atual,
                intensidade_atual
            )

            offset_y=random.randint(
                -intensidade_atual,
                intensidade_atual
            )

        else:
            tremendo=False


    # ========================================================
    # RASTRO DO MOUSE
    # ========================================================

    agora=pygame.time.get_ticks()

    rastro_mouse=[
        ponto
        for ponto in rastro_mouse
        if agora-ponto[1]<DURACAO_RASTRO
    ]


    # ========================================================
    # FUNDO
    # ========================================================

    if jogo.game_over:

        tela.blit(
            fundo2,
            (0,0)
        )

    else:

        tela.blit(
            fundo,
            (offset_x,offset_y)
        )


    # ========================================================
    # RASTRO VISUAL
    # ========================================================

    if (
        len(rastro_mouse)>1
        and not tela_inicial
        and not tela_nome
        and not jogo.game_over
    ):

        for i in range(
            1,
            len(rastro_mouse)
        ):

            posicao_anterior=rastro_mouse[i-1][0]
            posicao_atual=rastro_mouse[i][0]

            idade=agora-rastro_mouse[i][1]

            intensidade=max(
                0,
                255-int(
                    255*(
                        idade/DURACAO_RASTRO
                    )
                )
            )

            espessura=max(
                2,
                int(
                    12*(
                        i/len(rastro_mouse)
                    )
                )
            )

            pygame.draw.line(
                tela,
                (
                    intensidade,
                    intensidade,
                    intensidade
                ),
                posicao_anterior,
                posicao_atual,
                espessura
            )


    # ========================================================
    # FEEDBACK "+1"
    # ========================================================

    agora=pygame.time.get_ticks()

    for feedback in feedbacks_pontos[:]:

        tempo_passado=(
            agora
            -feedback["inicio"]
        )

        if tempo_passado>=700:

            feedbacks_pontos.remove(
                feedback
            )

            continue

        y=(
            feedback["y"]
            -(tempo_passado*0.05)
        )

        texto_feedback=fonte_feedback.render(
            "+1",
            True,
            (255,255,255)
        )

        tela.blit(
            texto_feedback,
            texto_feedback.get_rect(
                center=(
                    int(feedback["x"]),
                    int(y)
                )
            )
        )


    # ========================================================
    # ATUALIZAÇÃO DOS OBJETOS
    # ========================================================

    if (
        not tela_inicial
        and not tela_nome
        and not jogo.game_over
    ):

        # Frutas e bombas ficam congeladas durante explosões
        if not bomba_explodiu:


            # ------------------------------------------------
            # FRUTAS
            # ------------------------------------------------

            for fruta in frutas[:]:

                fruta.atualizar()

                if fruta.y-fruta.raio>ALTURA:

                    frutas.remove(fruta)

                    if not fruta.cortada:
                        jogo.perder_vida()

                    if jogo.game_over:
                        break


            # ------------------------------------------------
            # BOMBAS
            # ------------------------------------------------

            if not jogo.game_over:

                for bomba in bombas[:]:

                    bomba.atualizar()

                    if bomba.y-bomba.raio>ALTURA:

                        bombas.remove(bomba)

                        if len(bombas)==0:
                            sons.parar_pavio()


        # ----------------------------------------------------
        # EXPLOSÕES
        # ----------------------------------------------------

        for explosao in explosoes[:]:

            explosao.atualizar()

            if explosao.finalizada:
                explosoes.remove(explosao)


        # ----------------------------------------------------
        # GAME OVER PELA BOMBA
        # ----------------------------------------------------

        if bomba_explodiu:

            tempo_passado=(
                pygame.time.get_ticks()
                -momento_explosao
            )

            if (
                len(explosoes)==0
                or tempo_passado>=DURACAO_MAX_EXPLOSAO
            ):

                explosoes.clear()
                rastro_mouse.clear()

                jogo.game_over=True


    # ========================================================
    # NOVO GAME OVER
    # ========================================================

    if jogo.game_over and not game_over_anterior:

        musica.parar()
        sons.parar_pavio()
        sons.tocar("fim_de_jogo")

        # Salva exatamente uma vez por partida
        salvar_pontuacao(
            nome_jogador,
            jogo.pontuacao
        )


    # ========================================================
    # DESENHO DOS OBJETOS
    # ========================================================

    if not tela_inicial and not tela_nome:

        for fruta in frutas:
            fruta.desenhar(tela)

        for bomba in bombas:
            bomba.desenhar(tela)

        for explosao in explosoes:
            explosao.desenhar(tela)


    # ========================================================
    # MENU
    # ========================================================

    if tela_inicial:

        pygame.draw.rect(
            tela,
            (30,30,30),
            (140,110,1000,480)
        )

        texto_titulo=fonte_titulo.render(
            NOME_DO_JOGO,
            True,
            (255,255,255)
        )

        tela.blit(
            texto_titulo,
            texto_titulo.get_rect(
                center=(
                    LARGURA//2,
                    180
                )
            )
        )

        y_instrucao=290

        for instrucao in instrucoes:

            texto_instrucao=fonte_instrucoes.render(
                instrucao,
                True,
                (255,255,255)
            )

            tela.blit(
                texto_instrucao,
                texto_instrucao.get_rect(
                    center=(
                        LARGURA//2,
                        y_instrucao
                    )
                )
            )

            y_instrucao+=45

        texto_iniciar=fonte_instrucoes.render(
            "Pressione ENTER para jogar",
            True,
            (120,230,120)
        )

        tela.blit(
            texto_iniciar,
            texto_iniciar.get_rect(
                center=(
                    LARGURA//2,
                    520
                )
            )
        )


    # ========================================================
    # ESCOLHA DO NOME
    # ========================================================

    elif tela_nome:

        pygame.draw.rect(
            tela,
            (30,30,30),
            (290,180,700,360)
        )

        texto_nome=fonte_pontuacao_final.render(
            "DIGITE SEU NOME",
            True,
            (255,255,255)
        )

        tela.blit(
            texto_nome,
            texto_nome.get_rect(
                center=(
                    LARGURA//2,
                    260
                )
            )
        )

        # Exibe o que está sendo digitado
        texto_digitado=fonte_nome.render(
            nome_digitado,
            True,
            (255,255,255)
        )

        tela.blit(
            texto_digitado,
            texto_digitado.get_rect(
                center=(
                    LARGURA//2,
                    360
                )
            )
        )

        texto_confirmar=fonte_feedback.render(
            "ENTER para confirmar | ESC para voltar",
            True,
            (255,255,255)
        )

        tela.blit(
            texto_confirmar,
            texto_confirmar.get_rect(
                center=(
                    LARGURA//2,
                    460
                )
            )
        )


    # ========================================================
    # INTERFACE DA PARTIDA
    # ========================================================

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

            if i<jogo.vidas:

                tela.blit(
                    coracao_cheio,
                    (x,y)
                )

            else:

                tela.blit(
                    coracao_vazio,
                    (x,y)
                )


    # ========================================================
    # GAME OVER
    # ========================================================

    else:

        # Borda preta
        texto_game_over_borda=fonte_game_over_borda.render(
            "GAME OVER",
            True,
            (0,0,0)
        )

        # Texto principal vermelho
        texto_game_over=fonte_game_over.render(
            "GAME OVER",
            True,
            (255,0,0)
        )

        # Pontuação
        texto_final=fonte_pontuacao_final.render(
            f"PONTUAÇAO FINAL: {jogo.pontuacao}",
            True,
            (255,255,255)
        )

        # Jogador atual
        texto_jogador=fonte_feedback.render(
            f"JOGADOR: {nome_jogador}",
            True,
            (255,255,255)
        )

        # Comandos
        texto_reiniciar=fonte_instrucoes.render(
            "R: JOGAR NOVAMENTE | ESC: MENU",
            True,
            (255,255,255)
        )

        # Borda
        tela.blit(
            texto_game_over_borda,
            texto_game_over_borda.get_rect(
                center=(
                    LARGURA//2,
                    250
                )
            )
        )

        # GAME OVER
        tela.blit(
            texto_game_over,
            texto_game_over.get_rect(
                center=(
                    LARGURA//2,
                    250
                )
            )
        )

        # Pontuação final
        tela.blit(
            texto_final,
            texto_final.get_rect(
                center=(
                    LARGURA//2,
                    350
                )
            )
        )

        # Nome
        tela.blit(
            texto_jogador,
            texto_jogador.get_rect(
                center=(
                    LARGURA//2,
                    440
                )
            )
        )

        # Reiniciar/menu
        tela.blit(
            texto_reiniciar,
            texto_reiniciar.get_rect(
                center=(
                    LARGURA//2,
                    650
                )
            )
        )


    # ========================================================
    # ATUALIZAÇÃO DA JANELA
    # ========================================================

    pygame.display.flip()

    clock.tick(60)


# ============================================================
# ENCERRAMENTO
# ============================================================

pygame.quit()