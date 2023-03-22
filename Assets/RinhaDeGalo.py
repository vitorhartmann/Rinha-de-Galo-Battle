import pygame
import pygame.font

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simulador de Batalhas Pokemon")


class Personagem:
    def __init__(self, nome, hp, atk, defe):
        self.nome = nome
        self.hp = hp
        self.atk = atk
        self.defe = defe


class Ataque:
    def __init__(self, nome, forca, tipo):
        self.nome = nome
        self.forca = forca
        self.tipo = tipo


class Batalha:
    def __init__(self, jogador, adversario, ataques):
        self.jogador = jogador
        self.adversario = adversario
        self.ataques = ataques



class Interface:
    def __init__(self, tela, batalha):
        self.tela = tela
        self.batalha = batalha
        self.fonte = pygame.font.SysFont(None, 30)

        self.botao1 = pygame.Rect(50, 500, 200, 50)
        self.botao2 = pygame.Rect(300, 500, 200, 50)
        self.botao3 = pygame.Rect(550, 500, 200, 50)
        self.botao4 = pygame.Rect(50, 550, 200, 50)
        self.botao5 = pygame.Rect(300, 550, 200, 50)

    def desenhar(self):
        pygame.draw.rect(self.tela, (255, 255, 255), self.botao1)
        pygame.draw.rect(self.tela, (255, 255, 255), self.botao2)
        pygame.draw.rect(self.tela, (255, 255, 255), self.botao3)
        pygame.draw.rect(self.tela, (255, 255, 255), self.botao4)
        pygame.draw.rect(self.tela, (255, 255, 255), self.botao5)

        texto_botao1 = self.fonte.render(self.batalha.ataques[0].nome, True, (0, 0, 0))
        texto_botao2 = self.fonte.render(self.batalha.ataques[1].nome, True, (0, 0, 0))
        texto_botao3 = self.fonte.render(self.batalha.ataques[2].nome, True, (0, 0, 0))
        texto_botao4 = self.fonte.render(self.batalha.ataques[3].nome, True, (0, 0, 0))
        texto_botao5 = self.fonte.render("Desistir", True, (0, 0, 0))

        self.tela.blit(texto_botao1, (self.botao1.x + 10, self.botao1.y + 10))
        self.tela.blit(texto_botao2, (self.botao2.x + 10, self.botao2.y + 10))
        self.tela.blit(texto_botao3, (self.botao3.x + 10, self.botao3.y + 10))
        self.tela.blit(texto_botao4, (self.botao4.x + 10, self.botao4.y + 10))
        self.tela.blit(texto_botao5, (self.botao5.x + 10, self.botao5.y + 10))

        texto_hp_jogador = self.fonte.render(f"{self.batalha.jogador.nome} ({self.batalha.jogador.hp})", True, (0, 0, 0))
        texto_hp_adversario = self.fonte.render(f"{self.batalha.adversario.nome} ({self.batalha.adversario.hp})", True, (0, 0, 0))
        self.tela.blit(texto_hp_jogador, (50, 450))
        self.tela.blit(texto_hp_adversario, (550, 50))

    def atualizar_mensagem_batalha(self, mensagem):
        texto_mensagem = self.fonte.render(mensagem, True, (0, 0, 0))
        self.tela.blit(texto_mensagem, (50, 250))

    def clicar_botao(self, posicao_mouse):
        if self.botao1.collidepoint(posicao_mouse):
             self.batalha.ataque_jogador(self.batalha.ataques[0])
        elif self.botao2.collidepoint(posicao_mouse):
            self.batalha.ataque_jogador(self.batalha.ataques[1])
        elif self.botao3.collidepoint(posicao_mouse):
            self.batalha.ataque_jogador(self.batalha.ataques[2])
        elif self.botao4.collidepoint(posicao_mouse):
            self.batalha.ataque_jogador(self.batalha.ataques[3])
        elif self.botao5.collidepoint(posicao_mouse):
            self.batalha.desistir()

    def mostrar_vitoria(self, mensagem):
        self.tela.fill((255, 255, 255))
        texto_mensagem = self.fonte.render(mensagem, True, (0, 0, 0))
        self.tela.blit(texto_mensagem, (250, 250))
    pygame.display.update()
    pygame.time.wait(2000)