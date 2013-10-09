import os
import sys
import math
import pygame as pg

from particle.particle_alt import Emitter


CAPTION = "Plasma Example"


class Control(object):
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        pg.mouse.set_pos(self.screen_rect.center)
        self.particle_surface = pg.Surface(self.screen_rect.size).convert()
        self.particle_surface.set_colorkey((0,0,0))
        self.clock = pg.time.Clock()
        self.done = False
        self.fps = 60.0
        self.generator = self.make_emitter()
        self.tick = pg.time.get_ticks()

    def make_emitter(self):
        kwarg_dict = {"texture"     : FUZZ,
                      "speed"       : (0.1,0.5),
                      "size"        : (10,30),
                      "start_color" : (50,50,255)}
        return Emitter(self.screen_rect.center,150,**kwarg_dict)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

    def update(self):
        self.generator.pos = pg.mouse.get_pos()
        self.screen.fill((170,238,187))
        self.particle_surface.fill(0)
        self.generator.update(self.particle_surface,self.tick)
        self.screen.blit(self.particle_surface,(0,0))

    def main_loop(self):
        while not self.done:
            self.tick = pg.time.get_ticks()
            self.event_loop()
            self.update()
            pg.display.update()
            self.clock.tick(self.fps)
            caption = "{} - FPS: {:.2f}".format(CAPTION,self.clock.get_fps())
            pg.display.set_caption(caption)


if __name__ == "__main__":
    os.environ["SDL_VIDEO_CENTERED"] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode((500,500))
    PATH = os.path.join("resources","fuzzball5.png")
    FUZZ = pg.image.load(PATH).convert_alpha()
    run_it = Control()
    run_it.main_loop()
    pg.quit()
    sys.exit()
