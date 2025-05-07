import pygame as pg

def play_tetris ():
    print("Tetris")

def play_flappy() :
    print("Flappy Bird")

def main():
    # Inicialização do Pygame
    pg.init()
    pg.display.set_caption("Mini Games")
    window_size = 42
    screen = pg.display.set_mode((window_size * 14, window_size * 20))

    running = True
    while running:
        for event in pg.event.get() :
            if event.type == pg.QUIT :
                running = False

    pg.quit()

if __name__ == "__main__":
    main()