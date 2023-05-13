from tkinter import font
import pygame
import random


pygame.font.init()
font = pygame.font.SysFont("Arial", 30)
Pequena = pygame.font.SysFont("Arial", 15)
Grande = pygame.font.SysFont("Verdana", 20)
Titulo = pygame.font.SysFont("Verdana", 40)
Jogar = pygame.font.SysFont("Arial", 30)


# De onde vem os sons utilizados
pygame.mixer.init()
Derrota = pygame.mixer.Sound('Sons/Derrota.mp3')
Vitoria = pygame.mixer.Sound('Sons/Vitoria.mp3')
EntradaJogador = pygame.mixer.Sound('Sons/Jogador.mp3')
EntradaOponente = pygame.mixer.Sound('Sons/Oponente.mp3')
AtaqueJogador = pygame.mixer.Sound('Sons/AtaqueJogador.mp3')
AtaqueOponente = pygame.mixer.Sound('Sons/AtaqueOponente.mp3')
GaloDeArma = pygame.mixer.Sound('Sons/GaloDeArma.mp3')
GaloDeCalca = pygame.mixer.Sound('Sons/GaloDeCalca.mp3')
GaloDeTenis = pygame.mixer.Sound('Sons/GaloDeTenis.mp3')
Bicada = pygame.mixer.Sound('Sons/Bicada.mp3')
Tiro = pygame.mixer.Sound('Sons/Tiro.mp3')
Calcada = pygame.mixer.Sound('Sons/Calcada.mp3')
Chute = pygame.mixer.Sound('Sons/Chute.mp3')


pygame.init()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rinha de Galo")
background = pygame.image.load(f"Imagens/PlanoDeFundoALT.png")
MenuPrincipal = pygame.image.load(f"Imagens/RinhaOfTheGalo.png")
MenuFundo = pygame.transform.scale(MenuPrincipal, (800, 700))

global terrenos
global fundo

# Modificadores de dano referente aos terrenos
terrenos = {
    "Favela": {"Arma": 1.2, "Calca": 0.9, "Tenis": 0.9},
    "Loja de Roupas": {"Arma": 0.9, "Calca": 1.2, "Tenis": 0.9},
    "Quadra de Esportes": {"Arma": 0.9, "Calca": 0.9, "Tenis": 1.2}
}

fundos = [
    pygame.image.load(f"Imagens/Favela.png"),
    pygame.image.load(f"Imagens/Loja.png"),
    pygame.image.load(f"Imagens/Quadra.png")
]

terreno_escolhido = random.choice(list(terrenos.keys()))
fundoGrande = fundos[list(terrenos.keys()).index(terreno_escolhido)]
fundo = pygame.transform.scale(fundoGrande, (800, 800))

# Função para desenhar o botão de jogar


def draw_play_button(screen):
    surface = Jogar.render("Jogar", True, (255, 255, 255))
    text_rect = surface.get_rect()
    padding = 10  # Espaço de 10 pixels em cada lado

    # Define as dimensões do retângulo branco
    button_width = text_rect.width + 2 * padding
    button_height = text_rect.height + 2 * padding

    x = (screen.get_width() - button_width) // 2
    y = (screen.get_height() - button_height) // 2 + 180

    # Desenha o retângulo branco
    button_rect = pygame.Rect(x, y, button_width, button_height)
    pygame.draw.rect(screen, (255, 255, 255), button_rect)

    # Define as dimensões do retângulo preto
    border_width = button_width - 2
    border_height = button_height - 2

    # Desenha o retângulo preto
    border_rect = pygame.Rect(x + 1, y + 1, border_width, border_height)
    pygame.draw.rect(screen, (0, 0, 0), border_rect)

    # Posiciona o texto centralizado dentro do retângulo
    text_x = x + padding + (button_width - 2 * padding - text_rect.width) // 2
    text_y = y + padding + (button_height - 2 *
                            padding - text_rect.height) // 2
    screen.blit(surface, (text_x, text_y))


# Função para verificar se o botão de jogar foi clicado


