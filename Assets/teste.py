from tkinter import font
import pygame
import random
from sklearn.linear_model import LogisticRegression

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
        self.attack = attack


class Player:
    def __init__(self, pokemon):
        self.pokemon = pokemon


class Game:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 16)
        self.player = Player(Pokemon("Charmander", "Fire", 100, 20))
        self.opponent = Pokemon("Bulbasaur", "Grass", 100, 20)
        if self.opponent.hp <= 0:
            hp_label = 1  # player wins the battle
        else:
            hp_label = 0  # battle continues
        self.logistic = LogisticRegression(random_state=0)
        self.logistic.fit([[self.player.pokemon.hp, self.player.pokemon.attack]], [hp_label])

    def draw_text(self, text, x, y):
        surface = self.font.render(text, True, (255, 255, 255))
        screen.blit(surface, (x, y))

    def draw_pokemon(self, pokemon, x, y):
        surface = pygame.image.load(f"{pokemon.name}.png")
        screen.blit(surface, (x, y))

    def update_screen(self):
        screen.blit(background, (0, 0))
        self.draw_pokemon(self.player.pokemon, 50, 200)
        self.draw_pokemon(self.opponent, 450, 50)
        self.draw_text(f"{self.player.pokemon.name} - {self.player.pokemon.hp} HP", 50, 180)
        self.draw_text(f"{self.opponent.name} - {self.opponent.hp} HP", 450, 30)
        pygame.display.update()

    def battle(self):
        player_attack = random.randint(1, self.player.pokemon.attack)
        opponent_attack = random.randint(1, self.opponent.attack)
        self.player.pokemon.hp -= opponent_attack
        self.opponent.hp -= player_attack
        if self.opponent.hp <= 0:
            self.draw_text("Você venceu!", 50, 50)
        elif self.player.pokemon.hp <= 0:
            self.draw_text("Você perdeu!", 50, 50)
        else:
            player_prediction = self.logistic.predict([[self.player.pokemon.hp, player_attack]])
            opponent.hp -= player_prediction[0]
        if self.opponent.hp <= 0:
            self.draw_text("Você venceu!", 50, 50)
        else:
            self.draw_text("A batalha continua!", 50, 50)
            self.update_screen()

def main():
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.battle()
        game.update_screen()
    pygame.quit()

if __name__ == "__main__":
    main()
