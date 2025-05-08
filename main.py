import pygame as pg

def play_tetris ():
    print("Tetris")

def play_flappy() :
    print("Flappy Birds")

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

    pg.quit()

if __name__ == "__main__":
    main()