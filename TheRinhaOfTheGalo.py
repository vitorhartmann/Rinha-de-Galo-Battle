from tkinter import font
import pygame
import random


pygame.font.init()
font = pygame.font.SysFont("Arial", 30)
Pequena = pygame.font.SysFont("Arial", 15)
Grande = pygame.font.SysFont("Verdana", 20)



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
width, height = 720, 640
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rinha de Galo")
background = pygame.image.load(f"Imagens/PlanoDeFundoALT.png")

global terrenos
global fundo

terrenos = {
    "Favela": {"Arma": 1.1, "Calca": 0.9, "Tenis": 0.9},
    "Loja de Roupas": {"Arma": 0.9, "Calca": 1.1, "Tenis": 0.9},
    "Quadra de Esportes": {"Arma": 0.9, "Calca": 0.9, "Tenis": 1.1}
}

fundos = [
    pygame.image.load(f"Imagens/Favela.png"),
    pygame.image.load(f"Imagens/Loja.png"),
    pygame.image.load(f"Imagens/Quadra.png")
]

terreno_escolhido = random.choice(list(terrenos.keys()))
fundoGrande = fundos[list(terrenos.keys()).index(terreno_escolhido)]
fundo = pygame.transform.scale(fundoGrande, (720, 640))


class Galo:
    # Definindo o que representa um galo e seus atributos.

    def __init__(self, name, type, hp, attack):
        self.name = name
        self.type = type
        self.hp = hp
        self.attacks = [
            {"name": "Ataque 1", "power": 10},
            {"name": "Ataque 2", "power": 20},
            {"name": "Ataque 3", "power": 30},
            {"name": "Ataque 4", "power": 40}
        ]

        if name == "Galo de Arma":
            self.attacks = [
                {"name": "Bicada", "power": 5},
                {"name": "Tiro", "power": 10},
                {"name": "Ataque Especial", "power": 10},
                {"name": "Aumentar Ataque", "power": 0}
            ]
        elif name == "Galo de Calca":
            self.attacks = [
                {"name": "Bicada", "power": 5},
                {"name": "Calçada", "power": 10},
                {"name": "Ataque Especial", "power": 10},
                {"name": "Aumentar Ataque", "power": 0}
            ]
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
        "Arma": {"Arma": 1, "Calca": 0.8, "Tenis": 1.25},
        "Calca": {"Arma": 1.25, "Calca": 1, "Tenis": 0.8},
        "Tenis": {"Arma": 0.8, "Calca": 1.25, "Tenis": 1}
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
            draw_text(screen, "Selecione seu Galo de Briga:", 50, 50)

            # exibe as imagens dos galos disponíveis

            galo1 = Galo("Galo de Arma", "Arma", 100, 20)
            galo1_rect = draw_galo(screen, galo1, 150, 100, 100)

            galo2 = Galo("Galo de Calca", "Calca", 100, 20)
            galo2_rect = draw_galo(screen, galo2, 300, 100, 100)

            galo3 = Galo("Galo de Tenis", "Tenis", 100, 20)
            galo3_rect = draw_galo(screen, galo3, 450, 100, 100)

            # verifica se o jogador clicou em algum dos galos
            mouse_pos = pygame.mouse.get_pos()
            if galo1_rect.collidepoint(mouse_pos):
                draw_text(screen, galo1.name, 120, 210)
                draw_text(screen, f"Bom contra: {galo3.name}", 200, 280)
                draw_text(screen, f"Modificador de Terreno:", 200, 310)
                draw_text(screen, f"Favela (1.1X)", 200, 340)
                draw_text(screen, f"Loja (0.9X)", 200, 370)
                draw_text(screen, f"Quadra (1.0X)", 200, 400)
                if pygame.mouse.get_pressed()[0]:
                    selected_galo = galo1
                    pygame.time.delay(1500)  # adiciona um delay de 500 ms

            elif galo2_rect.collidepoint(mouse_pos):
                draw_text(screen, galo2.name, 270, 210)
                draw_text(screen, f"Bom contra: {galo1.name}", 200, 280)
                draw_text(screen, f"Modificador de Terreno:", 200, 310)
                draw_text(screen, f"Loja (1.1X)", 200, 340)
                draw_text(screen, f"Quadra (0.9X)", 200, 370)
                draw_text(screen, f"Favela (1.0X)", 200, 400)
                if pygame.mouse.get_pressed()[0]:
                    selected_galo = galo2
                    pygame.time.delay(1500)  # adiciona um delay de 500 ms

            elif galo3_rect.collidepoint(mouse_pos):
                draw_text(screen, galo3.name, 420, 210)
                draw_text(screen, f"Bom contra: {galo2.name}", 200, 280)
                draw_text(screen, f"Modificador de Terreno:", 200, 310)
                draw_text(screen, f"Quadra (1.1X)", 200, 340)
                draw_text(screen, f"Favela (0.9X)", 200, 370)
                draw_text(screen, f"Loja (1.0X)", 200, 400)
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
            screen, f"Jogador: Dê seu melhor, {self.player.galo.name}", 50, 100)
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
        draw_text(screen, "Oponente Escolhendo.", 200, 250)
        pygame.display.update()
        pygame.time.delay(1000)
        screen.blit(background, (0, 0))
        draw_galo(screen, self.player.galo, 50, 320, 200)
        draw_text(screen, "Oponente Escolhendo..", 200, 250)
        pygame.display.update()
        pygame.time.delay(1000)
        screen.blit(background, (0, 0))
        draw_galo(screen, self.player.galo, 50, 320, 200)
        draw_text(screen, "Oponente Escolhendo...", 200, 250)
        pygame.display.update()
        pygame.time.delay(2000)
        screen.blit(background, (0, 0))
        draw_galo(screen, self.player.galo, 50, 320, 200)
        draw_text(
            screen, f"Oponente: Ganha a aposta, {self.opponent.galo.name}", 50, 100)
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
                        attack_modifier = Game.type_chart[self.player.galo.type][self.opponent.galo.type]

                    else:
                        attack_modifier = 1

                    if self.selected_attack['name'] == "Aumentar Ataque":
                        if contadorJogador < 2:
                            base_de_ataqueJogador = base_de_ataqueJogador + 0.5
                            contadorJogador = contadorJogador + 1
                            draw_grande(screen, f"Você aumentou seu dano base para " +
                                        str(float(base_de_ataqueJogador)), 50, 190)
                        else:
                            draw_grande(
                                screen, "Você já aumentou o máximo de vezes o aumento de ataque", 50, 190)

                    else:
                        base_de_ataqueJogador = base_de_ataqueJogador

                    terreno_modifier = terrenos[terreno_escolhido][self.player.galo.type]

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
                            attack_modifier = Game.type_chart[self.opponent.galo.type][self.player.galo.type]
                        else:
                            attack_modifier = 1

                        terreno_modifier = terrenos[terreno_escolhido][opponent_galo.type]

                        damage = int(
                            attack['power'] * attack_modifier * terreno_modifier * base_de_ataqueOponente)

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
            break
        elif game.opponent.galo.hp <= 0:
            draw_text_centered(screen, "Você Ganhou!")
            Vitoria.play()
            pygame.display.update()
            pygame.time.wait(5000)
            break

        # Seleciona o ataque e inicia a luta
        game.select_attack()
        game.fight()

    pygame.quit()


if __name__ == "__main__":
    main()
