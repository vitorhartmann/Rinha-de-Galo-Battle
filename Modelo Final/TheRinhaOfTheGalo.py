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
pygame.display.set_caption("Batalha Pokemon")
background = pygame.image.load("background.png")


class Pokemon:
    def __init__(self, name, type, hp, attack):
        self.name = name
        self.type = type
        self.hp = hp
        self.attacks = [Attack("Tackle", 10), Attack("Flame Thrower", 20)]


class Player:
    def __init__(self, pokemon):
        self.pokemon = pokemon


class Game:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 16)
        self.player = Player(Pokemon("Charmander", "Fire", 100, 20))
        self.opponent = Pokemon("Bulbasaur", "Grass", 100, 20)
        hp_label = None
        if self.opponent.hp <= 0:
            hp_label = [1]  # player wins the battle
        else:
            hp_label = [0]  # battle continues
        self.logistic = None
        if len(hp_label) > 1:
            self.logistic = LogisticRegression(random_state=0)
            self.logistic.fit([[self.player.pokemon.hp, self.player.pokemon.attack]], [hp_label])


    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 16)
        self.player = Player(Pokemon("Charmander", "Fire", 100, 20))
        self.opponent = Pokemon("Bulbasaur", "Grass", 100, 20)
        self.logistic = None
        self.selected_attack = None
        
    def select_attack(self, index):
        self.selected_attack = self.player.pokemon.attacks[index]


class Attack:
    def __init__(self, name, power):
        self.name = name
        self.power = power





def draw_text(screen, text, x, y):
    surface = font.render(text, True, (255, 255, 255))
    screen.blit(surface, (x, y))

    
def draw_pokemon(screen, pokemon, x, y):
    surface = pygame.image.load(f"{pokemon.name}.png")
    screen.blit(surface, (x, y))



def update_screen(screen, player, opponent):
    screen.blit(background, (0, 0))
    draw_pokemon(screen, player.pokemon, 50, 200)
    draw_pokemon(screen, opponent, 450, 50)
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

