import pygame as pg
import random
import time

class Tetris:

    def __init__(self, window_size):
        #seta a tela do jogo como uma janela com 14 colunas e 20 linhas
        self.window = pg.display.set_mode((window_size*14,window_size*20)) 

        #fonte
        pg.font.init()
        self.font = pg.font.SysFont("Courier New", window_size, bold=True)

        #define o fps do jogo -> 60 frames por segundo
        self.clock = pg.time.Clock()
        #velocidade da queda das pecas
        self.time = 0

        #cores;
        #algumas cores possuem um color code especifico -> ajuda no desenho das pecas
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.gray = (150,150,150)
        self.purple = (171,57,219)
        self.blue = (23,31,223)
        self.light_blue = (3,133,166)
        self.red = (246,51,73)
        self.orange = (250,123,21)
        self.yellow = (245,198,42)
        self.green = (99,209,21)

        #variavel do mouse 
        self.last_click_status = (False, False, False)

        #outras variaveis
        self.starting_first_game = True #identifica o inicio do jogo para sortear as formas 
        self.show_restart_button = True #aparece o botao de restart
        self.board_square = window_size #tamanho dos quadrados
        self.next_shapes_list = ['', '', '', ''] #as proximas formas que vao aparecer no jogo
        self.score = 0 
        self.speed = 1
        self.selected_form = 'shape_1' #forma em jogo
        self.shape_pos = [4,0] #posicao da selected_form
        self.shape_matrix = [[]] #matriz que define o formato da forma 
        self.new_shape = True #define quando uma nova forma deve ser inserida no jogo

        #formato das pecas

        self.shape = {
            'shape_1': {
                'shape':[[1, 1],
                         [1, 1]],
                'color': self.yellow
            },
            'shape_2': {
                'shape': [[0, 1, 0],
                          [1, 1, 1]],
                'color': self.purple
            },
            'shape_3': {
                'shape': [[1, 1, 1, 1]],
                'color': self.light_blue
            },
            'shape_4': {
                'shape': [[1, 1, 0],
                          [0, 1, 1]],
                'color': self.red
            },
            'shape_5': {
                'shape': [[0, 1, 1],
                          [1, 1, 0]],
                'color': self.green
            },
            'shape_6': {
                'shape': [[1, 0, 0],
                          [1, 1, 1]],
                'color': self.blue
            },
            'shape_7': {
                'shape': [[0, 0, 1],
                          [1, 1, 1]],
                'color': self.orange
            }
        }
        
        #define os quadrados preenchidos do jogo; de inicio, é uma matriz vazia. ao percorrer do jogo essa area vazia eépreenchida pelo color code da cor colorida
        self.map = [['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', '']]
        

    #limpa o ultimo desenho feito
    def clear_window(self):
        pg.draw.rect(self.window, self.black, (0, 0, self.window.get_width(), self.window.get_height()))

    #define uma tupla para saber qual botao foi clicado (esquerdo, centro, direito)
    def mouse_has_clicked(self, input):
        if self.last_click_status == input:
            return (False, False, False)
        else:
            left_button = False
            center_button = False
            right_button = False
            if self.last_click_status[0] == False and input[0] == True:
                left_button = True
            if self.last_click_status[1] == False and input[1] == True:
                center_button = True
            if self.last_click_status[2] == False and input[2] == True:
                right_button = True
            
            return (left_button, center_button, right_button)

    #desenha a tela de jogo
    def board(self):
        #desenha a grade do jogo
        for y in range(20):
            for x in range(10):
                pg.draw.rect(self.window, self.gray, (self.board_square*x, self.board_square*y, self.board_square, self.board_square), 1)
        pg.draw.rect(self.window, self.white, (0, 0, self.board_square*10, self.board_square*20), 2)

        #forma em jogo
        self.draw_shapes_in_game()

        #'caixa' da proxima forma
        self.text_box('Next', 10, 0, 4, 1, True)
        self.text_box('', 10, 1, 4, 13, False)
        self.draw_next_shapes()
        
        #'caixa' do placar
        self.text_box('Score', 10, 14, 4, 1, True)
        self.text_box(str(self.score), 10, 15, 4, 2, False)

        #'caixa' da velocidade
        self.text_box('Speed', 10, 17, 4, 1, True)
        self.text_box(str(self.speed) + 'x', 10, 18, 4, 2, False)

    def text_box(self, text, x, y, width, height, background_fill):
        next_square_x = self.board_square * x
        next_square_y = self.board_square * y
        next_square_w = self.board_square * width
        next_square_h = self.board_square * height
        if background_fill:
            pg.draw.rect(self.window, self.white, (next_square_x, next_square_y, next_square_w, next_square_h))
            next_text = self.font.render(text, 1, self.black)
        else:
            pg.draw.rect(self.window, self.white, (next_square_x, next_square_y, next_square_w, next_square_h), 1)
            next_text = self.font.render(text, 1, self.white)
        next_text_w = next_text.get_width()
        next_text_h = next_text.get_height()
        blit_x = next_square_x + ((next_square_w/2) - (next_square_w/2))
        blit_y = next_square_y + ((next_square_h/2) - (next_square_h/2))
        self.window.blit(next_text, (blit_x, blit_y))

    #retorna uma forma aleatoria para ser adicioonada no jogo
    def new_random_shape(self):
        return 'shape_' + str(random.randint(1, 7))
    
    def add_random_shape(self):
        for i in range(len(self.next_shapes_list)):
            if i != 0:
                self.next_shapes_list[i - 1] = self.next_shapes_list[i]
        self.next_shapes_list[-1] = self.new_random_shape()

    def init_random_shapes(self):
        for i in range(4):
            self.next_shapes_list[i] = self.new_random_shape()

    #decide quais as proximas formas que serao desenhadas apos posicionar a forma em jogo
    def draw_next_shapes(self):
        for i in range(len(self.next_shapes_list)):
            next_shape_code = self.next_shapes_list[i]
            next_shape_x = self.board_square * 12 - ((len(self.shape[next_shape_code]['shape'][0])/2) * self.board_square)
            next_shape_y = self.board_square * 3 - ((len(self.shape[next_shape_code]['shape'])/2) * self.board_square) + (i*3*self.board_square)
            border_color = tuple(min(rgb+50,255) for rgb in self.shape[next_shape_code]['color'])
            for y in range(len(self.shape[next_shape_code]['shape'])):
                for x in range(len(self.shape[next_shape_code]['shape'][0])):
                    if self.shape[next_shape_code]['shape'][y][x] == 1:
                        pos_x = (self.board_square * x) + next_shape_x
                        pos_y = (self.board_square * y) + next_shape_y
                        pg.draw.rect(self.window, self.shape[next_shape_code]['color'], (pos_x, pos_y, self.board_square, self.board_square))
                        pg.draw.rect(self.window, border_color, (pos_x, pos_y, self.board_square, self.board_square), 1)

    #coloca a forma que esta na 'caixa' proxima no jogo
    def get_next_shape(self):
        self.selected_form = self.next_shapes_list[0] #pega o item 0 da lista
        self.shape_matrix = self.shape[self.selected_form]['shape'] #volta pro dic shape e seleciona a forma
        self.add_random_shape() #adiciona uma lista nova
        self.new_shape = False
        self.shape_pos = [4, 0] #coloca a nova forma no topo da tela

    #determina se a forma esta colidindo com outra
    def did_shape_collide_sideways(self):
        shape_pos_x = self.shape_pos[0]
        shape_pos_y = self.shape_pos[1]
        for y in range(len(self.shape_matrix)): #faz uma varredura para ver se a forma ocupa um mesmo quadrado do que outra. ou seja, colidiu com outra forma.
            for x in range(len(self.shape_matrix[0])):
                if self.shape_matrix[y][x] == 1:
                    shape_unit_pos_x = shape_pos_x + x
                    shape_unit_pos_y = shape_pos_y + y
                    if self.map[shape_unit_pos_y][shape_unit_pos_x] == '':
                        pass
                    else: 
                        return True
        return False

    #confere se a forma saiu da tela do jogo
    def is_shape_in_the_game(self):
        shape_pos_x = self.shape_pos[0]
        for y in range(len(self.shape_matrix)):
            for x in range(len(self.shape_matrix[0])):
                if self.shape_matrix[y][x] == 1:
                    shape_unit = shape_pos_x + x
                    if shape_unit >= 0 and shape_unit <= 9:
                        pass
                    else:
                        return False
        return True

    #rotaciona a forma para o sentido horario
    def rotate_shape_to_the_right(self):
        transpose_matrix = list(zip(*self.shape_matrix))

        self.shape_matrix = [list(row[::-1]) for row in transpose_matrix]

    #rotaciona a forma para o sentido anti horario
    def rotate_shape_to_the_left(self):
        transpose_matrix = list(zip(*self.shape_matrix))

        self.shape_matrix = [list(row) for row in transpose_matrix[::-1]]

    #joga a peca para baixo (apertando o espaco)
    def send_shape_to_end(self):
        for i in range(20):
            #move a peca do jogo 1 bloco para baixo
            self.shape_pos[1] += 1
            #checa se a forma colidiu com alguma coisa
            shape_pos_x = self.shape_pos[0]
            shape_pos_y = self.shape_pos[1]
            for y in range(len(self.shape_matrix)):
                for x in range(len(self.shape_matrix[0])):
                    if self.shape_matrix[y][x] == 1:
                        try:
                            if self.map[y + shape_pos_y][x + shape_pos_x] != '':
                                self.shape_pos[1] -= 1
                                self.lock_shape()
                                return
                        except:
                            self.shape_pos[1] -= 1
                            self.lock_shape()
                            return

    #movimentacao do jogo
    def move(self, key):
        if key == 'a' or key == 'left':
            self.shape_pos[0] -= 1
            if self.is_shape_in_the_game() == False or self.did_shape_collide_sideways():
                self.shape_pos[0] += 1
        elif key == 's' or key == 'down':
            self.shape_pos[1] += 1
        elif key == 'd' or key == 'right':
            self.shape_pos[0] += 1
            if self.is_shape_in_the_game() == False or self.did_shape_collide_sideways():
                self.shape_pos[0] -= 1
        elif key == 'q': 
            self.rotate_shape_to_the_left()
            if self.is_shape_in_the_game() == False:
                self.rotate_shape_to_the_right()
        elif key == 'e':
            self.rotate_shape_to_the_right()
            if self.is_shape_in_the_game() == False:
                self.rotate_shape_to_the_left()
        elif key == 'space':
            self.send_shape_to_end()

    def get_color (self, color_code):
        if color_code == 'p':
            return self.purple
        elif color_code == 'b':
            return self.blue
        elif color_code == 'l':
            return self.light_blue
        elif color_code == 'r':
            return self.red
        elif color_code == 'o':
            return self.orange
        elif color_code == 'y':
            return self.yellow
        elif color_code == 'g':
            return self.green
        elif color_code == 'x':
            return self.gray
        else:
            return None
    def get_color_code(self, color):
        if color == self.purple:
            return 'p'
        elif color == self.blue:
            return 'b'
        elif color == self.light_blue:
            return 'l'
        elif color == self.red:
            return 'r'
        elif color == self.orange:
            return 'o'
        elif color == self.yellow:
            return 'y'
        elif color == self.green:
            return 'g'
        else:
            return None
    
    def draw_shapes_in_game(self):
        #desenha as formas ja colocadas no jogo
        for y in range(20):
            for x in range(10):
                if self.map[y][x] != '':
                    color = self.get_color(self.map[y][x])
                    border_color = tuple(min(rgb + 50, 255) for rgb in color)
                    pg.draw.rect(self.window, color, (self.board_square*x, self.board_square*y, self.board_square, self.board_square))
                    pg.draw.rect(self.window, border_color, (self.board_square * x, self.board_square*y, self.board_square, self.board_square), 1)

        #forma que esta em jogo 
        shape_pos_x = self.shape_pos[0]
        shape_pos_y = self.shape_pos[1]
        color = self.shape[self.selected_form]['color']
        border_color = tuple(min(rgb + 50, 255) for rgb in color)
        for y in range(len(self.shape_matrix)):
            for x in range(len(self.shape_matrix[0])):
                if self.shape_matrix[y][x] == 1:
                    pg.draw.rect(self.window, color, (self.board_square*(x+shape_pos_x), self.board_square*(y+shape_pos_y), self.board_square, self.board_square))
                    pg.draw.rect(self.window, border_color, (self.board_square*(x+shape_pos_x), self.board_square * (y + shape_pos_y), self.board_square, self.board_square), 1)

    #velocidade aumentada em proporcao a quantidade de pontos
    def game_speed(self):
        self.speed = min(1 + (self.score // 100), 50)

    #pontuacao ao posicionar uma peca no jogo
    def add_point(self, rows):
        for y in range(len(self.shape_matrix)):
            for x in range(len(self.shape_matrix[0])):
                if self.shape_matrix[y][x] == 1:
                    self.score += 1
        #pontos via linhas
        self.score += rows * 10

        self.game_speed()
        self.time = 0

    def lock_shape(self):
        shape_pos_x = self.shape_pos[0]
        shape_pos_y = self.shape_pos[1]
        for y in range(len(self.shape_matrix)):
            for x in range(len(self.shape_matrix[0])):
                if self.shape_matrix[y][x] == 1: #atualiza a posicao da forma em map
                    self.map[shape_pos_y + y][shape_pos_x + x] = self.get_color_code(self.shape[self.selected_form]['color'])
        self.get_next_shape() #pra pegar a proxima peca apos colocar a peca em jogo 

        completed_row_count = 0
        for y in range(20):
            row_count = 0
            for x in range(10):
                    if self.map[y][x] != '':
                        row_count += 1
            if row_count == 10:
                completed_row_count += 1

        self.add_point(completed_row_count)
        if completed_row_count >= 1:
            self.remove_completed_rows()

    def game_step(self):
        #velocidade do jogo
        self.time += 1
        if self.time == 61 - self.speed:
            self.shape_pos[1] += 1
            self.time = 0
        #checagem se a formula colidiu com alguma coisa
        shape_pos_x = self.shape_pos[0]
        shape_pos_y = self.shape_pos[1]
        for y in range(len(self.shape_matrix)):
            for x in range(len(self.shape_matrix[0])):
                if self.shape_matrix[y][x] == 1:
                    try:
                        if self.map[y + shape_pos_y][x + shape_pos_x] != '':
                            self.shape_pos[1] -= 1 #volta um quadrado
                            self.lock_shape()
                            return
                    except:
                        self.shape_pos[1] -= 1
                        self.lock_shape()
                        return

    def remove_completed_rows(self):
        #muda a cor das linhas completadas para cinza
        completed_rows_list = []
        for y in range(20):
            columns = 0
            for x in range(10):
                if self.map[y][x] != '':
                    columns += 1
            if columns == 10:
                completed_rows_list.append(y)
                for x in range(10):
                    self.map[y][x] = 'x'

        #limpa a tela e espera 1 seg
        self.clear_window()
        self.board()
        pg.display.update() #update da tela do jogo
        time.sleep(1) #espera 1 seg no loop

        #deleta a linha completada
        for row in completed_rows_list:
            for x in range(10):
                self.map[row][x] = ''
        
        #faz uma varredura e move as pecas para baixo.
        for rows in range(len(completed_rows_list)):
            for y in range(20):
                bottom_to_top_y = 19 - y
                columns = 0
                for x in range(10):
                    if self.map[bottom_to_top_y][x] == '':
                        columns += 1
                if columns == 10:
                    shift_y = 1
                    while bottom_to_top_y - shift_y >= 0:
                        for x in range(10):
                            self.map[bottom_to_top_y - shift_y + 1][x] = self.map[bottom_to_top_y - shift_y][x]
                        shift_y += 1

    #verifica se o jogo terminou
    def is_game_end(self):
        shape_pos_x = self.shape_pos[0]
        shape_pos_y = self.shape_pos[1]
        if self.show_restart_button == False: # == false, o jogo ainda nao terminou. faz uma varredura pra conitnuar verificando se o jogo acabou
            for y in range(len(self.shape_matrix)):
                for x in range(len(self.shape_matrix[0])):
                    if self.shape_matrix[y][x] == 1 and self.map[shape_pos_y + y][shape_pos_x + x] != '':
                        self.show_restart_button = True #botao restart aparece
                        self.shape_matrix = [[]]
                        return

    def restart_button(self, mouse):
        if self.show_restart_button: #verifica se esta ativo
            #caracteristicar do botao
            button_color = (0,200,0)
            button_width = self.window.get_width()/2.5
            button_height = button_width/2.5
            button_x = (self.window.get_width()/2) - (button_width/2)
            button_y = (self.window.get_height()/2) - (button_height/2)
            button_border = int(self.board_square/5)
            #hover quando o botao passar por cima
            if mouse[0][0] >= button_x and mouse[0][0] <= button_x + button_width and mouse [0][1] >= button_y and mouse[0][1] <= button_y + button_height:
                button_hover_color = tuple(min(rgb + 50, 255) for rgb in button_color)
                pg.draw.rect(self.window, button_hover_color, (button_x, button_y, button_width, button_height))
                if mouse[2][0]: #verifica se clicou no botao, mudando restart game para true
                    self.restart_game(True)
            else: #restart texto
                pg.draw.rect(self.window, button_color, (button_x, button_y, button_width, button_height))
            pg.draw.rect(self.window, self.white, (button_x, button_y, button_width, button_height), button_border)
            text = self.font.render('Reiniciar', 1, self.black)
            blit_x = (self.window.get_width()/2) - (text.get_width()/2)
            blit_y = (self.window.get_height()/2) - (text.get_height()/2)
            self.window.blit(text, (blit_x, blit_y))

    def restart_game(self, restart=False):
        if self.starting_first_game or restart: #verifica se o jogo esta iniciando, reinicia todas as variaveis do jogo
            self.init_random_shapes()
            self.score = 0
            self.speed = 1
            #loop pelo mapa do jogo, adiciona a string vazia
            for y in range(20): 
                for x in range(10):
                    self.map[y][x] = ''
            self.show_restart_button = False
            self.starting_first_game = False
            self.get_next_shape()