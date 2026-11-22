# IMPORTAÇÃO DAS BIBLIOTECAS
import pygame
import random
import os

# Importa as classes
from fruta import Fruta
from jogo import Jogo
from bomba import Bomba
from explosao import Explosao

# Inicializa os módulos do Pygame
pygame.init()

# Objeto que representa o estado da partida
jogo = Jogo()

# Define as dimensões da janela
LARGURA=1280
ALTURA=720
NOME_DO_JOGO="Jogo das Frutas"

# LISTA DE FRUTAS
# Armazena todas as frutas ou bombas ativas na tela
frutas=[]
bombas=[]
explosoes=[]
bomba_explodiu=False
feedbacks_pontos=[]

# Momento (em ms) em que a bomba explodiu e tempo máximo permitido
# para a animação. Garante o game over mesmo que a explosão nunca termine.
momento_explosao=0
DURACAO_MAX_EXPLOSAO=2000

# CONFIGURAÇÃO DO TEMPORIZADOR
# Controla a geração aleatória das frutas e bombas.
# Evento personalizado para gerar frutas e bombas.
EVENTO_FRUTA=pygame.USEREVENT+1
EVENTO_BOMBA=pygame.USEREVENT+2

# Intervalo mínimo e máximo inicial (milissegundos) (frutas)
TEMPO_MIN=300
TEMPO_MAX=1500

# Intervalo mínimo e máximo (milissegundos) (bombas)
TEMPO_BOMBA_MIN=3000
TEMPO_BOMBA_MAX=6000

# Os primeiros lançamentos serão agendados somente ao iniciar com Enter

# CONFIGURAÇÃO DA JANELA
# Cria a janela do jogo
tela=pygame.display.set_mode((LARGURA,ALTURA))

CAMINHO_FONTE=os.path.join(
    os.path.dirname(__file__),
    "..",
    "assets",
    "fonts",
    "game_over.ttf"
)

fonte_game_over=pygame.font.Font(CAMINHO_FONTE,200)
fonte_pontuacao_final=pygame.font.Font(CAMINHO_FONTE,100)

# IMAGEM DE FUNDO
CAMINHO_FUNDO=os.path.join(
    os.path.dirname(__file__),
    "..",
    "assets",
    "images",
    "fundo.jpg"
)

fundo=pygame.image.load(CAMINHO_FUNDO).convert()

# Ajusta a imagem para o tamanho da janela
fundo=pygame.transform.scale(fundo,(LARGURA,ALTURA))

# IMAGENS DAS VIDAS
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

# Define o título
pygame.display.set_caption(NOME_DO_JOGO)

# Controla a taxa de atualização
clock=pygame.time.Clock()

# Fonte usada na interface (criada uma única vez)
fonte=pygame.font.SysFont("Arial",46)
fonte_game_over=pygame.font.Font(CAMINHO_FONTE,300)
fonte_titulo=pygame.font.Font(CAMINHO_FONTE,200)
fonte_instrucoes=pygame.font.SysFont("Arial",36)
fonte_feedback=pygame.font.SysFont("Arial",30)

instrucoes=[
    "Passe o mouse sobre as frutas para cortá-las.",
    "Cada fruta cortada vale 1 ponto.",
    "Voce tem 3 vidas: perde uma a cada fruta que cair.",
    "Evite as bombas: tocar nelas encerra a partida."
]

# Mantém o jogo em execução
rodando=True
# Mostra as instruções antes de começar a primeira partida
tela_inicial=True

# RASTRO DO MOUSE
rastro_mouse=[]
DURACAO_RASTRO=300

