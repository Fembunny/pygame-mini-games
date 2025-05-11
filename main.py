import pygame as pg
from games.flappy_birds.flappy import FlappyBirds

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

        # Mouse info
        mouse_position = pg.mouse.get_pos()
        mouse_input = pg.mouse.get_pressed()
        mouse_click = flappy.mouse_has_clicked(mouse_input)
        mouse = (mouse_position, mouse_input, mouse_click)

        # Game
        flappy.clock.tick(60)

        flappy.last_click_status = mouse_input

        pg.display.update()

def main():
    # Inicialização do Pygame
    pg.init()
    window_size = 42
    screen = pg.display.set_mode((window_size * 14, window_size * 20))

    imagem = pg.image.load('assets/games.png')
    pg.display.set_icon(imagem)
    pg.display.set_caption("Mini Games")

    running = True
    while running:
        for event in pg.event.get() :
            if event.type == pg.QUIT :
                running = False
            if event.type == pg.KEYDOWN:
                # IF DE TESTE PARA VERIFICAR A TELA DO FLAPPY
                if pg.key.name(event.key) == 'escape':
                    return play_flappy()

    pg.quit()

if __name__ == "__main__":
    main()