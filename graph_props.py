import pygame

import b_grapher.palletts as p

class domain:
    def __init__( self, pos, size, padding=(75, 30), parent=None, pallett=p.green_tea):
        self.pos = pos
        self.size = size
        self.padding = padding

        self.pallett = pallett
        self.parent = parent

    def __reinit__(self, parent):
        self.parent = parent
        self.pallett = parent.pallett

    def render(self):

        # print(self.padding[0], self.padding[1])
        rect = pygame.Rect(
            self.pos[0] - self.padding[0], 
            self.pos[1] + self.size[1] + self.padding[1], 
            self.size[0] + (self.padding[0] * 2),
            self.size[1] + (self.padding[1] * 2)
        )


        self.parent.graph.handler.render_rect( rect, self.pallett.back_RGB )
    
    # User Functions

    def update_padding(self, padding):
        self.padding = padding
        return self.parent

default_domain = domain(  
    pos=(100, 100 ), 
    size=(500, 500),
)