# Otimização de imagens preparada com assistência de IA (ChatGPT).
# Este módulo compartilha imagens entre objetos, sem mudar a física ou os sons.

# lru_cache guarda resultados para reutilizar chamadas com os mesmos argumentos.
from functools import lru_cache

# pygame carrega as imagens, recorta as animações e ajusta seus tamanhos.
import pygame


# Guarda os originais das poucas imagens usadas pelas frutas, bombas e explosões.
# Repetir o mesmo caminho devolve a imagem existente, sem reler o arquivo.
@lru_cache(maxsize=None)
def carregar_imagem(caminho):
    """Carrega e converte uma imagem na primeira vez em que ela é solicitada."""
    # A primeira chamada ocorre após a criação da janela, permitindo convert_alpha.
    return pygame.image.load(caminho).convert_alpha()


# Reaproveita também os tamanhos já preparados, guardando até 128 combinações.
# Ao atingir esse limite, descarta a combinação que ficou mais tempo sem uso.
@lru_cache(maxsize=128)
def imagem_redimensionada(caminho, largura, altura):
    """Obtém uma imagem compartilhada no tamanho pedido, preservando o original."""
    # Buscar o original não provoca outra leitura se o arquivo já foi carregado.
    original = carregar_imagem(caminho)

    # scale cria outra Surface; o original continua disponível em seu tamanho real.
    return pygame.transform.scale(original, (largura, altura))


# Conserva o recorte das folhas de animação; o projeto usa uma folha de explosão.
# O limite permite reutilização sem guardar um número ilimitado de animações.
@lru_cache(maxsize=4)
def _quadros_originais(caminho, quantidade_frames):
    """Recorta uma folha de animação uma vez e compartilha seus quadros originais."""
    # A folha passa pelo mesmo carregador, que evita leituras repetidas do arquivo.
    spritesheet = carregar_imagem(caminho)

    # Cada quadro ocupa uma das partes de mesma largura na faixa horizontal.
    largura_frame = spritesheet.get_width() // quantidade_frames
    altura_frame = spritesheet.get_height()
    quadros = []

    # Os recortes referenciam a folha original, sem criar novas cópias de seus pixels.
    for numero in range(quantidade_frames):
        quadro = spritesheet.subsurface(
            numero * largura_frame, 0, largura_frame, altura_frame
        )
        quadros.append(quadro)

    # A tupla evita adicionar ou remover quadros de uma animação compartilhada.
    return tuple(quadros)


# Conserva somente oito tamanhos de explosão para limitar o uso de memória.
# Um tamanho descartado pode ser preparado novamente, sem reler a imagem do disco.
@lru_cache(maxsize=8)
def quadros_explosao(caminho, quantidade_frames, tamanho):
    """Obtém os quadros de uma explosão no tamanho pedido, com memória limitada."""
    # Reaproveita os recortes originais e redimensiona apenas em uma combinação nova.
    originais = _quadros_originais(caminho, quantidade_frames)
    quadros = []

    # Todos os objetos do mesmo tamanho podem desenhar estes mesmos quadros.
    for quadro in originais:
        quadros.append(pygame.transform.scale(quadro, (tamanho, tamanho)))

    # Somente as imagens são compartilhadas; posição, tempo e índice ficam no objeto.
    # As classes devem desenhar estas Surfaces sem modificar seus pixels ou seu alpha.
    return tuple(quadros)
