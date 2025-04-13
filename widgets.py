if __name__ == "__main__":
    import main
    exit()

from abc import ABC, abstractmethod
import pygame as pg

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