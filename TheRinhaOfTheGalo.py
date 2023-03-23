from tkinter import font
import pygame
import pygame.font
import random

pygame.font.init()
font = pygame.font.SysFont("Arial", 16)


pygame.init()
width, height = 720, 640
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rinha de Galo")
background = pygame.image.load(f"Imagens/PlanoDeFundoALT.png")


class Pokemon:
    def __init__(self, name, type, hp, attack):
        self.name = name
        self.type = type
        self.hp = hp
        self.attacks = [Attack("Bater", 10), Attack("Bater mais Forte", 20)]


class Player:
    def __init__(self, pokemon):
        self.pokemon = pokemon


class Game:
    def __init__(self):
        self.player = None
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
            pokemon1_rect = draw_pokemon(screen, pokemon1, 150, 100, 100)

            pokemon2 = Pokemon("Galo de Calca", "Calca", 100, 20)
            pokemon2_rect = draw_pokemon(screen, pokemon2, 300, 100, 100)

            pokemon3 = Pokemon("Galo de Tenis", "Tenis", 100, 20)
            pokemon3_rect = draw_pokemon(screen, pokemon3, 450, 100, 100)

            # Verifica a posição do mouse
            mouse_pos = pygame.mouse.get_pos()

            # Verifica se está em cima de um pokemon, e exibe as informações
            if pokemon1_rect.collidepoint(mouse_pos):
                pokemon_info_text = f"{pokemon1.name}"
                tipopokemon = f"Tipo:{pokemon1.type}"
                dicadetipos = f"Ótimo contra tipo {pokemon2.type} "
            elif pokemon2_rect.collidepoint(mouse_pos):
                pokemon_info_text = f"{pokemon2.name}"
                tipopokemon = f"Tipo:{pokemon2.type}"
                dicadetipos = f"Ótimo contra tipo {pokemon3.type} "
            elif pokemon3_rect.collidepoint(mouse_pos):
                pokemon_info_text = f"{pokemon3.name}"
                tipopokemon = f"Tipo:{pokemon3.type}"
                dicadetipos = f"Ótimo contra tipo {pokemon1.type} "
            else:
                pokemon_info_text = ""
                tipopokemon = ""
                dicadetipos = ""

            # Posição da Informação (Nome)
            draw_text(screen, pokemon_info_text, 310, 330)

            # Posição da Informação (Tipo)
            draw_text(screen, tipopokemon, 320, 350)

            # Posição da Informação (Dica de Vantagem)
            draw_text(screen, dicadetipos, 290, 380)

            

            # Quando clica com o mouse na posição das imagens dos galos, ele seleciona
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0]:
                if pokemon1_rect.collidepoint(mouse_pos):
                    selected_pokemon = pokemon1
                elif pokemon2_rect.collidepoint(mouse_pos):
                    selected_pokemon = pokemon2
                elif pokemon3_rect.collidepoint(mouse_pos):
                    selected_pokemon = pokemon3


            
            

            # Atualiza a tela
            pygame.display.update()

        # Define o pokemon do jogador pelo escolhido
        self.player = Player(selected_pokemon)

        # Verificação da "IA", que sempre escolhe o galo com melhor vantagem contra o escolhido do jogador
        if selected_pokemon == pokemon1:

            self.opponent = Pokemon(
                "Galo de Tenis", "Tênis", 100, 20)
        elif selected_pokemon == pokemon2:
            self.opponent = Pokemon(
                "Galo de Arma", "Arma", 100, 20)
        elif selected_pokemon == pokemon3:
            self.opponent = Pokemon(
                "Galo de Calca", "Calça", 100, 20)
        else:
            self.opponent = Pokemon(
                "Galo de Arma", "Arma", 100, 20)
            


         # Pausa aleatória para o oponente escolher o pokemon

        delay_time = (750)  # Delay Pra "animação" de escolha
        draw_text(screen, "Oponente escolhendo.", 50, 570)
        pygame.display.update()
        pygame.time.delay(delay_time)

        delay_time =  (750)  # Delay Pra "animação" de escolha
        draw_text(screen, "Oponente escolhendo..", 50, 570)
        pygame.display.update()
        pygame.time.delay(delay_time)

        delay_time = random.randint(750, 1500)  # Delay Pra "animação" de escolha
        draw_text(screen, "Oponente escolhendo...", 50, 570)
        pygame.display.update()
        pygame.time.delay(delay_time)



    def select_attack(self, index):
        self.selected_attack = self.player.pokemon.attacks[index]


class Attack:
    def __init__(self, name, power):
        self.name = name
        self.power = power


def draw_text(screen, text, x, y):
    surface = font.render(text, True, (255, 255, 255))
    screen.blit(surface, (x, y))

# Definição de onde renderizar a foto do galo do jogador, e de onde pegar a imagem


def draw_pokemon(screen, pokemon, x, y, size):
    image = pygame.image.load(f"Imagens/{pokemon.name}.png")
    image = pygame.transform.scale(image, (size, size))
    screen.blit(image, (x, y))
    return pygame.Rect(x, y, image.get_width(), image.get_height())

# Definição de onde renderizar a foto do galo do oponente, e de onde pegar a imagem


def draw_pokemonoponnent(screen, pokemon, x, y, size):
    image = pygame.image.load(f"Imagens/{pokemon.name} Oponente.png")
    image = pygame.transform.scale(image, (size, size))
    screen.blit(image, (x, y))
    return pygame.Rect(x, y, image.get_width(), image.get_height())


def update_screen(screen, player, opponent):
    screen.blit(background, (0, 0))
    draw_pokemon(screen, player.pokemon, 50, 200, 150)
    draw_pokemonoponnent(screen, opponent, 450, 50, 150)
    draw_text(
        screen, f"{player.pokemon.name} - {player.pokemon.hp} HP", 50, 180)
    draw_text(screen, f"{opponent.name} - {opponent.hp} HP", 450, 30)
    pygame.display.update()

# BATALHA - A SER PROGRAMADA AINDA


def battle(player, opponent, selected_attack):
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
                        battle(game.player, game.opponent,
                               game.logistic, game.selected_attack)
        update_screen(screen, game.player, game.opponent)
    pygame.quit()


if __name__ == "__main__":
    main()
