import sys
import os
# Import non-standard modules.
import pygame
import pygame_widgets
from pygame.locals import *
import numpy as np
import pygame_widgets as pw
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FUCHSIA = (255, 0, 255)
GRAY = (128, 128, 128)
LIME = (0, 128, 0)
MAROON = (128, 0, 0)
NAVYBLUE = (0, 0, 128)
OLIVE = (100, 150, 0)
PURPLE = (128, 0, 128)
REDDIE = (200, 50, 50)
RED = (240, 20, 20)
SILVER = (192, 192, 192)
TEAL = (0, 128, 128)
YELLOW = (200, 200, 0)
ORANGE = (255, 128, 0)
ORANGE_D = (128,80,0)
CYAN = (0, 255, 255)

class Sound(pygame.mixer.Sound):
    def playSound(self, slider):
        volume = slider.getValue() / 100
        self.stop()
        self.set_volume(volume)
        self.play()

class GridManager:
    def __init__(self, paths):
        self.paths = paths

        self.min_x = 250
        self.min_y = 200

        self.slider_width = 250
        self.slider_height = 50
        self.slider_margins = [70, 10]
        self.positions, self.slider_positions = self._build_positions()

    def _build_positions(self):
        pos = {}
        pos_slider = {}

        count = len(self.paths)
        w, h = pygame.display.get_surface().get_size()

        but_x = np.floor(w / (self.min_x))
        print(but_x)
        pos_y = 10
        x_fact = 0
        slider_y_offset = int(self.slider_margins[1] / 2)
        for x in range(0, count):
            if (x - x_fact) >= but_x:
                x_fact += but_x
                pos_y += self.min_y + self.slider_height

            pos_slider[self.paths[x]] = [((x - x_fact) * (self.min_x)) + (self.min_x - self.slider_width) + (self.slider_margins[0] / 2), pos_y + self.min_y + slider_y_offset, self.slider_width - self.slider_margins[0], self.slider_height - self.slider_margins[1]]
            #pos_slider[self.paths[x]] = [((x - x_fact) * (self.min_x - self.slider_width)) + (self.min_x - self.slider_width), pos_y]
            pos[self.paths[x]] = [(x - x_fact) * (self.min_x), pos_y, self.min_x, self.min_y]

        return [pos, pos_slider]


def runPyGame():
    global screen
    # Initialise PyGame.
    pygame.init()
    #pygame.FULLSCREEN = True
    # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
    fps = 144
    
    fpsClock = pygame.time.Clock()

    # Set up the window.
    WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    close_button = Button(screen, WIDTH-50, HEIGHT-50, 50, 50, text="X", onRelease=pygame.quit)
    # Main game loop.
    dt = 1 / fps  # dt is the time since last frame.

    sounds = {}
    buttons = {}

    sliders = {}

    global key_bind
    key_bind = {}
    paths = os.listdir("sound")

    manager = GridManager(paths)
    #print(manager.slider_positions)
    for path in paths:
        sounds[path] = Sound(os.path.join("sound", path))

        sliders[path] = Slider(screen, *manager.slider_positions[path],
                               handleRadius=20,
                               max=130,
                               initial=65
                               )
        buttons[path] = Button(screen,
                               *manager.positions[path],
                               text=path,
                               onClick=sounds[path].playSound,
                               onClickParams=[sliders[path], pygame.event.get()])
    stop_params = [250, 100]
    buttons["stop"] = Button(screen, 0, HEIGHT-stop_params[1], *stop_params, text="Stop all sounds",
                             onClick=pygame.mixer.stop)

    while True:  # Loop forever!

        dt = fpsClock.tick(fps)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            #print(event)
            if event.type == pygame.KEYDOWN and event.key != pygame.K_LCTRL:
                if event.key not in key_bind:
                    pass
                else:
                    key_bind[event.key][0](key_bind[event.key][1])

        screen.fill((40,40,40))

        pygame_widgets.update(pygame.event.get())
        pygame.display.flip()


if __name__ == "__main__":
    runPyGame()