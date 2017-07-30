import pygame
from GuiConstants import *

class GuiCross(pygame.sprite.Sprite):
    """Cross object"""

    def __init__(self, center):
        self.center = center

        (centerx, centery) = center
        width = LINE_WIDTH * 2

        self.crossrect = pygame.Rect((centerx - LINE_WIDTH, centery - LINE_WIDTH), (width, width))
        self.scontrol = pygame.Rect((centerx - LINE_WIDTH, centery - LINE_WIDTH - CONTROL_DISTANCE - CONTROL_WIDTH), (LINE_WIDTH, CONTROL_WIDTH))
        self.ncontrol = pygame.Rect((centerx, centery + LINE_WIDTH + CONTROL_DISTANCE), (LINE_WIDTH, CONTROL_WIDTH))
        self.wcontrol = pygame.Rect((centerx + LINE_WIDTH + CONTROL_DISTANCE, centery - LINE_WIDTH), (CONTROL_WIDTH, LINE_WIDTH))
        self.econtrol = pygame.Rect((centerx - LINE_WIDTH - CONTROL_DISTANCE - CONTROL_WIDTH, centery), (CONTROL_WIDTH, LINE_WIDTH))


    def draw(self):
        """Renders the crossroad"""

        #Main crossroad
        screen = pygame.display.get_surface()
        pygame.draw.rect(screen, YELLOW, self.crossrect, 0)

        #Draw controls
        pygame.draw.rect(screen, WHITE, self.ncontrol, 0)
        pygame.draw.rect(screen, WHITE, self.scontrol, 0)
        pygame.draw.rect(screen, WHITE, self.wcontrol, 0)
        pygame.draw.rect(screen, WHITE, self.econtrol, 0)

