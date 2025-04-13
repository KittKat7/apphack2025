if __name__ == "__main__":
    import main
    exit()

from abc import ABC, abstractmethod
from typing import Union
import pygame as pg

from entity import Entity
from gameobject import GameObject
from world import World

widgetFont: pg.font.Font

class Widget():
    """
    """
    @staticmethod
    def setFont(font) -> None:
        global widgetFont
        widgetFont = font

    @abstractmethod
    def __init__(self):
        self.x: int
        self.y: int
        self.initWidth: int
        self.width: int
        self.initHeight: int
        self.height: int
        pass
    @abstractmethod
    def render(self, screen, scale):
        pass
    @abstractmethod
    def event(self, event):
        pass

    def isMouseHover(self) -> bool:
        mouse = pg.mouse.get_pos()
        return self.x <= mouse[0] and mouse[0] <= self.x + self.width and self.y <= mouse[1] and mouse[1] <= self.y + self.height

class Text(Widget):
    def __init__(self, x: int, y: int, width: int, height: int, onClickFunction, text: str):
        self.x = x
        self.y = y
        self.initWidth = width
        self.width = width
        self.initHeight = height
        self.height = height
        self.onClickFunction = onClickFunction
        self.text = text

    def render(self, screen, scale):
        textSurface = widgetFont.render(self.text, False, (0, 0, 0))
        self.width, self.height = textSurface.get_size()
        self.width = self.width * scale
        self.height = self.height * scale
        textSurface = pg.transform.scale(textSurface, (self.width, self.height))
        screen.blit(textSurface, (self.x, self.y))

class Button(Widget):
    def __init__(self, x, y, width, height, onClickFunction, buttonText='Button', onePress=False):
        self.x = x
        self.y = y
        self.initWidth = width
        self.width = width
        self.initHeight = height
        self.height = height
        self.onClickFunction = onClickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.image = pg.image.load("./assets/button.png").convert_alpha()
        self.imageHover = pg.image.load("./assets/button_hover.png").convert_alpha()
        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.text = Text(x, y, width, height, None, buttonText)

    def render(self, screen, scale):
        self.width = self.initWidth * scale
        self.height = self.initHeight * scale
        if self.isMouseHover():
            # pg.draw.rect(screen, self.fillColors["hover"], [self.x,self.y,self.width,self.height], border_radius=25)
            screen.blit(pg.transform.scale(self.imageHover, (self.width, self.height)), (self.x, self.y))
        else:
            # pg.draw.rect(screen, self.fillColors["normal"], [self.x,self.y,self.width,self.height], border_radius=25)
            screen.blit(pg.transform.scale(self.image, (self.width, self.height)), (self.x, self.y))

        self.text.x = int(self.x + self.width / 2 - self.text.width / 2)
        self.text.y = int(self.y + self.height / 2 - self.text.height / 2)
        self.text.render(screen, scale)


        # pg.draw.line(screen, '#333333', (self.x + self.width/3, self.y), (self.x + self.width/3*2, self.y + self.height), width=5)
        # pg.draw.line(screen, '#333333', (self.x + self.width/3*2, self.y), (self.x + self.width/3, self.y + self.height), width=5)

    def event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse = pg.mouse.get_pos()
            if self.isMouseHover():
                self.onClickFunction()

class EntityWidget(Widget):

    entityImage = None
    lifeImage = None
    perceptionImage = None
    speedImage = None
    staminaImage = None
    strongImage = None
    toughImage = None

    def __init__(self, x: int, y: int, width: int, height: int, entity: Entity):
        self.x = x
        self.y = y
        self.initWidth = width
        self.width = width
        self.initHeight = height
        self.height = height
        self.entity = entity
        if EntityWidget.entityImage == None:
            EntityWidget.entityImage = pg.image.load("./assets/entity_base.png").convert_alpha()
            EntityWidget.lifeImage = pg.image.load("./assets/entity_life.png").convert_alpha()
            EntityWidget.perceptionImage = pg.image.load("./assets/entity_perception.png").convert_alpha()
            EntityWidget.speedImage = pg.image.load("./assets/entity_speed.png").convert_alpha()
            EntityWidget.staminaImage = pg.image.load("./assets/entity_stamina.png").convert_alpha()
            EntityWidget.strongImage = pg.image.load("./assets/entity_strong.png").convert_alpha()
            EntityWidget.toughImage = pg.image.load("./assets/entity_tough.png").convert_alpha()

    def render(self, screen, scale):
        self.width = self.initWidth * scale
        self.height = self.initHeight * scale
        en = pg.transform.scale(EntityWidget.entityImage, (self.width, self.height)) # type: ignore
        r = 0
        g = max(min(int(255 * 0.2 * (self.entity.energy/World.MAX_ENERGY)), 255), 0)
        b = max(min(int(255 * 0.9 * (self.entity.energy/World.MAX_ENERGY)), 255), 0)
        c = pg.Color(r, g, b)

        en.fill(c, special_flags=pg.BLEND_RGBA_MULT)
        screen.blit(en, (self.x, self.y)) # type: ignore

        # life = pg.transform.scale(EntityWidget.lifeImage, (self.width, self.height)) # type: ignore
        # life.set_alpha(128 * self.entity.lifespan) # type: ignore
        # screen.blit(life, (self.x, self.y))

        perception = pg.transform.scale(EntityWidget.lifeImage, (self.width, self.height)) # type: ignore
        perception.set_alpha(128 * self.entity.perception) # type: ignore
        screen.blit(perception, (self.x, self.y))

        speed = pg.transform.scale(EntityWidget.strongImage, (self.width, self.height)) # type: ignore
        speed.set_alpha(128 * self.entity.speed) # type: ignore
        screen.blit(speed, (self.x, self.y))

        stamina = pg.transform.scale(EntityWidget.staminaImage, (self.width, self.height)) # type: ignore
        stamina.set_alpha(128 * self.entity.stamina) # type: ignore
        screen.blit(stamina, (self.x, self.y))

        # strong = pg.transform.scale(EntityWidget.strongImage, (self.width, self.height)) # type: ignore
        # strong.set_alpha(128 * self.entity.strength) # type: ignore
        # screen.blit(strong, (self.x, self.y))

        # tough = pg.transform.scale(EntityWidget.toughImage, (self.width, self.height)) # type: ignore
        # tough.set_alpha(128 * self.entity.toughness) # type: ignore
        # screen.blit(tough, (self.x, self.y))

class FoodWidget(Widget):
    foodImage: Union[pg.surface.Surface, None] = None
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.initWidth = width
        self.width = width
        self.initHeight = height
        self.height = height
        if FoodWidget.foodImage == None:
            FoodWidget.foodImage = pg.image.load("./assets/food.png").convert_alpha()

    def render(self, screen, scale):
        self.width = self.initWidth * scale
        self.height = self.initHeight * scale
        screen.blit(pg.transform.scale(FoodWidget.foodImage, (self.width, self.height)), (self.x, self.y)) # type: ignore