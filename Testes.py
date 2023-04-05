from tkinter import font
import pygame
import random


pygame.font.init()
font = pygame.font.SysFont("Arial", 16)

pygame.init()
width, height = 720, 640
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rinha de Galo")
background = pygame.image.load(f"Imagens/PlanoDeFundoALT.png")


class Galo:
    #Definindo o que representa um galo e seus atributos.
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
                {"name": "Bicada - 10", "power": 10},
                {"name": "Tiro - 15", "power": 15},
                {"name": "Ataque Especial", "power": 15},
                {"name": "Aumentar ataque", "power": 0}
            ]
        elif name == "Galo de Calca":
            self.attacks = [
                {"name": "Bicada - 10", "power": 10},
                {"name": "Calçada - 15", "power": 15},
                {"name": "Ataque Especial", "power": 15},
                {"name": "Aumentar ataque", "power": 0}
            ]
        elif name == "Galo de Tenis":
            self.attacks = [
                {"name": "Bicada - 10", "power": 10},
                {"name": "Chute - 15", "power": 15},
                {"name": "Ataque Especial", "power": 15},
                {"name": "Aumentar ataque", "power": 0}
            ]

#Tela de inicio, definição padrão básica
def draw_text(screen, text, x, y):
    surface = font.render(text, True, (255, 255, 255))
    screen.blit(surface, (x, y))

#Função de desenhar os galos na tela, tamanho, e de onde pegar a imagem.
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

#Função da barra de vida de forma visual
def draw_health_bars(screen, player_galo, opponent_galo):
    # Barra de vida do jogador
    draw_text(screen, str(player_galo.hp), 100, 590)
    pygame.draw.rect(screen, (255, 0, 0), (50, 550, 200, 20))
    health_percentage = player_galo.hp / 100
    pygame.draw.rect(screen, (0, 255, 0),
                     (50, 550, int(200 * health_percentage), 20))

    # Barra de vida do oponente
    draw_text(screen, str(opponent_galo.hp), 570, 250)
    pygame.draw.rect(screen, (255, 0, 0), (490, 220, 200, 20))
    health_percentage = opponent_galo.hp / 100
    pygame.draw.rect(screen, (0, 255, 0), (490, 220,
                     int(200 * health_percentage), 20))

#Função de atualizar as barras de vida
def update_health_bars(player_galo, opponent_galo):
    player_galo_hp = player_galo.hp
    opponent_galo_hp = opponent_galo.hp
    return player_galo_hp, opponent_galo_hp

#Função para escrever no centro da tela uma mensagem
def draw_text_centered(screen, text):
            surface = font.render(text, True, (255, 255, 255))
            x = (screen.get_width() - surface.get_width()) // 2
            y = (screen.get_height() - surface.get_height()) // 2
            screen.blit(surface, (x, y))


#Inicio da classe jogador
class Player:
    def __init__(self, galo):
        self.galo = galo


