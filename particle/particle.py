import os
import sys
import math
import random
import pygame as pg


class Particle(object):
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)
        self.rect = pg.Rect((0,0),self.size)
        self.image = pg.Surface(self.size).convert_alpha()
        self.make_image(self.image)
        self.rect.center = self.pos
        self.real_center = list(self.pos)
        self.vector = self.make_vector(self.speed,self.angle)
        self.dead = False

    def make_image(self,surface):
        surface.fill((0,0,0,0))
        rect = surface.get_rect()
        if self.texture:
            scale = pg.transform.smoothscale(self.texture,rect.size)
            surface.blit(scale,(0,0))
            surface.fill(self.start_color,special_flags=pg.BLEND_RGBA_MULT)
        else:
            pg.draw.ellipse(surface,self.start_color,rect)

    def make_vector(self,speed,angle):
        x = speed*math.cos(angle)
        y = -speed*math.sin(angle)
        return [x,y]

    def update(self,surface,tick):
        if not self.dead:
            self.real_center[0] += self.vector[0]
            self.real_center[1] += self.vector[1]
            self.rect.center = self.real_center
            self.draw(surface)
            if tick-self.birth_time > self.life_span*1000:
                self.dead = True

    def draw(self,surface):
        surface.blit(self.image,self.rect,special_flags=pg.BLEND_RGB_ADD)


class Emitter(object):
    def __init__(self,location,slots,**kwargs):
        self.pos = location
        self.emission_speed = 10
        self.last_emit_time = 0.0
        self.slots = [None for i in range(slots)]
        self.particle_kwargs = self.set_kwargs(kwargs)

    def update(self,surface,tick):
        for i,particle in enumerate(self.slots):
            if particle:
                if particle.dead:
                    if tick-self.last_emit_time > self.emission_speed:
                        particle.__init__(**self.new_particle(tick))
                        self.last_emit_time = tick
                else:
                    particle.update(surface,tick)
            else:
                if tick-self.last_emit_time > self.emission_speed:
                    self.slots[i] = Particle(**self.new_particle(tick))
                    self.last_emit_time = tick

    def new_particle(self,tick):
        part_dict = {}
        for k in ("angle","speed","life_span"):
            if isinstance(self.particle_kwargs[k],(float,int)):
                part_dict[k] = self.particle_kwargs[k]
            else:
                part_dict[k] = random.uniform(*self.particle_kwargs[k])

        if isinstance(self.particle_kwargs["size"],int):
            size = self.particle_kwargs["size"]
            part_dict["size"] = (size,size)
        else:
            size = random.randint(*self.particle_kwargs["size"])
            part_dict["size"] = (size,size)
        part_dict["texture"] = self.particle_kwargs["texture"]
        part_dict["start_color"] = self.particle_kwargs["start_color"]
        part_dict["end_color"] = self.particle_kwargs["end_color"]
        delta_x,delta_y = self.particle_kwargs["delta"]
        pos_x = self.pos[0]+random.randint(-delta_x,delta_x)
        pos_y = self.pos[1]+random.randint(-delta_y,delta_y)
        part_dict["pos"] = pos_x,pos_y
        part_dict["birth_time"] = tick
        return part_dict

    def set_kwargs(self,kwargs):
        kwarg_dict = {"texture" : None,
                      "angle" : (0,2*math.pi),
                      "speed" : (1,3),
                      "size"  : (15,20),
                      "life_span" : 2.0,
                      "start_color" : (255,50,15),
                      "end_color" : None,
                      "delta" : (25,0)
                      }
        for kwarg in kwargs:
            if kwarg in kwarg_dict:
                kwarg_dict[kwarg] = kwargs[kwarg]
        return kwarg_dict
