import pygame
import math
import os

import palletts as p
import accessors as a

class text:
    def __init__(self, color=-1, font=a.monoid, fontSize=10, text=-1):
        self.color = color
        
        self.font = self.return_font(font)

        self.fontSize = fontSize
        self.text = text

        self.parent = None
        self.rendering = True

        self.default = False

    def return_font(self, font):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        p = dir_path + font
        if os.path.exists( p ):
            return p
        elif os.path.exists( font ):
            return font
        return dir_path + a.monoid


    def __reinit__(self, parent):
        self.parent = parent
        if self.color == -1:
            self.default = True
            self.color = parent.pallett.text_RGB

    def __color__(self, color):
        if color == - 1 or not self.default:
            return self.color
        else:
            return color

    def __text__(self, text):
        if self.text == -1:
            return text
        else:
            return self.text

    def render(self, message, pos, color=-1, alignmentX="center", alignmentY="center"):
        if self.rendering:
            font = pygame.font.Font(self.font, self.fontSize)
            text = font.render(self.__text__(message),
                               True, self.__color__(color))
            textRect = text.get_rect()

            y = self.parent.graph.handler.height - pos[1]
            textRect.center = (pos[0], y)
            if alignmentX == "left":
                textRect.left = pos[0]
            elif alignmentX == "right":
                textRect.right = pos[0]
            if alignmentY == "top":
                textRect.top = y
            elif alignmentY == "bottom":
                textRect.bottom = y

            self.parent.graph.handler.surface.blit(text, textRect)

    # USER FUNCTIONS
    def update_visibility(self, vis):
        self.rendering = vis
        return self.parent


class line:
    def __init__(self, color=-1, stroke=1):
        self.color = color
        self.stroke = stroke

        self.parent = None
        self.rendering = True

        self.default = False

    def __reinit__(self, parent):
        self.parent = parent
        if self.color == -1:
            self.default = True
            self.color = parent.pallett.text_RGB

    def __color__(self, color):
        if color == - 1 or not self.default:
            return self.color
        else:
            return color

    def render(self, p, p2, color=-1):
        if self.rendering:
            pos = (p[0], self.parent.graph.handler.height - p[1])
            pos2 = (p2[0], self.parent.graph.handler.height - p2[1])

            pygame.draw.line(self.parent.graph.handler.screen,
                             self.__color__(color), pos, pos2, self.stroke)

    # USER FUNCTIONS
    def update_visibility(self, vis):
        self.rendering = vis
        return self.parent


class point:
    def __init__(self, color=-1, radius=2, stroke=0, stroke_color=-1, shape=-1):
        self.color = color

        self.radius = radius
        self.stroke = stroke
        self.stroke_color = stroke_color
        self.shape = shape

        self.handler = None
        self.parent = None

        self.rendering = True
        self.default = False

    def __reinit__(self, parent):
        self.parent = parent
        self.handler = parent.graph.handler
        if self.stroke_color == -1:
            self.stroke_color = parent.pallett.text_RGB
        if self.color == -1:
            self.default = True
            self.color = parent.pallett.prim_RGB

    def __color__(self, color):
        if color == - 1 or not self.default:
            return self.color
        else:
            return color

    def __render_polygon__(self, center, color):
        coords = []
        outlines = []
        for side in range(0, self.shape):
            theta = 2 * math.pi * (side / self.shape)
            point = ((math.cos(theta) * self.radius),
                     (math.sin(theta) * self.radius))
            outline = (math.cos(theta) * (self.radius + self.stroke),
                       math.sin(theta) * (self.radius + self.stroke))
            coords.append((point[0]+center[0], point[1]+center[1]))
            outlines.append((outline[0]+center[0], outline[1]+center[1]))

        pygame.draw.polygon(self.handler.surface, self.stroke_color, outlines)
        pygame.draw.polygon(self.handler.surface, color, coords)

    def render(self, p, color=-1):
        if self.rendering:
            pos = (p[0], self.handler.height - p[1])
            if self.shape == -1:
                pygame.draw.circle(
                    self.handler.surface, self.stroke_color, pos, self.radius + self.stroke)
                pygame.draw.circle(self.handler.surface,
                                   self.__color__(color), pos, self.radius)
            else:
                self.__render_polygon__(pos, self.__color__(color))

    # USER FUNCTIONS

    def update_visibility(self, vis):
        self.rendering = vis
        return self.parent


class domain:
    def __init__(self, pos, size, padding=(75, 30), parent=None, pallett=p.green_tea):
        self.pos = pos
        self.size = size
        self.padding = padding

        self.pallett = pallett
        self.parent = parent

        self.rendering = True

    def __reinit__(self, parent):
        self.parent = parent
        self.pallett = parent.pallett

    def render(self):
        if self.rendering:

            rect = pygame.Rect(
                self.pos[0] - self.padding[0],
                self.pos[1] + self.size[1] + self.padding[1],
                self.size[0] + (self.padding[0] * 2),
                self.size[1] + (self.padding[1] * 2)
            )

            self.parent.graph.handler.render_rect(rect, self.pallett.back_RGB)

    # User Functions

    def update_padding(self, padding):
        self.padding = padding
        return self.parent

    def update_visibility(self, vis):
        self.rendering = vis
        return self.parent


default_domain = domain(
    pos=(100, 100),
    size=(500, 500),
)
