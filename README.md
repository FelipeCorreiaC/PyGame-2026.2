# Fruit Frenzy

Membros: Felipe Correia da Costa, Thiago Felipe Alves de Araujo, Giovane Bruscato Bortoluzzo

## Como rodar o jogo:

Para executar o jogo, é necessário ter o Python instalado no computador, juntamente com a biblioteca `pygame-ce`.

Após instalar as dependências descritas abaixo, execute o arquivo principal do projeto pelo terminal.

## Vídeo de apresentação do projeto:

[link]

## Descrição:

Fruit Frenzy é um jogo desenvolvido em Python utilizando a biblioteca Pygame, inspirado na mecânica de jogos como Fruit Ninja.

O objetivo do jogador é cortar as frutas que aparecem na tela utilizando o movimento do mouse, acumulando pontos e evitando deixar frutas caírem.

O jogador inicia a partida com três vidas. Sempre que uma fruta sai da tela sem ser cortada, uma vida é perdida. Além das frutas, bombas aparecem durante a partida e devem ser evitadas. Caso o jogador passe o mouse sobre uma bomba, a partida termina imediatamente.

O jogo também contará com um sistema de níveis, aumentando progressivamente a dificuldade da partida.

## Instalação de dependências:

Para instalar a biblioteca necessária para executar o jogo, utilize:

```bash
pip install pygame-ce
```

É possível verificar se a instalação foi realizada corretamente utilizando:

```bash
pip show pygame-ce
```

## Execução do programa:

Após clonar o repositório, acesse a pasta principal do projeto pelo terminal e execute:

```bash
python src/main.py
```

Uma janela do Pygame será aberta e o jogo será iniciado.