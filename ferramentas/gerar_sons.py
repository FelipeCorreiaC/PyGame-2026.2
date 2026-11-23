# Efeitos originais sintetizados para o Jogo das Frutas com assistência de IA.
# Este script usa apenas a biblioteca padrão do Python e não baixa sons prontos.
# Execute-o somente se quiser recriar os WAV; o jogo utiliza os arquivos já salvos.

# math fornece as ondas, random produz o ruído e wave grava o formato WAV.
import math
import random
import wave

# array transforma as amostras em inteiros de 16 bits; Path encontra as pastas.
from array import array
from pathlib import Path
import sys

# Todos os efeitos possuem um canal (mono) e 44.100 amostras por segundo.
TAXA = 44100

# A saída é relativa a este arquivo, funcionando mesmo em outro diretório atual.
PASTA_SONS = Path(__file__).resolve().parents[1] / "assets" / "sounds"


# Suaviza as extremidades, limita o volume e salva um efeito em PCM de 16 bits.
def salvar_wav(nome, amostras, pico):
    # Retira a componente contínua para manter o sinal centralizado em zero.
    media = sum(amostras) / len(amostras)
    amostras = [valor - media for valor in amostras]

    # As rampas de 8 ms suavizam o começo e o fim natural de cada arquivo.
    rampa = int(TAXA * 0.008)
    for i in range(rampa):
        ganho = i / (rampa - 1)
        amostras[i] *= ganho
        amostras[-1 - i] *= ganho

    # Normaliza para um pico moderado, abaixo do limite máximo permitido no WAV.
    maior = max(abs(valor) for valor in amostras)
    dados = array("h", (round(valor / maior * pico * 32767) for valor in amostras))

    # O WAV PCM guarda os inteiros no formato little-endian em qualquer sistema.
    if sys.byteorder != "little":
        dados.byteswap()

    # Cria a pasta se necessário e grava um canal com dois bytes por amostra.
    PASTA_SONS.mkdir(parents=True, exist_ok=True)
    with wave.open(str(PASTA_SONS / nome), "wb") as arquivo:
        arquivo.setnchannels(1)
        arquivo.setsampwidth(2)
        arquivo.setframerate(TAXA)
        arquivo.writeframes(dados.tobytes())


# Combina um sopro curto com uma pequena oscilação para sugerir um corte suculento.
def gerar_corte():
    # A semente fixa reproduz exatamente o mesmo efeito a cada execução.
    sorteio = random.Random(12)
    duracao = 0.19
    amostras = []
    filtrado = 0.0
    fase = 0.0

    # Calcula separadamente cada instante do efeito de corte.
    for i in range(round(TAXA * duracao)):
        tempo = i / TAXA
        progresso = tempo / duracao

        # Retirar o ruído suavizado destaca o sopro agudo do movimento da lâmina.
        ruido = sorteio.uniform(-1, 1)
        filtrado = 0.65 * filtrado + 0.35 * ruido
        sopro = ruido - filtrado

        # Uma oscilação descendente discreta acrescenta a sensação de fruta úmida.
        frequencia = 1100 * (0.24 ** progresso)
        fase += 2 * math.pi * frequencia / TAXA
        gota = math.sin(fase) + 0.3 * math.sin(2 * fase)

        # O som cresce rapidamente e desaparece antes do próximo corte.
        envoltoria = math.sin(math.pi * progresso) ** 0.85
        envoltoria *= math.exp(-3 * progresso)
        amostras.append(envoltoria * (0.75 * sopro + 0.22 * gota))

    # Salva um corte com 190 ms e pico máximo de 60% da escala digital.
    salvar_wav("corte.wav", amostras, 0.60)


# Mistura impacto, ruído e grave em queda para representar uma bomba de desenho.
def gerar_explosao():
    # A explosão é curta para não competir com a mensagem de encerramento.
    sorteio = random.Random(34)
    duracao = 0.80
    amostras = []
    filtrado = 0.0
    fase = 0.0

    # Produz um ataque forte seguido de uma cauda cada vez mais fraca.
    for i in range(round(TAXA * duracao)):
        tempo = i / TAXA
        ruido = sorteio.uniform(-1, 1)

        # A média móvel aproxima um ruído grave, semelhante a um pequeno estrondo.
        filtrado = 0.94 * filtrado + 0.06 * ruido
        frequencia = 38 + 40 * math.exp(-tempo / 0.10)
        fase += 2 * math.pi * frequencia / TAXA

        # O ruído agudo aparece só no início; o grave permanece durante a cauda.
        impacto = 0.40 * ruido * math.exp(-tempo / 0.07)
        grave = 1.3 * filtrado + 0.35 * math.sin(fase)
        envoltoria = (1 - math.exp(-tempo / 0.002)) * math.exp(-tempo / 0.15)
        amostras.append(envoltoria * (impacto + grave))

    # Salva 800 ms, com folga de volume para evitar saturação na reprodução.
    salvar_wav("explosao.wav", amostras, 0.72)


# Cria um sinal breve de derrota, com altura descendente; não é música de fundo.
def gerar_fim_de_jogo():
    # Uma única queda de frequência deixa o encerramento claro e discreto.
    duracao = 0.68
    amostras = []
    fase = 0.0

    # A oscilação começa mais aguda e perde altura até desaparecer.
    for i in range(round(TAXA * duracao)):
        tempo = i / TAXA
        progresso = tempo / duracao
        frequencia = 280 * (0.28 ** progresso)
        fase += 2 * math.pi * frequencia / TAXA

        # Harmônicos suaves dão ao aviso um timbre de jogo sem som estridente.
        onda = math.sin(fase) + 0.25 * math.sin(2 * fase)
        envoltoria = (1 - math.exp(-tempo / 0.012)) * (1 - progresso) ** 1.5
        amostras.append(envoltoria * onda)

    # O encerramento usa um volume menor do que a explosão.
    salvar_wav("fim_de_jogo.wav", amostras, 0.48)


# Executar o script cria os três efeitos; importá-lo não modifica arquivos.
if __name__ == "__main__":
    gerar_corte()
    gerar_explosao()
    gerar_fim_de_jogo()
    print("Efeitos criados em:", PASTA_SONS)
