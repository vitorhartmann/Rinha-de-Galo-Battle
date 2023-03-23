from tkinter import font
import pygame
import pygame.font
import random
from sklearn.linear_model import LogisticRegression

pygame.font.init()
font = pygame.font.SysFont("Arial", 16)


pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rinha de Galo")
background = pygame.image.load("PlanoDeFundoALT.png")


class Pokemon:
    def __init__(self, name, type, hp, attack):
        self.name = name
        self.type = type
        self.hp = hp
        self.attacks = [Attack("Bater", 10), Attack("Bater mais Forte", 20)]


class Player:
    def __init__(self, pokemon):
        self.pokemon = pokemon


class Opponent:
    def __init__(self, player_pokemon):
        self.types = {'Arma': 'Tenis', 'Calca': 'Arma', 'Tenis': 'Calca'}
        self.pokemon = self.choose_pokemon(player_pokemon)

    


class Game:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 16)
        self.player = None
        # self.opponent = Pokemon("Galo de Tenis", "Normal", 100, 20)
        self.opponent = None
    
        
       
        

    def select_pokemon(self):
        selected_pokemon = None
        while selected_pokemon is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    

            screen.blit(background, (0, 0))
            draw_text(screen, "Selecione seu Galo de Briga:", 50, 50)

            # exibe as imagens dos pokemons disponíveis
            
            
            pokemon1 = Pokemon("Galo de Arma", "Arma", 100, 20)
            draw_text(screen, f"{pokemon1.name} - Tipo: {pokemon1.type}", 40, 180)
            draw_pokemon(screen, pokemon1, 50, 100, 100)

            pokemon2 = Pokemon("Galo de Calca", "Calca", 100, 20)
            draw_text(screen, f"{pokemon2.name} - Tipo: {pokemon2.type}", 240, 180)
            draw_pokemon(screen, pokemon2, 200, 100, 100)

            pokemon3 = Pokemon("Galo de Tenis", "Tenis", 100, 20)
            draw_text(screen, f"{pokemon3.name} - Tipo: {pokemon3.type}", 440, 180)
            draw_pokemon(screen, pokemon3, 350, 100, 100)

            # verifica se o jogador selecionou um pokemon
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0]:
                if 50 < mouse_pos[0] < 150 and 100 < mouse_pos[1] < 200:
                    selected_pokemon = pokemon1
                elif 200 < mouse_pos[0] < 300 and 100 < mouse_pos[1] < 200:
                    selected_pokemon = pokemon2
                elif 350 < mouse_pos[0] < 450 and 100 < mouse_pos[1] < 200:
                    selected_pokemon = pokemon3

            pygame.display.update()

        self.player = Player(selected_pokemon)

       

        if selected_pokemon == pokemon1:
            self.opponent = Pokemon("Galo de Tenis", "Tenis", 100, 20)
        elif selected_pokemon == pokemon2:
            self.opponent = Pokemon("Galo de Arma", "Arma", 100, 20)
        elif selected_pokemon == pokemon3:
            self.opponent = Pokemon("Galo de Calca", "Calca", 100, 20)
        else:
            self.opponent = Pokemon("Galo de Arma", "Arma", 100, 20)
    

    
        
    def select_attack(self, index):
        self.selected_attack = self.player.pokemon.attacks[index]


class Attack:
    def __init__(self, name, power):
        self.name = name
        self.power = power





def draw_text(screen, text, x, y):
    surface = font.render(text, True, (255, 255, 255))
    screen.blit(surface, (x, y))

    
def draw_pokemon(screen, pokemon, x, y, size):
    surface = pygame.image.load(f"{pokemon.name}.png")
    surface = pygame.transform.scale(surface, (size, size))
    screen.blit(surface, (x, y))



def update_screen(screen, player, opponent):
    screen.blit(background, (0, 0))
    draw_pokemon(screen, player.pokemon, 50, 200, 150)
    draw_pokemon(screen, opponent, 450, 50, 150)
    draw_text(screen, f"{player.pokemon.name} - {player.pokemon.hp} HP", 50, 180)
    draw_text(screen, f"{opponent.name} - {opponent.hp} HP", 450, 30)
    pygame.display.update()





def battle(player, opponent, logistic, selected_attack):
    player_attack = selected_attack.power
    opponent_attack = random.randint(1, opponent.attack)
    player.pokemon.hp -= opponent_attack
    opponent.hp -= player_attack
    if opponent.hp <= 0:
        draw_text(screen, "Você venceu!", 50, 50)
    elif player.pokemon.hp <= 0:
        draw_text(screen, "Você perdeu!", 50, 50)
    else:
        opponent_attack = random.choice(opponent.attacks)
        player.pokemon.hp -= opponent_attack.power
        if player.pokemon.hp <= 0:
            draw_text(screen, "Você perdeu!", 50, 50)
        else:
            draw_text(screen, "A batalha continua!", 50, 50)
            update_screen(screen, player, opponent)


def main():
    game = Game()
    game.select_pokemon()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game.select_attack(0)
                elif event.key == pygame.K_2:
                    game.select_attack(1)
                elif event.key == pygame.K_SPACE:
                    if game.selected_attack is not None:
                        battle(game.player, game.opponent, game.logistic, game.selected_attack)
        update_screen(screen, game.player, game.opponent)
    pygame.quit()


if __name__ == "__main__":
    main()

