import pygame as pg
import random

class FlappyBirds:
    # Função responsável por inicializar o jogo e as variáveis
    def __init__(self, window_size):
        # Cores que serão usadas nos botões
        self.white  = (255, 255, 255)
        self.black  = (  0,   0,   0)
        self.orange = (255, 165,   0)

        self.window = pg.display.set_mode(window_size)                          # Definindo o tamanho da tela

        pg.font.init()                                                          # Iniciando a fonte do jogo
        self.font = pg.font.SysFont("Courier New", 50, bold=True)    # Variável responsável por armazenar uma fonte específica
        self.clock = pg.time.Clock()                                            # Variável para definir o fps do jogo

        # Mouse variables
        self.last_click_status = (False, False, False)                          # Verificar quando o botão esquerdo do mouse foi clicado
        self.gravity = 5                                                        # Variável para definir a gravidade do jogo (5)
        self.in_play = False                                                    # Variável para verificar se esta rodando

        self.bird_pos = [100, 100]                                              # Variável para a posição do bird no jogo
        self.vertical_speed = 0                                                 # Velocidade vertical do bird (verificar se ele está a subir ou a descer)
        self.score = 0                                                          # Variável para armazenar a pontuação
        self.last_random_height_for_pipe = 0                                    # Variável para determinar as alturas aleatórias dos tubos
        self.bird_passing_through_obstacle = False                              # Determinar se o bird esta passando pelo tubo ou não

        # Variáveis que definem as posições dos 5 canos recebendo a posição x e a altura aleatória
        self.pipe_1_pos = [ 400, self.new_height_for_pipe()]
        self.pipe_2_pos = [ 800, self.new_height_for_pipe()]
        self.pipe_3_pos = [1200, self.new_height_for_pipe()]
        self.pipe_4_pos = [1600, self.new_height_for_pipe()]
        self.pipe_5_pos = [2000, self.new_height_for_pipe()]

        # Variáveis para o 'background' de base indo para a esquerda
        self.background_1_pos = [   0, 0]
        self.background_2_pos = [2120, 0]

        # Variáveis para a movimentação do chão indo para a esquerda
        self.ground_1_pos = [ 0, 634]
        self.ground_2_pos = [1010, 634]
        self.ground_3_pos = [2020, 634]

        # Variáveis definidas para carregar as imagens utilizadas no jogo
        background = pg.image.load('assets/Background.png')
        ground     = pg.image.load('assets/Ground.png')
        bird       = pg.image.load('assets/Bird.png')
        pipe       = pg.image.load('assets/Pipe.png')
        pipe_usd   = pg.image.load('assets/Pipe Up Side Down.png')

        # Utilizando as variáveis das imagens em escala
        self.background = pg.transform.scale(background, (2120, 634))
        self.bird       = pg.transform.scale(bird,       (  51,  36))
        self.ground     = pg.transform.scale(ground,     (1010,  86))
        self.pipe       = pg.transform.scale(pipe,       ( 123, 600))
        self.pipe_usd   = pg.transform.scale(pipe_usd,   ( 123, 600))

    # Função para verificar qual botão do mouse foi clicado
    def mouse_has_clicked(self, input) :
        if self.last_click_status == input :
            return False, False, False
        else :                                                              # Se um botão foi clicado
            left_button = False
            center_button = False
            right_button = False
            if self.last_click_status[0] == False and input[0] == True :    # Verificar botão esquerdo
                left_button = True
            if self.last_click_status[1] == False and input[1] == True :    # Verificar botão do meio
                center_button = True
            if self.last_click_status[2] == False and input[2] == True :    # Verificar botão da esquerda
                right_button = True

        return left_button, center_button, right_button                     # Retorna os status dos botões (clicados ou não)

    # Função para limpar e desenhar a tela do jogo
    def clear_window(self):
        pg.draw.rect(self.window, self.white, (0, 0, self.window.get_width(), self.window.get_height()))