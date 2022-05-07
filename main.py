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

class Sound(pygame.mixer.Sound):
    def setVars(self, slider, name):
        self.slider = slider
        self.path = name

    def playSound(self, events=None):
        global set_bind
        print("play")
        #print(events)
        """
        print(KEY_TO_BIND)
        if BIND_STATE:
            print("try to bind")
            print(pygame.event.event_name(KEY_TO_BIND))
            key_bind[KEY_TO_BIND] = self.playSound
            BIND_STATE = False
        """
        print(set_bind)
        if set_bind:
            key_bind[KEY_TO_BIND] = self.playSound
            set_bind = False

            #renew Buttons text
            buttons[self.path] = Button(screen,
                               *manager.positions[self.path],
                               text=self.path.replace(".mp3", "") + f" ({pygame.key.name(KEY_TO_BIND)})",
                               onClick=self.playSound,
                               onClickParams=[])
        volume = self.slider.getValue() / 100
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
    global screen, key_bind, BIND_STATE, KEY_TO_BIND, set_bind
    set_bind = False
    BIND_STATE = False
    KEY_TO_BIND = 0

    # button to enable binding
    BIND_BUTTON = pygame.K_SPACE

    # Initialise PyGame.
    pygame.init()
    #pygame.FULLSCREEN = True
    # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
    fps = 60
    
    fpsClock = pygame.time.Clock()

    # Set up the window.
    WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    close_button = Button(screen, WIDTH-50, HEIGHT-50, 50, 50, text="X", onRelease=pygame.quit)
    # Main game loop.
    dt = 1 / fps  # dt is the time since last frame.
    global sounds, buttons, sliders, manager
    sounds = {}
    buttons = {}

    sliders = {}

    #list of sounds binded to keys
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

        #assign slider to sound
        sounds[path].setVars(sliders[path], name=path)

        #bind button to sound
        buttons[path] = Button(screen,
                               *manager.positions[path],
                               text=path.replace(".mp3", ""),
                               onClick=sounds[path].playSound,
                               onClickParams=[])

    stop_params = [250, 100]
    buttons["stop"] = Button(screen, 0, HEIGHT-stop_params[1], *stop_params, text="Stop all sounds",
                             onClick=pygame.mixer.stop)

    disable_bind_mode = False
    fill_col = (40,40,40)
    while True:  # Loop forever!
        dt = fpsClock.tick(fps)
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
            #print(event)
            if event.type == pygame.KEYDOWN and event.key == BIND_BUTTON and not BIND_STATE:
                fill_col = (150,20,20)
                BIND_STATE = True
                #print(pygame.key.name(event.key))
                print("rdy to bind")

            #select key to bind
            elif event.type == pygame.KEYDOWN and event.key != BIND_BUTTON and BIND_STATE:
                KEY_TO_BIND = event.key
                disable_bind_mode = True
                set_bind = True
                print(pygame.key.name(event.key) + " SELECTED TO BIND")

            elif (event.type == pygame.KEYDOWN and event.key == BIND_BUTTON and BIND_STATE) or disable_bind_mode:
                disable_bind_mode = False
                print("unrdy to bind")
                BIND_STATE = False
                fill_col = (40,40,40)

            if event.type == pygame.KEYDOWN:
                if event.key in key_bind:
                    print("PLAYSOUND")
                    key_bind[event.key]()




        screen.fill(fill_col)

        pygame_widgets.update(pygame.event.get())
        pygame.display.flip()


if __name__ == "__main__":

    runPyGame()
