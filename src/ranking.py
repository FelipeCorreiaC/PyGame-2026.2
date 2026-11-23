import os

# Caminho do arquivo de ranking
CAMINHO_RANKING=os.path.join(
    os.path.dirname(__file__),
    "..",
    "ranking.txt"
)


def salvar_pontuacao(nome,pontuacao):
    ranking=[]

    # Lê as pontuações que já existem
    if os.path.exists(CAMINHO_RANKING):

        with open(CAMINHO_RANKING,"r",encoding="utf-8") as arquivo:

            for linha in arquivo:
                linha=linha.strip()

                if linha:
                    nome_salvo,pontos=linha.rsplit(" - ",1)
                    ranking.append((nome_salvo,int(pontos)))

    # Adiciona a nova pontuação
    ranking.append((nome,pontuacao))

    # Ordena da maior pontuação para a menor
    ranking.sort(
        key=lambda jogador: jogador[1],
        reverse=True
    )

    # Salva novamente o ranking ordenado
    with open(CAMINHO_RANKING,"w",encoding="utf-8") as arquivo:

        for nome_salvo,pontos in ranking:
            arquivo.write(f"{nome_salvo} - {pontos}\n")