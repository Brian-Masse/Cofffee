import pygame
import sys
import os

sys.path.append( sys.path[-1] + "/cofffee" )

class handler:
    def __init__(self, width=0, height=0, title=""):
        pygame.init()

        self.width = width
        self.height = height

        self.title = title

        self.running = True
        self.screen = pygame.display.set_mode((self.width, self.height))

        dir_path = os.path.dirname(os.path.realpath(__file__))
        p = dir_path + "/Extra/icon.png"
        if os.path.exists(p):
            Icon = pygame.image.load(p)
            pygame.display.set_icon(Icon)
    
        pygame.display.set_caption(self.title)

        self.surface = self.__return_surface__()

    def start(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            pygame.display.flip()
        pygame.quit()

    # OBJECT RENDERING

    def __return_surface__(self):
        return pygame.Surface((self.width, self.height), pygame.SRCALPHA)

    def render_que(self):
        self.screen.blit(self.surface, (0, 0))
        self.surface = self.__return_surface__()

    def render_rect(self, rect, color):
        new_rect = pygame.Rect(rect.left, self.height -
                               rect.top, rect.width, rect.height)
        pygame.draw.rect(self.screen, color, new_rect)

    def render_line(self, start_pos, end_pos, color, thickness=2):
        pygame.draw.line(self.screen, color, (
            start_pos[0], self.height - start_pos[1]), (end_pos[0], self.height - end_pos[1]), thickness)