# LOOP PRINCIPAL DO JOGO
while rodando:

    # Guarda o pedido de início ou reinício até terminar os eventos deste quadro
    iniciar_solicitado=False

    # PROCESSAMENTO DE EVENTOS
    for evento in pygame.event.get():

        # Fecha o jogo
        if evento.type==pygame.QUIT:
            rodando=False

        # Enter inicia na tela inicial; R reinicia depois do game over
        if evento.type==pygame.KEYDOWN:
            if tela_inicial and evento.key==pygame.K_RETURN:
                iniciar_solicitado=True
            elif not tela_inicial and jogo.game_over and evento.key==pygame.K_r:
                iniciar_solicitado=True

        # Gera uma nova bomba (não gera mais após uma explosão)
        if evento.type==EVENTO_BOMBA and not tela_inicial and not jogo.game_over and not bomba_explodiu:

            x=random.randint(200,LARGURA-200)

            bomba=Bomba(x,ALTURA+30)
            bombas.append(bomba)

            proximo_tempo=random.randint(
                TEMPO_BOMBA_MIN,
                TEMPO_BOMBA_MAX
            )

            pygame.time.set_timer(
                EVENTO_BOMBA,
                proximo_tempo,
                loops=1
            )

        # DETECÇÃO DE CORTE COM O MOUSE
        # Bloqueada assim que uma bomba explode
        if evento.type==pygame.MOUSEMOTION and not tela_inicial and not jogo.game_over and not bomba_explodiu:

            # Adiciona a posição atual e o momento ao rastro do mouse
            rastro_mouse.append((evento.pos,pygame.time.get_ticks()))

            # Verifica se o mouse passou sobre alguma fruta
            for fruta in frutas[:]:

                if fruta.verificar_corte(evento.pos) and not fruta.cortada:

                    fruta.cortar()

                    # Adiciona 1 ponto pela fruta cortada
                    jogo.adicionar_pontos(1)

                    # Cria o feedback visual da pontuação
                    feedbacks_pontos.append({
                        "x": fruta.x,
                        "y": fruta.y,
                        "inicio": pygame.time.get_ticks()
                    })

            # Verifica as bombas
            for bomba in bombas[:]:

                if bomba.verificar_colisao(evento.pos):

                    # Indica que uma bomba foi atingida
                    bomba_explodiu=True
                    momento_explosao=pygame.time.get_ticks()

                    # Explosão principal na posição da bomba
                    explosao=Explosao(bomba.x,bomba.y)
                    explosoes.append(explosao)

                    # Cria explosões adicionais em posições aleatórias
                    for i in range(15):

                        x=random.randint(100,LARGURA-100)
                        y=random.randint(100,ALTURA-100)

                        explosao=Explosao(x,y)
                        explosoes.append(explosao)

                    # Remove a bomba
                    bombas.remove(bomba)

                    break

        # Gera uma nova fruta (não gera mais após uma explosão)
        if evento.type==EVENTO_FRUTA and not tela_inicial and not jogo.game_over and not bomba_explodiu:

            # Sorteia a posição horizontal
            x=random.randint(200,LARGURA-200)

            # Cria uma fruta abaixo da tela
            fruta=Fruta(x,ALTURA+30)

            # Adiciona à lista de frutas
            frutas.append(fruta)

            # Reduz a espera máxima conforme a pontuação, mantendo o mínimo
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

            # Aplica a dificuldade ao agendar a próxima fruta
            proximo_tempo=random.randint(TEMPO_MIN,tempo_max_fruta)

            # Agenda a próxima geração
            pygame.time.set_timer(
                EVENTO_FRUTA,
                proximo_tempo,
                loops=1
            )

    # INÍCIO OU REINÍCIO DA PARTIDA
    # Reutiliza a preparação para o Enter da tela inicial e o R do game over
    if iniciar_solicitado and rodando:

        # Cancela lançamentos da partida anterior e limpa os que estavam na fila
        pygame.time.set_timer(EVENTO_FRUTA,0)
        pygame.time.set_timer(EVENTO_BOMBA,0)
        pygame.event.clear([EVENTO_FRUTA,EVENTO_BOMBA])

        # Limpa todos os objetos da partida anterior
        frutas.clear()
        bombas.clear()
        explosoes.clear()
        feedbacks_pontos.clear()

        # Restaura o estado da explosão
        bomba_explodiu=False
        momento_explosao=0

        # Restaura pontuação, vidas e game over
        jogo.reiniciar()
        tela_inicial=False

        # Agenda um novo lançamento de cada tipo a partir deste momento
        pygame.time.set_timer(
            EVENTO_FRUTA,
            random.randint(TEMPO_MIN,TEMPO_MAX),
            loops=1
        )

        pygame.time.set_timer(
            EVENTO_BOMBA,
            random.randint(TEMPO_BOMBA_MIN,TEMPO_BOMBA_MAX),
            loops=1
        )

    # Remove pontos antigos do rastro
    agora=pygame.time.get_ticks()

    rastro_mouse=[
        ponto for ponto in rastro_mouse
        if agora-ponto[1] < DURACAO_RASTRO
    ]   

    # DESENHA O FUNDO
    tela.blit(fundo,(0,0))

    # DESENHA O RASTRO DO MOUSE
    if len(rastro_mouse) > 1 and not tela_inicial and not jogo.game_over:

        for i in range(1,len(rastro_mouse)):

            posicao_anterior=rastro_mouse[i-1][0]
            posicao_atual=rastro_mouse[i][0]

            idade=agora-rastro_mouse[i][1]

            # Quanto mais antigo, mais escuro
            intensidade=max(
                0,
                255-int(255*(idade/DURACAO_RASTRO))
            )

            # O início fica fino e a ponta fica mais grossa
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

        # Remove o feedback depois de 700 ms
        if tempo_passado >= 700:
            feedbacks_pontos.remove(feedback)
            continue

        # Faz o texto subir
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

        # Frutas e bombas só se movem se nenhuma bomba explodiu
        # (quando explode, a cena fica congelada e só as explosões animam)
        if not bomba_explodiu:

            # Percorre uma cópia para remover frutas com segurança
            for fruta in frutas[:]:

                fruta.atualizar()

                if fruta.y-fruta.raio > ALTURA:

                    frutas.remove(fruta)

                    # Só perde vida se a fruta não tiver sido cortada
                    if not fruta.cortada:
                        jogo.perder_vida()

                    # Interrompe o laço se esta era a última vida
                    if jogo.game_over:
                        break

            # A partida pode ter terminado durante a atualização das frutas
            if not jogo.game_over:

                for bomba in bombas[:]:

                    bomba.atualizar()

                    # Se a bomba cair, apenas remove
                    if bomba.y-bomba.raio > ALTURA:
                        bombas.remove(bomba)

        # ATUALIZAÇÃO DAS EXPLOSÕES
        # Continuam animando mesmo com o resto congelado
        for explosao in explosoes[:]:

            explosao.atualizar()

            if explosao.finalizada:
                explosoes.remove(explosao)

        # Game Over quando as explosões terminarem OU quando o tempo máximo passar
        if bomba_explodiu:

            tempo_passado=pygame.time.get_ticks()-momento_explosao

            if len(explosoes)==0 or tempo_passado>=DURACAO_MAX_EXPLOSAO:
                explosoes.clear()
                rastro_mouse.clear()
                jogo.game_over=True

    # DESENHO DOS OBJETOS
    # Continua desenhando após o game over para manter a cena parada
    if not tela_inicial:
        for fruta in frutas:
            fruta.desenhar(tela)

        for bomba in bombas:
            bomba.desenhar(tela)

        for explosao in explosoes:
            explosao.desenhar(tela)

    if tela_inicial:
        # Painel simples para facilitar a leitura sobre a imagem de fundo
        pygame.draw.rect(tela,(30,30,30),(140,110,1000,480))

        texto_titulo=fonte_titulo.render(NOME_DO_JOGO,True,(255,255,255))
        tela.blit(texto_titulo,texto_titulo.get_rect(center=(LARGURA//2,180)))

        y_instrucao=290
        for instrucao in instrucoes:
            texto_instrucao=fonte_pontuacao_final.render(instrucao,True,(255,255,255))
            tela.blit(texto_instrucao,texto_instrucao.get_rect(center=(LARGURA//2,y_instrucao)))
            y_instrucao+=45

        texto_iniciar=fonte_pontuacao_final.render("Pressione ENTER para jogar",True,(120,230,120))
        tela.blit(texto_iniciar,texto_iniciar.get_rect(center=(LARGURA//2,520)))

    elif not jogo.game_over:

        # EXIBIÇÃO DA PONTUAÇÃO
        texto_pontos=fonte.render(
            f"{jogo.pontuacao}",
            True,
            (255,255,255)
        )

        tela.blit(texto_pontos,(100,60))

        # EXIBIÇÃO DAS VIDAS
        for i in range(3):

            x=1040+(i*70)
            y=50

            if i < jogo.vidas:
                tela.blit(coracao_cheio,(x,y))
            else:
                tela.blit(coracao_vazio,(x,y))

    else:

        # Exibe apenas as informações de Game Over
        texto_game_over=fonte_game_over.render(
            "GAME OVER",
            True,
            (255,255,255)
        )

        texto_final=fonte_pontuacao_final.render(
            f"PONTUAÇAO FINAL: {jogo.pontuacao}",
            True,
            (255,255,255)
        )

        texto_reiniciar=fonte_pontuacao_final.render(
            "Pressione R para jogar novamente",
            True,
            (255,255,255)
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

    # Limita a aproximadamente 60 FPS
    clock.tick(60)

# ENCERRAMENTO
pygame.quit()