class Game:

    #Modificadores de dano dos galos - Valores teste, são utilizados para multiplicar o dano referente à vantagem de tipo
    type_chart = {
        "Arma": {"Arma": 1, "Calca": 0.7, "Tenis": 1.3},
        "Calca": {"Arma": 1.3, "Calca": 1, "Tenis": 0.7 },
        "Tenis": {"Arma": 0.7, "Calca": 1.3, "Tenis": 1}
    }

    #Iniciando o jogador, e seus atributos
    def __init__(self):
        self.player = None
        self.opponent = None
        self.player_turn = True
        self.attack_selected = False
        self.selected_attack = None

    #Definindo o galo do jogador (tela de seleção)
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
                draw_text(screen, galo1.name, 150, 210)
                if pygame.mouse.get_pressed()[0]:
                    selected_galo = galo1
                    pygame.time.delay(1500)  # adiciona um delay de 500 ms

            elif galo2_rect.collidepoint(mouse_pos):
                draw_text(screen, galo2.name, 300, 210)
                if pygame.mouse.get_pressed()[0]:
                    selected_galo = galo2
                    pygame.time.delay(1500)  # adiciona um delay de 500 ms

            elif galo3_rect.collidepoint(mouse_pos):
                draw_text(screen, galo3.name, 450, 210)
                if pygame.mouse.get_pressed()[0]:
                    selected_galo = galo3
                    pygame.time.delay(1500)  # adiciona um delay de 500 ms

        # "Inteligência artificial" escolhendo o galo
            pygame.display.update()
        draw_text(screen, "Oponente Escolhendo.", 200, 400)
        pygame.display.update()
        pygame.time.delay(1000)
        draw_text(screen, "Oponente Escolhendo..", 200, 400)
        pygame.display.update()
        pygame.time.delay(1000)
        draw_text(screen, "Oponente Escolhendo...", 200, 400)
        pygame.display.update()
        pygame.time.delay(2000)
        
        return Player(selected_galo)

    #Função de escolher o galo do oponente
    def select_opponent(self):
        opponents = [
            Galo("Galo de Arma", "Arma", 100, 20),
            Galo("Galo de Calca", "Calca", 100, 20),
            Galo("Galo de Tenis", "Tenis", 100, 20)
        ]

        # Cria uma lista ordenada de tipos de galos, do mais forte ao mais fraco
        types_ordered = ["Arma", "Calca", "Tenis"]
        player_type = self.player.galo.type
        types_ordered.remove(player_type) # remove o tipo de galo do jogador da lista

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

    

    def select_attack(self):
        selected_attack = None
        while selected_attack is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                
            screen.blit(background, (0, 0))
            draw_text(screen, f"{self.player.galo.name} ataca:", 50, 50)
            draw_galo(screen, self.player.galo, 50, 320, 200)
            draw_galooponnent(screen, self.opponent.galo, 500, 20, 200)
            draw_health_bars(screen, self.player.galo, self.opponent.galo)

            # exibe os ataques disponíveis
            for i, attack in enumerate(self.player.galo.attacks):
                text = f"{i + 1}. {attack['name']}"
                draw_text(screen, text, 50, 100 + i * 50)

                # verifica se o jogador clicou em algum dos ataques
                mouse_pos = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0] and 100 + i * 50 <= mouse_pos[1] <= 100 + i * 50 + 50:
                    selected_attack = attack

            pygame.display.update()

        self.selected_attack = selected_attack
        self.attack_selected = True

    def fight(self):
        clock = pygame.time.Clock()


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            screen.blit(background, (0, 0))

            if self.player_turn:
                draw_text(screen, "Sua vez de atacar", 50, 50)
                draw_galo(screen, self.player.galo, 50, 320, 200)
                draw_galooponnent(screen, self.opponent.galo, 500, 20, 200)
                draw_health_bars(screen, self.player.galo, self.opponent.galo)

                # exibe os ataques disponíveis
                for i, attack in enumerate(self.player.galo.attacks):
                    text = f"{i + 1}. {attack['name']}"
                    draw_text(screen, text, 250, 200 + i * 50)

                if not self.attack_selected:
                    self.select_attack()  # seleciona o ataque apenas uma vez
                else:
                    draw_text(
                        screen, f"Você usou {self.selected_attack['name']}", 50, 400)
                    if self.selected_attack['name'] == "Ataque Especial":
                        attack_modifier = Game.type_chart[self.player.galo.type][self.opponent.galo.type]
                    
                    else:
                       attack_modifier = 1 

                    self.opponent.galo.hp -= int(self.selected_attack['power'] * attack_modifier)

                    if self.opponent.galo.hp <= 0:
                        self.opponent.galo.hp = 0

                        screen.fill((0, 0, 0))
                        screen.blit(background, (0, 0))
                        draw_text(
                        screen, f"{self.opponent.galo.name} desmaiou e saiu de combate", 250, 50)
                        draw_galo(screen, self.player.galo, 50, 320, 200)
                        draw_galooponnent(screen, self.opponent.galo, 500, 20, 200)
                        draw_health_bars(screen, self.player.galo, self.opponent.galo)
                        draw_health_bars(screen, self.player.galo, self.opponent.galo)
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
                draw_text(screen, "Vez do oponente atacar", 50, 50)
                draw_galo(screen, self.player.galo, 50, 320, 200)
                draw_galooponnent(screen, self.opponent.galo, 500, 20, 200)
                draw_health_bars(screen, self.player.galo, self.opponent.galo)
                pygame.display.update()
                pygame.time.delay(3000)
                opponent_attack = random.choice(self.opponent.galo.attacks)
                draw_text(
                    screen, f"O oponente usou {opponent_attack['name']}", 50, 100)
                
                if opponent_attack['name'] == "Ataque Especial":
                    attack_modifier = Game.type_chart[self.opponent.galo.type][self.player.galo.type]
                else:
                    attack_modifier = 1
                    
                self.player.galo.hp -= int(opponent_attack['power'] * attack_modifier)


                if self.player.galo.hp <= 0:
                        self.player.galo.hp = 0

                        screen.fill((0, 0, 0))
                        screen.blit(background, (0, 0))
                        draw_text(
                        screen, f"{self.player.galo.name} desmaiou e saiu de combate", 50, 200)
                        draw_galo(screen, self.player.galo, 50, 320, 200)
                        draw_galooponnent(screen, self.opponent.galo, 500, 20, 200)
                        draw_health_bars(screen, self.player.galo, self.opponent.galo)
                        pygame.display.update()
                        pygame.time.delay(4000)
                        screen.fill((0, 0, 0))
                        pygame.display.update()
                        draw_text_centered(screen, "Você Perdeu!")
                        pygame.display.update()
                        pygame.time.wait(2000)
                        return
                
                draw_galo(screen, self.player.galo, 50, 320, 200)
                draw_galooponnent(screen, self.opponent.galo, 500, 20, 200)
                draw_health_bars(screen, self.player.galo, self.opponent.galo)
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
    game.opponent = game.select_opponent()

    # Loop principal do jogo
    while True:
        # Limpa a tela
        screen.fill((0, 0, 0))

        # Verifica se o jogador ou o oponente zerou a vida
        if game.player.galo.hp <= 0:
            draw_text_centered(screen, "Você Perdeu!")
            pygame.display.update()
            pygame.time.wait(10000)
            break
        elif game.opponent.galo.hp <= 0:
            draw_text_centered(screen, "Você Ganhou!")
            pygame.display.update()
            pygame.time.wait(5000)
            break

        # Seleciona o ataque e inicia a luta
        game.select_attack()
        game.fight()

    pygame.quit()



if __name__ == "__main__":
    main()
