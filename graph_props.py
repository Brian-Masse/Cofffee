import pygame
import math 

import b_grapher.palletts as p


class point:
    def __init__(self, color=-1, radius=2, stroke=0, stroke_color=-1, shape=-1) :
        self.color = color

        self.radius = radius
        self.stroke = stroke
        self.stroke_color = stroke_color
        self.handler = None
        self.shape = shape

    def __reinit__(self, parent):
        self.handler = parent.graph.handler
        if self.stroke_color == -1: self.stroke_color = parent.pallett.text_RGB
        if self.color == -1: self.color = parent.pallett.prim_RGB

    def __color__( self, color ):
        if color == - 1: return self.color
        else: return color

    def __render_polygon__(self, center, color):
        coords = []
        outlines = []
        for side in range(0, self.shape):
            theta = 2 * math.pi * ( side / self.shape )
            point = ((math.cos(theta) * self.radius), (math.sin(theta) * self.radius))
            outline = ( math.cos(theta) * (self.radius + self.stroke), math.sin(theta) * (self.radius + self.stroke))
            coords.append ( ( point[0]+center[0], point[1]+center[1] ) )
            outlines.append ( ( outline[0]+center[0], outline[1]+center[1] ) )

        pygame.draw.polygon(self.handler.surface, self.stroke_color, outlines)
        pygame.draw.polygon(self.handler.surface, color, coords)

    def render(self, p, color=-1):
        pos = (p[0], self.handler.height - p[1] )
        if self.shape == -1:
            pygame.draw.circle(self.handler.surface, self.stroke_color, pos, self.radius + self.stroke )
            pygame.draw.circle(self.handler.surface, self.__color__(color), pos, self.radius )
        else:
            self.__render_polygon__( pos, self.__color__(color) )
        

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
