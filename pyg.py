import pygame

pygame.init()


class handler:
    def __init__(self, width=0, height=0):
        self.width = width
        self.height = height
        self.running = True

        self.screen = pygame.display.set_mode((self.width, self.height))

    def start(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            pygame.display.flip()
        pygame.quit()

    # OBJECT RENDERING

    def render_text(self, message, position, color, size, alignment="center"):
        font = pygame.font.Font("freesansbold.ttf", size)
        text = font.render(message, True, color)
        textRect = text.get_rect()

        textRect.center = (position[0], self.height - position[1])
        if alignment =="left":
            textRect.left = position[0]
        elif alignment =="right":
            textRect.right = position[0]
            
        self.screen.blit(text, textRect)

    def render_point(self, pos, color, radius):
        pygame.draw.circle(self.screen, color,
                           (pos[0], self.height - pos[1]), radius)

    def render_line(self, start_pos, end_pos, color):
        pygame.draw.line(self.screen, color, (
            start_pos[0], self.height - start_pos[1]), (end_pos[0], self.height - end_pos[1]))
