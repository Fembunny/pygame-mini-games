import pygame as pg
from games.flappy_birds.flappy import FlappyBirds
from menu.button import Button

def play_tetris ():
    print("Tetris")

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
        tetris_button = Button(pos=(640, 350), text_input="Tetris", font=get_font(30), base_color="black", hovering_color="White")
        flappy_button = Button(pos=(640, 410), text_input="Flappy-Birds", font=get_font(30), base_color="black", hovering_color="White")
        quit_button = Button(pos=(640, 470), text_input="Quit", font=get_font(30), base_color="black", hovering_color="White")

        screen.blit(menu_text, menu_rect)

        # For para desenhar botões
        for button in [tetris_button, flappy_button, quit_button]:
            button.changeColor(mouse_position)
            button.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT :
                running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                if tetris_button.checkForInput(mouse_position) :
                    play_flappy()
                if flappy_button.checkForInput(mouse_position) :
                    play_flappy()
                if quit_button.checkForInput(mouse_position) :
                    running = False

        pg.display.update()

    pg.quit()

if __name__ == "__main__":
    main()