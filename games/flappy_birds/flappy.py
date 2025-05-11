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

    # Função responsável por desenhar cada imagem na tela do jogo conforme a sua posição
    def board(self) :
        # Imagem de plano de fundo (2)
        self.window.blit(self.background, (self.background_1_pos[0], self.background_1_pos[1]))
        self.window.blit(self.background, (self.background_2_pos[0], self.background_2_pos[1]))

        # Imagem dos canos (5)
        self.window.blit(self.pipe,     (self.pipe_1_pos[0], self.pipe_1_pos[1]))
        self.window.blit(self.pipe_usd, (self.pipe_1_pos[0], self.pipe_1_pos[1] - 800))
        self.window.blit(self.pipe,     (self.pipe_2_pos[0], self.pipe_2_pos[1]))
        self.window.blit(self.pipe_usd, (self.pipe_2_pos[0], self.pipe_2_pos[1] - 800))
        self.window.blit(self.pipe,     (self.pipe_3_pos[0], self.pipe_3_pos[1]))
        self.window.blit(self.pipe_usd, (self.pipe_3_pos[0], self.pipe_3_pos[1] - 800))
        self.window.blit(self.pipe,     (self.pipe_4_pos[0], self.pipe_4_pos[1]))
        self.window.blit(self.pipe_usd, (self.pipe_4_pos[0], self.pipe_4_pos[1] - 800))
        self.window.blit(self.pipe,     (self.pipe_5_pos[0], self.pipe_5_pos[1]))
        self.window.blit(self.pipe_usd, (self.pipe_5_pos[0], self.pipe_5_pos[1] - 800))

        # Imagem da grama (3)
        self.window.blit(self.ground, (self.ground_1_pos[0], self.ground_1_pos[1]))
        self.window.blit(self.ground, (self.ground_2_pos[0], self.ground_2_pos[1]))
        self.window.blit(self.ground, (self.ground_3_pos[0], self.ground_3_pos[1]))

        # Imagem do passáro (1)
        self.window.blit(self.bird, (self.bird_pos[0], self.bird_pos[1]))

    # Função responsável pelo comando de movimentação e de ‘restart’
    def move(self, key) :
        if key == 'space' :
            # Para conseguir movimentar o passáro para cima (eixo y) é preciso colocar uma velocidade negativa
            self.vertical_speed = -7
        elif key == 'r' :
            self.restart()

    # Função responsável por definir alturas aleatórias para os canos sem repetir
    def new_height_for_pipe(self) :
        new_height = random.randint(6, 10) * 50               # Altura nova aleatória

        while self.last_random_height_for_pipe == new_height :      # While para impedir que a altura nova seja igual à última altura criada
            new_height = random.randint(6, 10) * 50

        self.last_random_height_for_pipe = new_height               # Atualizando a altura da última peça com a nova
        return new_height

    # Função responsável por dar movimento a todos os elementos do jogo (canos, grama, background e passáro)
    def movement(self) :
        print(self.in_play)
        if self.in_play :  # Se o jogo foi iniciado
            # Canos - movimentados 1.2 pixels para a esquerda a cada frame
            self.pipe_1_pos[0] -= 1.2
            self.pipe_2_pos[0] -= 1.2
            self.pipe_3_pos[0] -= 1.2
            self.pipe_4_pos[0] -= 1.2
            self.pipe_5_pos[0] -= 1.2

            if self.pipe_1_pos[0] <= -123 :  # Verificar se o primeiro tudo esta fora da tela
                # Alternando as posições (x e y) dos tubos para a esquerda
                self.pipe_1_pos[0] = self.pipe_2_pos[0]
                self.pipe_1_pos[1] = self.pipe_2_pos[1]
                self.pipe_2_pos[0] = self.pipe_3_pos[0]
                self.pipe_2_pos[1] = self.pipe_3_pos[1]
                self.pipe_3_pos[0] = self.pipe_4_pos[0]
                self.pipe_3_pos[1] = self.pipe_4_pos[1]
                self.pipe_4_pos[0] = self.pipe_5_pos[0]
                self.pipe_4_pos[1] = self.pipe_5_pos[1]
                self.pipe_5_pos[0] = 1877                           # Novo cano que precisa ser adicionado (eixo x) a direita
                self.pipe_5_pos[1] = self.new_height_for_pipe()     # Chamando a função para a altura aleatória

            # Background - movimentado 1.2 pixels para esquerda a cada frame
            self.background_1_pos[0] -= 1.2
            self.background_2_pos[0] -= 1.2
            if self.background_1_pos[0] <= -2120 :  # Verifica se ele saiu da tela
                self.background_1_pos[0] = 0
                self.background_2_pos[0] = 2120

            # Grama - movimentada 1.2 pixels para a esquerda a cada frame
            self.ground_1_pos[0] -= 1.2
            self.ground_2_pos[0] -= 1.2
            self.ground_3_pos[0] -= 1.2
            if self.ground_1_pos[0] <= -1010 :  # verifica se saiu da tela
                self.ground_1_pos[0] = 0
                self.ground_2_pos[0] = 1010
                self.ground_3_pos[0] = 2020

        # Passáro - atualizando a velocidade com limite de 5
        if self.vertical_speed <= 5 :
            self.vertical_speed += self.gravity / 15
        self.bird_pos[1] += self.vertical_speed

    # Função que desenha e atualiza o campo da pontuação
    def scoreboard(self) :
        # Se o passáro conseguir passar pelo cano nessas circunstâncias
        if self.pipe_1_pos[0] < self.bird_pos[0] + 51 and self.pipe_1_pos[0] + 123 > self.bird_pos[0]:
            self.bird_passing_through_obstacle = True                     # Está a passar
        else :
            if self.bird_passing_through_obstacle :                       # Adiciona mais um ponto
                self.score += 1

        self.bird_passing_through_obsacle = False                         # Não está a passar

        # Variáveis para desenhar o placar
        border = 5
        x = 1100
        y = 50
        height = 100
        width = 150

        text = self.font.render(str(self.score), 1, self.white)  # Escrevendo o valor da pontuação
        # Calculo para que o texto fique centralizado
        text_x = (x + (width / 2) - (text.get_width() / 2))
        text_y = (y + (height / 2) - (text.get_height() / 2))

        # Desenhando o quadrado e as bordas
        pg.draw.rect(self.window, self.orange, (x, y, width, height))
        pg.draw.rect(self.window, self.black,  (x, y, width, height), border)
        pg.draw.rect(self.window, self.white,  (x + border, y + border, width - (border * 2), height - (border * 2)), border)
        self.window.blit(text, (text_x, text_y))

    # Função verificar se esta acontecendo uma colisão
    def collision(self) :
        # Verificar se o passáro esta numa posição (x e y) que possui canos
        if self.pipe_1_pos[0] < self.bird_pos[0] + 51 and self.pipe_1_pos[0] + 123 > self.bird_pos[0] :
            # Verificar se as bordas da imagem do passaro estão em contato com o cano
            if self.bird_pos[1] + 36 > self.pipe_1_pos[1] or self.bird_pos[1] < self.pipe_1_pos[1] - 200 :
                self.in_play = False    # Para o jogo

        # Verifica se o passáro colidiu com o chão
        if self.bird_pos[1] + 36 > 634 :
            self.in_play = False        # Para o jogo