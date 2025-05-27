import pygame as pg
import random
import time

class Snake_Game:
    def __init__(self):
        """Fields (variaveis) essenciais para o funcionamento do jogo."""
        
        #Cores usadadas no jogo.
        self.color = {
            'black': (  0,   0,   0),
            'gray':  (150, 150, 150),
            'white': (255, 255, 255),
            'red':   (218, 73, 141),
            'green': (105, 36, 124),
            'blue':  (  0,   0, 255)
        }
        #Usado para escrever texto dentro do jogo.
        pg.font.init()
        self.font = pg.font.SysFont("Courier New", 50, bold=True)

        #Tamanho e representação da tela do jogo
        self.map_size = (53, 30) 
        self.map = [['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']]
        
        #"Coordenadas" para localizar a posição da maçã e da cobrinha.
        self.apple_position = (10, 10)
        self.snake_position = [(41, 20), (41, 21), (41, 22), (41, 23), (42, 23), (43, 23)]
        self.snake_direction = (-1, 0)
        
        #Variáveis para implementar na dinâmica do jogo.
        self.score = 0
        self.countdown = 3
        self.end_game = False

        #Responsáveis por responder caso uma tecla seja pressionada.
        self.key_pressed = False
        self.key_pressed_log = ''

    def snake_change_direction(self, key):
        """Faz a checagem de qual tecla foi pressionada, em conjunto de outra checagem
           para conferir se a cobrinha não está em uma posição oposta. """
        if (key == 'w' or key == 'up') and self.snake_direction != (0, 1):
            self.snake_direction = (0, -1)
        elif (key == 'a' or key == 'left') and self.snake_direction != (1, 0):
            self.snake_direction = (-1, 0)
        elif (key == 's' or key == 'down') and self.snake_direction != (0, -1):
            self.snake_direction = (0, 1)
        elif (key == 'd' or key == 'right') and self.snake_direction != (-1, 0):
            self.snake_direction = (1, 0)

    def game_start_countdown(self, window):
        """Desenha um círculo com a contagem regressiva para o início do jogo."""
        pg.draw.circle(window, self.color['white'], (636, 360), 50)

        if self.countdown == 3:
            countdown_text = self.font.render('3', True, self.color['black'])
            window.blit(countdown_text, (620, 336))
            self.countdown -= 1
        elif self.countdown == 2:
            countdown_text = self.font.render('2', True, self.color['black'])
            window.blit(countdown_text, (620, 336))
            self.countdown -= 1
        elif self.countdown == 1:
            countdown_text = self.font.render('1', True, self.color['black'])
            window.blit(countdown_text, (620, 336))
            self.countdown -= 1
        elif self.countdown == 0:
            countdown_text = self.font.render('Go!', True, self.color['black'])
            window.blit(countdown_text, (595, 336))
            self.countdown -= 1

        pg.display.update()
        time.sleep(1)

    def draw_map_elements(self, window):
        """Desenha todos os elementos que estão dentro da matriz map.
            s = snake (cobrinha);
            a = apple (maçã). """
        side = window.get_height() / self.map_size[1]

        for y in range(self.map_size[1]):
            for x in range(self.map_size[0]):
                if self.map[y][x] == 's':
                    pg.draw.rect(window, self.color['green'], (x * side , y * side, side, side))
                if self.map[y][x] == 'a':
                    pg.draw.rect(window, self.color['red'], (x * side , y * side, side, side))

    def update_snake_position(self, snake):
        """Atualiza a localização da cobrinha em relação à variável "snake.direction" """
        snake_size = len(snake) - 1        
        for i in range(len(snake)):
            if snake_size - i == 0:
                self.snake_position[0] = (self.snake_position[0][0] + self.snake_direction[0], self.snake_position[0][1] + self.snake_direction[1])
            else:
                self.snake_position[snake_size - i] = self.snake_position[snake_size - i - 1]

    def sort_apple_position(self):
        """Sorteia uma nova posição para a maçã."""
        map_x = len(self.map[0])
        map_y = len(self.map)
        x = random.randint(0, map_x - 1)
        y = random.randint(0, map_y - 1)
        self.apple_position = (x, y)

    def clear_map(self, target_map):
        """Percorre a matriz do mapa do jogo, inserindo uma string vazia para "limpar" """
        for y in range(len(target_map)):
            for x in range(len(target_map[0])):
                target_map[y][x] = ''

    def add_snake_position(self, map_size, snake):
        """Insere a string 's' onde a cobrinha está localizada na matriz."""
        for y in range(map_size[1]):
            for x in range(map_size[0]):
                for s in range(len(snake)):
                    if snake[s][0] == x and snake[s][1] == y:
                        self.map[y][x] = 's'

    def add_apple_position(self, map_size, apple):
        """Percorre o mapa e insere a letra 'a'."""
        for y in range(map_size[1]):
            for x in range(map_size[0]):
                if y == apple[1] and x == apple[0]:
                    self.map[y][x] = 'a'

    def snake_get_apple(self):
        """Verifica se a cobrinha está na mesma posição da maçã."""
        if self.snake_position[0] == self.apple_position:
            self.snake_position.append(self.snake_position[len(self.snake_position) - 1])
            self.sort_apple_position()
            self.score += 1

    def draw_score(self, window):
        """Desenha o score na tela."""
        score_text = self.font.render('Score: ' + str(self.score), True, self.color['white'])
        window.blit(score_text, (0, 0))

    def end_of_game(self):
        """Verifica se o jogo chegou a fim -> se a cobrinha colidiu consigo mesma ou com a beirada da tela de jogo."""
        if self.snake_position[0][0] < 0 or self.snake_position[0][1] < 0 or self.snake_position[0][0] > self.map_size[0] - 1 or self.snake_position[0][1] > self.map_size[1] - 1:
            self.end_game = True

        for i in range(1, len(self.snake_position)):
            if self.snake_position[0] == self.snake_position[i]:
                self.end_game = True

    def draw_end_game(self, window):
        """Desenha game over na tela"""
        if self.end_game == True:
            score_text = self.font.render('Game Over', True, self.color['white'])
            window.blit(score_text, (525, 336))

    def reset_game(self):
        """Acionada ao pressionar o botão restart. Reinicia as variáveis do jogo."""
        self.end_game = False
        self.score = 0
        self.snake_position = [(40, 20), (41, 20), (41, 21), (41, 22), (41, 23), (42, 23)]
        self.apple_position = (10, 10)
        self.snake_direction = (-1, 0)
