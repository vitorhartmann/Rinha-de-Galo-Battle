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
    def __init__(self, name, type, hp, attack):
        self.name = name
        self.type = type
        self.hp = hp

    def attack(self, target, attack_index):
        attack = self.attacks[attack_index]
        target.hp -= attack.power


class Player:
    def __init__(self, galo):
        self.galo = galo


class Game:
    def __init__(self):
        self.player = None
        self.opponent = None
        self.player_turn = True
        self.attack_selected = False
        self.selected_attack = None








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

            # Verifica a posição do mouse
            mouse_pos = pygame.mouse.get_pos()

            # Verifica se está em cima de um galo, e exibe as informações
            if galo1_rect.collidepoint(mouse_pos):
                galo_info_text = f"{galo1.name}"
                tipogalo = f"Tipo:{galo1.type}"
                dicadetipos = f"Ótimo contra tipo {galo2.type} "
                
            elif galo2_rect.collidepoint(mouse_pos):
                galo_info_text = f"{galo2.name}"
                tipogalo = f"Tipo:{galo2.type}"
                dicadetipos = f"Ótimo contra tipo {galo3.type} "

            elif galo3_rect.collidepoint(mouse_pos):
                galo_info_text = f"{galo3.name}"
                tipogalo = f"Tipo:{galo3.type}"
                dicadetipos = f"Ótimo contra tipo {galo1.type} "

            else:
                galo_info_text = ""
                tipogalo = ""
                dicadetipos = ""

            # Posição da Informação (Nome)
            draw_text(screen, galo_info_text, 310, 330)

            # Posição da Informação (Tipo)
            draw_text(screen, tipogalo, 320, 350)

            # Posição da Informação (Dica de Vantagem)
            draw_text(screen, dicadetipos, 290, 380)

            

            # Quando clica com o mouse na posição das imagens dos galos, ele seleciona o galo
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0]:
                if galo1_rect.collidepoint(mouse_pos):
                    selected_galo = galo1
                elif galo2_rect.collidepoint(mouse_pos):
                    selected_galo = galo2
                elif galo3_rect.collidepoint(mouse_pos):
                    selected_galo = galo3


            
            

            # Atualiza a tela
            pygame.display.update()

        # Define o galo do jogador pelo escolhido
        self.player = Player(selected_galo)

        # Verificação da "IA", que sempre escolhe o galo com melhor vantagem contra o escolhido do jogador
        if selected_galo == galo1:

            self.opponent = Galo(
                "Galo de Tenis", "Tênis", 100, 20)
        elif selected_galo == galo2:
            self.opponent = Galo(
                "Galo de Arma", "Arma", 100, 20)
        elif selected_galo == galo3:
            self.opponent = Galo(
                "Galo de Calca", "Calça", 100, 20)
        else:
            self.opponent = Galo(
                "Galo de Arma", "Arma", 100, 20)
            


         # Pausa aleatória para o oponente escolher o galo

        delay_time = random.randint(750, 1500)  # Delay Pra "animação" de escolha, entre 0,75 segundos e 1,5 segundos
        draw_text(screen, "Oponente escolhendo.", 300, 570)  #Posição de onde vai aparecer, X E Y
        pygame.display.update()
        pygame.time.delay(delay_time)

        delay_time = random.randint(750, 1500)  # Delay Pra "animação" de escolha, entre 0,75 segundos e 1,5 segundos
        draw_text(screen, "Oponente escolhendo..", 300, 570)   #Posição de onde vai aparecer, X E Y
        pygame.display.update()
        pygame.time.delay(delay_time)

        delay_time = random.randint(750, 1500)  # Delay Pra "animação" de escolha, entre 0,75 segundos e 1,5 segundos
        draw_text(screen, "Oponente escolhendo...", 300, 570)  #Posição de onde vai aparecer, X E Y
        pygame.display.update()
        pygame.time.delay(delay_time)

   

           

        


    



# Renderizando o texto na tela, conforme identificado anteriormente (X e Y), nas variaveis
def draw_text(screen, text, x, y):
    surface = font.render(text, True, (255, 255, 255))
    screen.blit(surface, (x, y))

# Definição de onde renderizar a foto do galo do jogador, e de onde pegar a imagem


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
    return pygame.Rect(x, y, image.get_width(), image.get_height())


def update_screen(screen, player, opponent):
    screen.blit(background, (0, 0))
    draw_galo(screen, player.galo, 50, 200, 150)
    draw_galooponnent(screen, opponent, 450, 50, 150)
    draw_text(
        screen, f"{player.galo.name} - {player.galo.hp} HP", 50, 180)
    draw_text(screen, f"{opponent.name} - {opponent.hp} HP", 450, 30)
    pygame.display.update()

# BATALHA - A SER PROGRAMADA AINDA





def main():
    game = Game()
    game.select_galo()
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
                        (game.player, game.opponent,
                               game.logistic, game.selected_attack)
        update_screen(screen, game.player, game.opponent)
    pygame.quit()


if __name__ == "__main__":
    main()