def check_play_button(screen):
    mouse_pos = pygame.mouse.get_pos()  # Obtém a posição do mouse
    surface = Jogar.render("Jogar", True, (255, 0, 0))
    x = (screen.get_width() - surface.get_width()) // 2
    y = (screen.get_height() - surface.get_height()) // 2 + 180
    # Retângulo do botão de jogar
    play_button_rect = pygame.Rect(
        x, y, surface.get_width(), surface.get_height())

    # Verifica se o mouse está sobre o botão
    if play_button_rect.collidepoint(mouse_pos):
        # Retorna True se o botão esquerdo do mouse foi clicado
        return pygame.mouse.get_pressed()[0]

    return False


class Galo:
    # Definindo o que representa um galo e seus atributos.

    def __init__(self, name, type, hp, attack):
        self.name = name
        self.type = type
        self.hp = hp
        self.contadorAtaqueEspecial = 0
        self.contadorAtaqueEspecialOponente = 0
        self.attacks = [
            {"name": "Ataque 1", "power": 10},
            {"name": "Ataque 2", "power": 20},
            {"name": "Ataque 3", "power": 30},
            {"name": "Ataque 4", "power": 40}
        ]
        # Ataques do galo de arma
        if name == "Galo de Arma":
            self.attacks = [
                {"name": "Bicada", "power": 5},
                {"name": "Tiro", "power": 10},
                {"name": "Ataque Especial", "power": 10},
                {"name": "Aumentar Ataque", "power": 0}
            ]
            # Ataques galo de calca
        elif name == "Galo de Calca":
            self.attacks = [
                {"name": "Bicada", "power": 5},
                {"name": "Calçada", "power": 10},
                {"name": "Ataque Especial", "power": 10},
                {"name": "Aumentar Ataque", "power": 0}
            ]
            # Ataques galo de tenis
        elif name == "Galo de Tenis":
            self.attacks = [
                {"name": "Bicada", "power": 5},
                {"name": "Chute", "power": 10},
                {"name": "Ataque Especial", "power": 10},
                {"name": "Aumentar Ataque", "power": 0}
            ]

# Tela de inicio, definição padrão básica


def draw_text(screen, text, x, y):
    surface = font.render(text, True, (255, 255, 255))
    screen.blit(surface, (x, y))


def draw_bom(screen, text, x, y):
    surface = font.render(text, True, (0, 255, 0))
    screen.blit(surface, (x, y))


def draw_ruim(screen, text, x, y):
    surface = font.render(text, True, (255, 0, 0))
    screen.blit(surface, (x, y))


def draw_neutro(screen, text, x, y):
    surface = font.render(text, True, (255, 255, 255))
    screen.blit(surface, (x, y))


def draw_text_vermelho(screen, text, x, y):
    surface = Titulo.render(text, True, (255, 0, 0))
    x = (screen.get_width() - surface.get_width()) // 2
    y = (screen.get_height() - surface.get_height()) // 2 + 30
    screen.blit(surface, (x, y))


def draw_text_amarelo(screen, text, x, y):
    surface = Titulo.render(text, True, (255, 255, 0))
    x = (screen.get_width() - surface.get_width()) // 2
    y = (screen.get_height() - surface.get_height()) // 2 - 30
    screen.blit(surface, (x, y))


def draw_grande(screen, text, x, y):
    # criando a superfície de texto
    surface = Grande.render(text, True, (255, 255, 255))

    # configurando o estilo do texto
    surface = pygame.font.Font.render(
        Grande, text, True, (255, 255, 255), (0, 0, 0))

    # exibindo o texto na tela
    screen.blit(surface, (x, y))

# Função de desenhar os galos na tela, tamanho, e de onde pegar a imagem.


def draw_galo(screen, galo, x, y, size):
    image = pygame.image.load(f"Imagens/{galo.name}.png")
    image = pygame.transform.scale(image, (size, size))
    screen.blit(image, (x, y))
    return pygame.Rect(x, y, image.get_width(), image.get_height())


# Definição de onde renderizar a foto do galo do oponente, e de onde pegar a imagem
def draw_galooponnent(screen, galo, x, y, size):
    image = pygame.image.load(f"Imagens/{galo.name} Oponente.png")
    image = pygame.transform.scale(image, (size, size))
    screen.blit(image, (x, y))


# Função da barra de vida de forma visual


