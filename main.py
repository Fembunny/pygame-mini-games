import pygame as pg
from games.snake_game.cobrinha import Snake_Game
from games.snake_game.window import Window
from games.tetris.tetris import Tetris
from games.flappy_birds.flappy import FlappyBirds
from menu.button import Button

def play_cobrinha():
    w = Window(screen_resolution=(1272, 720))
    snake_game = Snake_Game()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if w.home_menu == False:
                    snake_game.key_pressed_log = pg.key.name(event.key)
                    if snake_game.key_pressed == False:
                        snake_game.snake_change_direction(pg.key.name(event.key))
                        snake_game.key_pressed = True
                if pg.key.name(event.key) == 'escape':
                    w.pause_menu = w.pause_menu == False

        mouse_position  = pg.mouse.get_pos()
        mouse_input = pg.mouse.get_pressed()
        mouse_click = w.mouse_has_clicked(mouse_input)
        w.mouse = (mouse_position, mouse_input, mouse_click)

        w.clear_window('black')

        if w.home_menu == True:
            button_action = w.home_screen([('Start', 'purple', 'black')])

            if button_action == 'Start':
                w.home_menu = False
                snake_game.snake_position = [(40, 20), (41, 20), (41, 21), (41, 22), (41, 23), (42, 23)]
                snake_game.snake_direction = (-1, 0)
                snake_game.sort_apple_position()
        else:
            if w.pause_menu == False and snake_game.countdown == -1 and snake_game.end_game == False:
                snake_game.update_snake_position(snake_game.snake_position)

            snake_game.clear_map(snake_game.map)
            snake_game.add_snake_position(snake_game.map_size, snake_game.snake_position)
            snake_game.add_apple_position(snake_game.map_size, snake_game.apple_position)
            snake_game.draw_map_elements(w.window)
            snake_game.draw_score(w.window)
            snake_game.snake_get_apple()
            snake_game.end_of_game()

            if w.pause_menu == False and snake_game.countdown >= 0 and snake_game.end_game == False:
                snake_game.game_start_countdown(w.window)

            if snake_game.end_game == True:
                snake_game.draw_end_game(w.window)

            if w.pause_menu == True:
                button_action = w.pause_screen([('Restart', 'pink'), ('Quit Game', 'pale-yellow')], button_layout=(3, 3))
                snake_game.countdown = 3
                if button_action == 'Restart':
                    w.pause_menu = False
                    snake_game.reset_game()
                elif button_action == 'Quit Game':
                    return main()

        w.last_click_status = mouse_input

        pg.display.update()
        w.fps(30)
        snake_game.key_pressed = False
        snake_game.snake_change_direction(snake_game.key_pressed_log)

def play_flappy() :
    pg.display.set_caption("Flappy Birds")
    flappy = FlappyBirds((1280, 720))

    while True :
        for event in pg.event.get() :
            if event.type == pg.QUIT :
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN :
                flappy.move(pg.key.name(event.key))

                if pg.key.name(event.key) == 'escape':
                    return main()

        mouse_position = pg.mouse.get_pos()
        mouse_input = pg.mouse.get_pressed()
        mouse_click = flappy.mouse_has_clicked(mouse_input)
        mouse = (mouse_position, mouse_input, mouse_click)

        # Game
        flappy.clock.tick(60)
        flappy.clear_window()
        flappy.board()
        flappy.movement()
        flappy.scoreboard()
        flappy.collision()
        flappy.restart_button(mouse)

        flappy.last_click_status = mouse_input

        pg.display.update()

def play_tetris():
    tetris = Tetris(38) 
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                tetris.move(pg.key.name(event.key))
                if pg.key.name(event.key) == 'escape':
                    return main()

        mouse_position = pg.mouse.get_pos() 
        mouse_input = pg.mouse.get_pressed() 
        mouse_click = tetris.mouse_has_clicked(mouse_input) 
        mouse = (mouse_position, mouse_input, mouse_click) 


        tetris.clock.tick(60) 
        tetris.clear_window() 

        tetris.restart_game()

        if tetris.new_shape: 
        #Pega uma nova forma quando tetris.new_shape == True
            tetris.get_next_shape()

        tetris.board()
        tetris.game_step()

        tetris.is_game_end()
        
        tetris.restart_button(mouse)

        tetris.last_click_status = mouse_input

        pg.display.update()

def get_font(size):
    return pg.font.Font("assets/font.ttf", size)

def main():
    # Inicialização do Pygame
    pg.init()

    screen = pg.display.set_mode((1280, 720))
    imagem = pg.image.load('assets/games.png')
    pg.display.set_icon(imagem)
    pg.display.set_caption("Mini Games")
    background = pg.image.load("assets/tree.jpg")

    running = True
    while running:
        screen.blit(background, (0, 0))

        mouse_position = pg.mouse.get_pos()
        menu_text = get_font(40).render("START GAME", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(640, 280))

        # Chamando a classe e criando os botões
        cobrinha_button = Button(pos=(640, 350), text_input="Cobrinha", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        flappy_button = Button(pos=(640, 410), text_input="Flappy-Birds", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        tetris_button = Button(pos=(640, 470), text_input="Tetris", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(pos=(640, 530), text_input="Quit", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        screen.blit(menu_text, menu_rect)

        # For para desenhar botões
        for button in [cobrinha_button, flappy_button, tetris_button, quit_button]:
            button.changeColor(mouse_position)
            button.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT :
                running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                if cobrinha_button.checkForInput(mouse_position) :
                    play_cobrinha()
                if flappy_button.checkForInput(mouse_position) :
                    play_flappy()
                if tetris_button.checkForInput(mouse_position):
                    play_tetris()
                if quit_button.checkForInput(mouse_position) :
                    running = False

        pg.display.update()

    pg.quit()

if __name__ == "__main__":
    main()