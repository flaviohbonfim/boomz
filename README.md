# BoomZ! — Outbreak Response

> Jogo de ação no estilo Bomberman com tema de apocalipse zumbi. Plante bombas, destrua inimigos e limpe a área.

---

## Sobre o Projeto

**BoomZ!** é um jogo de navegador completo, construído com [Kaboom.js](https://kaboomjs.com/), inspirado no clássico Bomberman. O jogador controla um sobrevivente num cenário urbano infestado de zumbis e precisa eliminar todos os inimigos usando bombas estrategicamente posicionadas.

O jogo roda inteiramente no navegador a partir de um único arquivo `index.html`, sem necessidade de build ou dependências instaladas além de um servidor HTTP local.

---

## Como Rodar Localmente

O jogo carrega assets (sprites, áudio) via requisições HTTP, por isso **não pode ser aberto diretamente pelo sistema de arquivos** (`file://`). É necessário servir a pasta com um servidor HTTP.

### Opção 1 — Python

```bash
python -m http.server 8000
```

Acesse `http://localhost:8000`.

### Opção 2 — Node.js

```bash
npx http-server -p 8080
```

Acesse `http://localhost:8080`.

### Opção 3 — PHP

```bash
php -S localhost:8000
```

Acesse `http://localhost:8000`.

Nenhum `npm install` ou build é necessário. Abra o endereço no navegador e o jogo inicia imediatamente.

---

## Controles

### Teclado (desktop)

| Ação                  | Teclas                       |
|-----------------------|------------------------------|
| Mover o sobrevivente  | `←` `→` `↑` `↓` ou `WASD`  |
| Armar bomba           | `SPACE`, `Z` ou `X`          |
| Pausar operação       | `ESC` ou `P`                 |
| Silenciar áudio       | `T`                          |

### Controles virtuais (mobile)

| Botão  | Ação                                          |
|--------|-----------------------------------------------|
| D-pad  | Mover o sobrevivente / navegar nos menus      |
| **X**  | Armar bomba / confirmar seleção nos menus     |
| **Y**  | Pausar / voltar nos menus                     |

---

## Gameplay

- O mapa é uma grade de **19×15 tiles** com paredes sólidas, caixotes destruíveis e inimigos.
- **Bombas** detonam após ~3 segundos e propagam explosões em 4 direções.
- **Explosões** destroem caixotes, matam zumbis e eliminam o jogador se ele for atingido.
- Ao destruir caixotes, há 55% de chance de aparecer um **power-up**.
- O objetivo é **eliminar todos os zumbis** para vencer.
- O jogador começa com **3 vidas** e perde uma ao ser tocado por um zumbi ou atingido por uma explosão.

### Condições de Vitória e Derrota

- **Vitória:** Todos os zumbis eliminados → tela de resultado com estatísticas (tempo, dano recebido, kills).
- **Derrota:** Todas as vidas perdidas → tela de falha com opção de reiniciar.

---

## Power-ups

| Power-up | Efeito                                      |
|----------|---------------------------------------------|
| Bomba    | Aumenta o número máximo de bombas simultâneas |
| Fogo     | Aumenta o alcance das explosões             |

---

## Estrutura do Projeto

```
boomz/
├── index.html                  # Jogo completo (único arquivo de código)
├── favicon.svg                 # Favicon do jogo
├── generate_assets.js          # Gerador de sprites do jogador
├── generate_zombie.js          # Gerador de sprites do zumbi
├── gen_explosion.py            # Gerador de frames de explosão (Python)
└── assets/
    ├── audio/                  # Trilha sonora e efeitos sonoros (.wav)
    ├── backgrounds/            # Cenários do menu e do jogo (.svg)
    ├── characters/             # Sprite sheets do jogador e zumbi (.svg)
    ├── items/                  # Sprites de bombas, explosões e power-ups (.svg)
    ├── ui/                     # Painéis, ícones e logo (.svg)
    └── world/                  # Tiles do mapa: chão, parede, caixote (.svg)
```

---

## Stack Tecnológica

| Tecnologia     | Uso                                           |
|----------------|-----------------------------------------------|
| Kaboom.js v3000.1.17 | Engine de jogo (sprites, física, cenas, input, áudio) |
| JavaScript ES6 | Lógica do jogo                               |
| HTML5 Canvas   | Renderização (304×280px @ escala 2.5×)       |
| SVG            | Todos os assets gráficos                     |
| WAV            | Efeitos sonoros e música                     |

O jogo é servido como um único `index.html` com o código embutido em `<script type="module">`. Não há bundler, transpilador ou framework front-end.

---

## Componentes do Jogo

### Jogador
- Posição inicial: canto superior esquerdo (zona segura)
- Velocidade: 120px/s
- Animações: idle e walk em 3 direções, hurt e death
- Mecânica especial: atravessa a própria bomba recém-colocada até sair do tile

### Zumbis
- 3 inimigos, spawnam em posições pré-definidas
- Velocidade: 42px/s
- IA: patrulha aleatória com mudança de direção a cada 0.5–1.6 segundos
- São destruídos por explosões

### Bombas
- Fuse de 2.35s → fase de alerta de 0.65s → explosão
- Propagam chamas em 4 direções com alcance configurável
- Causam reação em cadeia ao ser atingidas por outras explosões

### Mapa
- Grade 19×15 com paredes indestruíveis nas bordas e em posições pares do interior
- Caixotes destruíveis distribuídos aleatoriamente (exceto na zona segura do jogador)

### Áudio
- Música de fundo e ambience
- SFX para: movimento no menu, confirmação, pausa, colocar bomba, alerta, explosão, dano, morte de zumbi, coleta de power-up, vitória e derrota
- Controle de volume por categoria; toggle de mute via opção nos menus ou tecla `T`

---

## Geradores de Assets

Os sprites do jogo são gerados programaticamente por scripts separados e salvos como SVG:

- **`generate_assets.js`** — Gera o sprite sheet do jogador (48 frames: 6 colunas × 8 linhas, 24×24px cada)
- **`generate_zombie.js`** — Gera o sprite sheet do zumbi (28 frames: 4 colunas × 7 linhas, 24×24px cada)
- **`gen_explosion.py`** — Gera os frames de explosão (15 frames: 3 colunas × 5 linhas, 16×16px cada)

Esses scripts não precisam ser executados para jogar — os assets já estão gerados em `assets/`.

---

## Versões

### v0.2 — Suporte Mobile & Polimento
- **Moldura de console portátil** — interface inspirada em handhelds clássicos (Game Boy) com grilles de alto-falante, logo e faixa inferior decorativa; aparece tanto no desktop quanto no mobile
- **Escala adaptativa** — canvas redimensiona automaticamente para caber na tela do dispositivo preservando a proporção original
- **Controles virtuais** — D-pad + botão X (bomba/confirmar) + botão START (pausar/voltar), exibidos apenas em dispositivos touch
- **Navegação por touch em todos os menus** — menu inicial, menu de pausa e tela de resultado navegáveis pelo D-pad e botão X
- **Toggle de som nos menus** — opção "SOM: ON/OFF" adicionada ao menu inicial e ao menu de pausa; labels de atalho de teclado removidas da tela
- **Favicon** — ícone SVG com temática de bomba e letra Z dourada

### v0.1 — Lançamento inicial
- Movimento e colocação de bombas
- IA de inimigos
- Sistema de explosões com reação em cadeia
- Power-ups
- Sistema de vidas e respawn
- Telas de vitória e derrota com estatísticas
- Trilha sonora e efeitos sonoros completos
- Menu principal, pausa e tela de controles