def draw_health_bars(screen, player_galo, opponent_galo):
    # Barra de vida do jogador
    draw_grande(screen, str(player_galo.hp), 100, 590)
    pygame.draw.rect(screen, (255, 0, 0), (50, 550, 200, 20))
    health_percentage = player_galo.hp / 100
    pygame.draw.rect(screen, (0, 255, 0),
                     (50, 550, int(200 * health_percentage), 20))

    # Barra de vida do oponente
    draw_grande(screen, str(opponent_galo.hp), 570, 590)
    pygame.draw.rect(screen, (255, 0, 0), (490, 550, 200, 20))
    health_percentage = opponent_galo.hp / 100
    pygame.draw.rect(screen, (0, 255, 0), (490, 550,
                     int(200 * health_percentage), 20))

# Função de atualizar as barras de vida


def update_health_bars(player_galo, opponent_galo):
    player_galo_hp = player_galo.hp
    opponent_galo_hp = opponent_galo.hp
    return player_galo_hp, opponent_galo_hp

# Função para escrever no centro da tela uma mensagem


def draw_text_centered(screen, text):
    surface = font.render(text, True, (255, 255, 255))
    x = (screen.get_width() - surface.get_width()) // 2
    y = (screen.get_height() - surface.get_height()) // 2
    screen.blit(surface, (x, y))


# Inicio da classe jogador
class Player:
    def __init__(self, galo):
        self.galo = galo


