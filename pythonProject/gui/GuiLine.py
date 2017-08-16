"""Line object"""
import pygame
from GuiConstants import *
from GuiCar import *

class GuiLine(pygame.sprite.Sprite):
    """Line"""

    def __init__(self, direction, length, position):
        self.direction = direction
        self.length = length
        self.position = position
        self.height = 0
        self.width = 0
        self.cars = []

        if self.direction == 'N' or self.direction == 'S':
            self.width = LINE_WIDTH
            self.height = length
        elif self.direction == 'E' or self.direction == 'W':
            self.width = length
            self.height = LINE_WIDTH

        self.rect = pygame.Rect(position, (self.width, self.height))

    def draw(self):
        """Renders the line"""

        screen = pygame.display.get_surface()
        pygame.draw.rect(screen, BLACK, self.rect, 0)

        (posx, posy) = self.position

        if self.direction in ['N', 'S']:
            pygame.draw.line(screen, WHITE, self.position, (posx, self.length), 1)
            pygame.draw.line(screen, WHITE, (posx + LINE_WIDTH, posy), (posx + LINE_WIDTH, self.length), 1)
        else:
            pygame.draw.line(screen, WHITE, self.position, (self.length, posy), 1)
            pygame.draw.line(screen, WHITE, (posx, posy + LINE_WIDTH), (posx + self.length, posy + LINE_WIDTH), 1)

    def add_car(self, ident):
        """A car starts driving by the line"""

        move_params = (0, 0)
        position = self.position
        (posx, posy) = position

        if self.direction == 'N':
            move_params = (90, -1)
            position = (posx, posy + self.length - CAR_LENGTH)
        elif self.direction == 'S':
            move_params = (90, 1)
        elif self.direction == 'W':
            move_params = (0, -1)
            position = (posx + self.length - CAR_LENGTH, posy)
        elif self.direction == 'E':
            move_params = (0, 1)

        self.cars.append(GuiCar(ident, move_params, position, self.direction))

    def add_block_car(self, position):
        """Adds a block car"""

        if len(self.cars) > 0:
            move_params = (0, 0)
            current_idx = 0

            for current_car in self.cars:
                if current_car.is_block:
                    break
                elif current_car.status == 'CO':
                    self.cars.insert(current_idx, GuiCar(-1, move_params, position, self.direction, True))
                    break

                current_idx += 1

    def remove_block_car(self):
        """Removes the block car"""

        if len(self.cars) > 0:
            current_idx = 0
            delete_car = None

            for current_car in self.cars:
                if current_car.is_block:
                    delete_car = current_car
                    break

                current_idx += 1

            if delete_car != None:
                self.cars.remove(delete_car)

    def update(self, timespent):
        """Update cars ni the line"""

        for i in range(0, len(self.cars)):
            if i > 0:
                self.cars[i].update(self.cars[i - 1], timespent)
            else:
                self.cars[i].update(None, timespent)

        self.check_out_screen()

    def check_out_screen(self):
        """Checks what cars are outside screen and removes them

        for current in self.cars:
            (carx, cary) = current.rect.center
            remove = False

            if self.direction == 'N':
                if cary < 0:
                    remove = True
            if self.direction == 'S':
                if cary > self.length:
                    remove = True
            if self.direction =="""

        contained_cars = []

        for current in self.cars:
            if self.rect.colliderect(current.rect):
                contained_cars.append(current)
            else:
                event = pygame.event.Event(pygame.USEREVENT, code="CAR_EXIT", car = current)
                pygame.event.post(event)

        self.cars = contained_cars

    def render(self):
        """Renders the cars of the line"""

        screen = pygame.display.get_surface()

        for current in self.cars:
            screen.blit(screen, current.rect, current.rect)
            current.carsprite.draw(screen)