class Game:

    # Modificadores de dano dos galos - Valores teste, são utilizados para multiplicar o dano referente à vantagem de tipo
    type_chart = {
        "Arma": {"Arma": 1, "Calca": 0.9, "Tenis": 1.15},
        "Calca": {"Arma": 1.15, "Calca": 1, "Tenis": 0.9},
        "Tenis": {"Arma": 0.9, "Calca": 1.15, "Tenis": 1}
    }

    # Iniciando o jogador, e seus atributos

    def __init__(self):
        self.player = None
        self.opponent = None
        self.player_turn = True
        self.attack_selected = False
        self.selected_attack = None

    # Definindo o galo do jogador (tela de seleção)
    def select_galo(self):

        selected_galo = None
        while selected_galo is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            screen.blit(background, (0, 0))

            surface = font.render(
                "Selecione seu Galo de Briga:", True, (255, 0, 0))
            x = (screen.get_width() - surface.get_width()) // 2
            y = (screen.get_height() - surface.get_height()) // 2 - 250
            # draw_text(screen, "Selecione seu Galo de Briga:", 190, 90)
            draw_text(screen, "Selecione seu Galo de Briga:", x, y)

            # exibe as imagens dos galos disponíveis

            galo1 = Galo("Galo de Arma", "Arma", 100, 20)
            galo1_rect = draw_galo(screen, galo1, 50, 100, 160)

            galo2 = Galo("Galo de Calca", "Calca", 100, 20)
            galo2_rect = draw_galo(screen, galo2, 300, 100, 160)

            galo3 = Galo("Galo de Tenis", "Tenis", 100, 20)
            galo3_rect = draw_galo(screen, galo3, 550, 100, 160)

            # verifica se o jogador clicou em algum dos galos
            mouse_pos = pygame.mouse.get_pos()

            surface = font.render(
                "Modificadores de Terreno: (Alteram ataque base)", True, (255, 0, 0))
            xterreno = (screen.get_width() - surface.get_width()) // 2
            ymodificadores = (screen.get_height() -
                              surface.get_height()) // 2 + 120

            if galo1_rect.collidepoint(mouse_pos):

                draw_text(screen, galo1.name, 50, 270)
                draw_text(screen, f"Vantagem contra: {galo3.name}", 200, 320)
                draw_text(
                    screen, f"Modificadores de Terreno: (Alteram ataque base)", xterreno, 350)
                draw_bom(screen, f"Favela (1.15X)", 160, ymodificadores)
                draw_neutro(screen, f"Quadra (1.0X)", 340, ymodificadores)
                draw_ruim(screen, f"Loja (0.9X)", 540, ymodificadores)
                if pygame.mouse.get_pressed()[0]:
                    selected_galo = galo1
                    pygame.time.delay(1500)  # adiciona um delay de 500 ms

            elif galo2_rect.collidepoint(mouse_pos):
                draw_text(screen, galo2.name, 300, 270)
                draw_text(screen, f"Vantagem contra: {galo1.name}", 200, 320)
                draw_text(
                    screen, f"Modificadores de Terreno: (Alteram ataque base)", xterreno, 350)
                draw_bom(screen, f"Loja (1.15X)", 160, ymodificadores)
                draw_neutro(screen, f"Favela (1.0X)", 340, ymodificadores)
                draw_ruim(screen, f"Quadra (0.9X)", 540, ymodificadores)
                if pygame.mouse.get_pressed()[0]:
                    selected_galo = galo2
                    pygame.time.delay(1500)  # adiciona um delay de 500 ms

            elif galo3_rect.collidepoint(mouse_pos):
                draw_text(screen, galo3.name, 550, 270)
                draw_text(screen, f"Vantagem contra: {galo2.name}", 200, 320)
                draw_text(
                    screen, f"Modificadores de Terreno: (Alteram ataque base)", xterreno, 350)
                draw_bom(screen, f"Quadra (1.15X)", 160, ymodificadores)
                draw_neutro(screen, f"Loja (1.0X)", 340, ymodificadores)
                draw_ruim(screen, f"Favela (0.9X)", 540, ymodificadores)
                if pygame.mouse.get_pressed()[0]:
                    selected_galo = galo3
                    pygame.time.delay(1500)  # adiciona um delay de 500 ms

            pygame.display.update()
        return Player(selected_galo)

    # Função de escolher o galo do oponente
    def select_opponent(self):

        opponents = [
            Galo("Galo de Arma", "Arma", 100, 20),
            Galo("Galo de Calca", "Calca", 100, 20),
            Galo("Galo de Tenis", "Tenis", 100, 20)
        ]

        # Cria uma lista ordenada de tipos de galos, do mais forte ao mais fraco
        types_ordered = ["Arma", "Calca", "Tenis"]
        player_type = self.player.galo.type
        # remove o tipo de galo do jogador da lista
        types_ordered.remove(player_type)

        # Seleciona o tipo de galo mais forte para combater o tipo do jogador
        opponent_type = None
        for t in types_ordered:
            if opponent_type is None:
                opponent_type = t
            elif Game.type_chart[t][player_type] > Game.type_chart[opponent_type][player_type]:
                opponent_type = t

        # Seleciona o galo mais forte do tipo escolhido pelo oponente
        opponent_galo = None
        for g in opponents:
            if g.type == opponent_type:
                if opponent_galo is None or g.hp > opponent_galo.hp:
                    opponent_galo = g

        return Player(opponent_galo)

    def animacaoentradajogador(self):
        # "Inteligência artificial" escolhendo o galo, enquanto você manda seu galo pra combate
        pygame.display.update()
        screen.blit(background, (0, 0))
        draw_text(
            screen, f"Jogador: Dê seu melhor, {self.player.galo.name}", 200, 100)
        if self.player.galo.name == "Galo de Arma":
            GaloDeArma.play()
        if self.player.galo.name == "Galo de Calca":
            GaloDeCalca.play()
        if self.player.galo.name == "Galo de Tenis":
            GaloDeTenis.play()
        draw_galo(screen, self.player.galo, 50, 320, 200)
        pygame.display.update()
        pygame.time.delay(3000)

    def animacaoentradaoponente(self):
        textoescolhaoponente = font.render(
            'Oponente Escolhendo', True, (255, 255, 255))
        x = (800 - textoescolhaoponente.get_width()) // 2
        y = 800 / 2

        draw_text(screen, "Oponente Escolhendo.", x, y)
        pygame.display.update()
        pygame.time.delay(1000)
        screen.blit(background, (0, 0))
        draw_galo(screen, self.player.galo, 50, 320, 200)
        draw_text(screen, "Oponente Escolhendo..", x, y)
        pygame.display.update()
        pygame.time.delay(1000)
        screen.blit(background, (0, 0))
        draw_galo(screen, self.player.galo, 50, 320, 200)
        draw_text(screen, "Oponente Escolhendo...", x, y)
        pygame.display.update()
        pygame.time.delay(2000)
        screen.blit(background, (0, 0))
        draw_galo(screen, self.player.galo, 50, 320, 200)
        draw_text(
            screen, f"Oponente: Ganha a aposta, {self.opponent.galo.name}", 200, 100)
        pygame.display.update()
        pygame.time.delay(2000)
        if self.opponent.galo.name == "Galo de Arma":
            GaloDeArma.play()
        if self.opponent.galo.name == "Galo de Calca":
            GaloDeCalca.play()
        if self.opponent.galo.name == "Galo de Tenis":
            GaloDeTenis.play()
        draw_galooponnent(screen, self.opponent.galo, 500, 320, 200)
        pygame.display.update()
        pygame.time.delay(5000)

    def select_attack(self):

        selected_attack = None
        while selected_attack is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            screen.blit(fundo, (0, 0))
            draw_grande(screen, f"{self.player.galo.name} ataca:", 50, 50)
            draw_galo(screen, self.player.galo, 50, 320, 200)
            draw_galooponnent(screen, self.opponent.galo, 500, 320, 200)
            draw_health_bars(screen, self.player.galo, self.opponent.galo)

            # exibe os ataques disponíveis
            for i, attack in enumerate(self.player.galo.attacks):
                text = f"{i + 1}. {attack['name']}"
                draw_grande(screen, text, 50, 100 + i * 50)

                # verifica se o jogador clicou em algum dos ataques
                mouse_pos = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0] and 100 + i * 50 <= mouse_pos[1] <= 100 + i * 50 + 50:
                    selected_attack = attack

            pygame.display.update()

        self.selected_attack = selected_attack
        self.attack_selected = True

    def fight(self):
        clock = pygame.time.Clock()

        contadorJogador = 0
        base_de_ataqueJogador = 1
        contadorOponente = 0
        base_de_ataqueOponente = 1
        contadorAtaqueEspecialJogador = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            screen.blit(fundo, (0, 0))

            if self.player_turn:
                Bicada.stop()
                Tiro.stop()
                Calcada.stop()
                Chute.stop()
                draw_grande(screen, "Sua vez de atacar", 50, 50)
                draw_galo(screen, self.player.galo, 50, 320, 200)
                draw_galooponnent(screen, self.opponent.galo, 500, 320, 200)
                draw_health_bars(screen, self.player.galo, self.opponent.galo)

                # exibe os ataques disponíveis

                if not self.attack_selected:
                    self.select_attack()  # seleciona o ataque apenas uma vez
                else:
                    draw_grande(
                        screen, f"Você usou {self.selected_attack['name']}", 50, 100)
                    if self.selected_attack['name'] == "Bicada":
                        Bicada.play()
                    if self.selected_attack['name'] == "Tiro":
                        Tiro.play()
                    if self.selected_attack['name'] == "Calçada":
                        Calcada.play()
                    if self.selected_attack['name'] == "Chute":
                        Chute.play()

                    if self.selected_attack['name'] == "Ataque Especial":
                        if contadorAtaqueEspecialJogador < 2:
                            contadorAtaqueEspecialJogador = contadorAtaqueEspecialJogador + 1
                            attack_modifier = Game.type_chart[self.player.galo.type][self.opponent.galo.type]
                        else:
                            draw_grande(
                                screen, "Você já usou o ataque especial duas vezes", 50, 190)
                            pygame.display.update()
                            pygame.time.delay(2000)
                            self.attack_selected = False
                            attack_modifier = 0

                    else:
                        attack_modifier = 1

                    if self.selected_attack['name'] == "Aumentar Ataque":
                        if contadorJogador < 2:
                            base_de_ataqueJogador = base_de_ataqueJogador + 0.5
                            contadorJogador = contadorJogador + 1
                            draw_grande(screen, f"Você aumentou seu dano base para " +
                                        str(float(base_de_ataqueJogador)) + "X", 50, 190)
                        else:
                            draw_grande(
                                screen, "Você já aumentou o máximo de vezes o aumento de ataque", 50, 190)
                            self.attack_selected = False

                    else:
                        base_de_ataqueJogador = base_de_ataqueJogador

                    terreno_modifier = terrenos[terreno_escolhido][self.player.galo.type]

                    if self.selected_attack['name'] == "Tiro":
                        attack_modifier = 1
                        terreno_modifier = 1
                    if self.selected_attack['name'] == "Calçada":
                        attack_modifier = 1
                        terreno_modifier = 1
                    if self.selected_attack['name'] == "Chute":
                        attack_modifier = 1
                        terreno_modifier = 1

                    draw_grande(screen, f"Você causou " + str(int(
                        self.selected_attack['power'] * attack_modifier * terreno_modifier * base_de_ataqueJogador)) + " de dano", 50, 150)
                    pygame.display.update()
                    pygame.time.delay(2000)

                    self.opponent.galo.hp -= int(
                        self.selected_attack['power'] * attack_modifier * terreno_modifier * base_de_ataqueJogador)

                    if self.opponent.galo.hp <= 0:
                        self.opponent.galo.hp = 0

                        screen.fill((0, 0, 0))
                        screen.blit(background, (0, 0))
                        screen.blit(fundo, (0, 0))
                        draw_grande(
                            screen, f"{self.opponent.galo.name} desmaiou e saiu de combate", 200, 50)
                        draw_galo(screen, self.player.galo, 50, 320, 200)
                        draw_galooponnent(
                            screen, self.opponent.galo, 500, 320, 200)
                        draw_health_bars(
                            screen, self.player.galo, self.opponent.galo)
                        draw_health_bars(
                            screen, self.player.galo, self.opponent.galo)
                        pygame.display.update()
                        pygame.time.delay(4000)
                        screen.fill((0, 0, 0))
                        pygame.display.update()
                        draw_text_centered(screen, "Você Ganhou!")
                        pygame.display.update()
                        pygame.time.wait(2000)
                        return
                    self.player_turn = False
                    self.attack_selected = False

                    pygame.time.delay(500)  # adiciona um delay de 500 ms
                    pygame.display.update()

            else:
                pygame.display.update()
                Bicada.stop()
                Tiro.stop()
                Calcada.stop()
                Chute.stop()
                draw_grande(screen, "Vez do oponente atacar", 50, 50)
                draw_galo(screen, self.player.galo, 50, 320, 200)
                draw_galooponnent(screen, self.opponent.galo, 500, 320, 200)
                draw_health_bars(screen, self.player.galo, self.opponent.galo)
                pygame.display.update()
                pygame.time.delay(3000)

                def find_best_attack(opponent_galo, player_galo):
                    best_attack = None
                    max_damage = 0
                    use_attack_modifier = False
                    if 'contadorAtaqueEspecialOponente' not in locals():
                        contadorAtaqueEspecialOponente = 0

                    # Priorize o uso do ataque "Aumentar Ataque" caso o contador ainda não tenha atingido 2 ou o HP do oponente seja maior que 65
                    if opponent_galo.hp > 65 and contadorOponente < 2:
                        use_attack_modifier = True

                    for attack in opponent_galo.attacks:
                        if attack['name'] == "Aumentar Ataque":
                            if contadorOponente >= 2 or opponent_galo.hp < 65:
                                continue

                            if use_attack_modifier:
                                best_attack = attack
                                max_damage = 0
                                break

                        if attack['name'] == "Ataque Especial":
                            if contadorAtaqueEspecialJogador < 2:
                                contadorAtaqueEspecialOponente = contadorAtaqueEspecialOponente + 1
                                attack_modifier = Game.type_chart[self.opponent.galo.type][self.player.galo.type]
                            else:
                                attack_modifier = 0
                        else:

                            attack_modifier = Game.type_chart[self.opponent.galo.type][self.player.galo.type]

                        terreno_modifier = terrenos[terreno_escolhido][opponent_galo.type]

                        if attack['name'] == "Tiro":
                            attack_modifier = 1
                            terreno_modifier = 1
                        if attack['name'] == "Calçada":
                            attack_modifier = 1
                            terreno_modifier = 1
                        if attack['name'] == "Chute":
                            attack_modifier = 1
                            terreno_modifier = 1

                        damage = int(
                            attack['power'] * attack_modifier * terreno_modifier * base_de_ataqueOponente)

                        print(attack['name'])
                        print(damage)
                        if damage > max_damage:
                            best_attack = attack
                            max_damage = damage

                    return best_attack
                opponent_attack = find_best_attack(
                    self.opponent.galo, self.player.galo)

                # Ataque aleatorio abaixo (para testes)
                # opponent_attack = random.choice(self.opponent.galo.attacks)
                # Fim do ataque aleatorio

                draw_grande(
                    screen, f"O oponente usou {opponent_attack['name']}", 50, 100)
                if opponent_attack['name'] == "Bicada":
                    Bicada.play()
                if opponent_attack['name'] == "Tiro":
                    Tiro.play()
                if opponent_attack['name'] == "Calçada":
                    Calcada.play()
                if opponent_attack['name'] == "Chute":
                    Chute.play()

                if opponent_attack['name'] == "Ataque Especial":
                    attack_modifier = Game.type_chart[self.opponent.galo.type][self.player.galo.type]
                else:
                    attack_modifier = 1

                if opponent_attack['name'] == "Aumentar Ataque":
                    if contadorOponente < 2:
                        base_de_ataqueOponente = base_de_ataqueOponente + 0.5
                        contadorOponente = contadorOponente + 1
                else:
                    base_de_ataqueOponente = base_de_ataqueOponente

                terreno_modifier = terrenos[terreno_escolhido][self.opponent.galo.type]

                draw_grande(screen, f"Oponente causou " + str(int(
                    opponent_attack['power'] * attack_modifier * terreno_modifier * base_de_ataqueOponente)) + " de dano", 50, 150)
                pygame.display.update()
                self.player.galo.hp -= int(
                    opponent_attack['power'] * attack_modifier * terreno_modifier * base_de_ataqueOponente)

                if self.player.galo.hp <= 0:
                    self.player.galo.hp = 0

                    screen.fill((0, 0, 0))
                    screen.blit(background, (0, 0))
                    screen.blit(fundo, (0, 0))
                    draw_grande(
                        screen, f"{self.player.galo.name} desmaiou e saiu de combate", 50, 200)
                    draw_galo(screen, self.player.galo, 50, 320, 200)
                    draw_galooponnent(
                        screen, self.opponent.galo, 500, 320, 200)
                    draw_health_bars(screen, self.player.galo,
                                     self.opponent.galo)
                    pygame.display.update()
                    pygame.time.delay(4000)
                    screen.fill((0, 0, 0))
                    pygame.display.update()
                    draw_text_centered(screen, "Você Perdeu!")
                    pygame.display.update()
                    pygame.time.wait(2000)
                    return

                pygame.display.update()

                pygame.time.delay(1500)  # adiciona um delay de 500 ms
                self.player_turn = True

            # atualiza as barras de vida
            player_galo_hp, opponent_galo_hp = update_health_bars(
                self.player.galo, self.opponent.galo)
            self.player.galo.hp = player_galo_hp
            self.opponent.galo.hp = opponent_galo_hp
            pygame.display.update()

            # verifica se o jogo acabou
            if self.player.galo.hp <= 0:
                pygame.display.update()
                return
            elif self.opponent.galo.hp <= 0:
                pygame.display.update()
                return

            pygame.display.update()
            clock.tick(30)


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    screen.blit(MenuFundo, (0, 0))

    pygame.display.update()
    pygame.time.wait(1000)

    game_started = False  # Variável para controlar se o jogo foi iniciado

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if not game_started and event.type == pygame.MOUSEBUTTONDOWN:
                if check_play_button(screen):
                    game_started = True

        if not game_started:
            draw_play_button(screen)
        else:
            game = Game()
            game.player = game.select_galo()
            game.entradajogador = game.animacaoentradajogador()
            game.opponent = game.select_opponent()
            game.entradaoponente = game.animacaoentradaoponente()

            # Loop principal do jogo
            while True:
                # Limpa a tela
                screen.fill((0, 0, 0))

                # Verifica se o jogador ou o oponente zerou a vida
                if game.player.galo.hp <= 0:
                    draw_text_centered(screen, "Você Perdeu!")
                    Derrota.play()
                    pygame.display.update()
                    pygame.time.wait(10000)
                    pygame.quit()
                    return
                elif game.opponent.galo.hp <= 0:
                    draw_text_centered(screen, "Você Ganhou!")
                    Vitoria.play()
                    pygame.display.update()
                    pygame.time.wait(5000)
                    pygame.quit()
                    return

                # Seleciona o ataque e inicia a luta
                game.select_attack()
                game.fight()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
